import ed
import multiprocessing as mp
import functools
method_names = [
    'lcs',
    'levenshtein',
    'dlevenshtein',
    'soundex',
    'double_meta'
]

methods = [
    ed.lcs_sim,
    ed.levenshtein_sim,
    ed.damerau_levenshtein_sim,
    ed.soundex_sim,
    ed.double_metaphone_sim
]


def top(lst, indexes, n=20):
    result = []
    for i in indexes[:n]:
        result.append(lst[i])
    return result


def read_csv(filename, sep=','):
    result = []
    with open(filename, "r") as fp:
        for line in fp:
            result.append(line.rstrip().split(sep))

    if len(result) == 0:
        raise ValueError("file is empty!")

    length = len(result[0])

    for row in result:
        if length != len(row):
            raise ValueError("malformed result")
    return result


def sm(name, top_n=50):
    data = read_csv("unique_names_with_count.csv")
    names = [r[0] for r in data]
    counts = [r[1] for r in data]
    similarities = {}
    # for m in method_names:
    #     similarities[m] = None
    processes = []
    parent_connections = []

    def worker(method_name, method, conn):
        print("worker starts")
        result = (method_name, [method(name, n) for n in names])

        print("worker finishes work")
        conn.send([result])
        conn.close()

        print("worker finishes sending")

    for method_name, method in zip(method_names, methods):
        parent_conn, child_conn = mp.Pipe()
        parent_connections.append(parent_conn)
        process = mp.Process(target=worker, args=(method_name, method, child_conn))
        processes.append(process)
        process.start()

    # cause for deadlock
    # for process in processes:
    #     process.join()

    for parent_conn in parent_connections:
        method_name, values = parent_conn.recv()[0]
        parent_conn.close()
        similarities[method_name] = values

    similarities['double_meta'] = list(zip(similarities['double_meta'], similarities["dlevenshtein"]))

    result = {}
    for method_name in similarities:
        values = similarities[method_name]
        indexes = list(range(len(names)))
        indexes.sort(key=lambda x: (values[x], counts[x]), reverse=True)
        result[method_name] = top(names, indexes, n=top_n)
    return result


if __name__ == '__main__':
    import time
    start = time.time()
    NAME = "Cathlaen"
    N = 100
    print(sm(NAME, N))
    print(time.time()-start,"s", sep="")