import ed
import multiprocessing as mp
import functools
from tfidf_sim import tf_idf

method_names = [
    'lcs',
    'levenshtein',
    'dlevenshtein',
    'double_meta',
    'soundex'
]

methods = [
    ed.lcs_sim,
    ed.levenshtein_sim,
    ed.damerau_levenshtein_sim,
    ed.double_metaphone_sim,
    ed.soundex_sim,
]


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


def sm(name, gender, top_n=50):
    data = read_csv("name_data.txt")
    names = [r[0] for r in data]
    counts = [int(r[2]) for r in data]
    genders = [int(r[1] == "F") for r in data]

    similarities = {}
    processes = []
    parent_connections = []

    def worker(method_name, method, conn):
        print(f"[WORKER]<{method_name}>: START")
        result = (method_name, [method(name, n) for n in names])
        print("[WORKER]: FINISH WORK")
        conn.send([result])
        print(f"[WORKER]<{method_name}>: SEND RESULT")
        conn.close()
        print(f"[WORKER]<{method_name}>: EXIT")

    def tfidf_n(method_name, conn, ng):
        print(f"[WORKER]<{method_name}>: START")
        result = (method_name, tf_idf(names,name, ng=ng))
        print(f"[WORKER]<{method_name}>: FINISH WORK")
        conn.send([result])
        print(f"[WORKER]<{method_name}>: SEND RESULT")
        conn.close()
        print(f"[WORKER]<{method_name}>: EXIT")

    for method_name, method in zip(method_names, methods):
        parent_conn, child_conn = mp.Pipe()
        parent_connections.append(parent_conn)
        process = mp.Process(target=worker, args=(method_name, method, child_conn))
        processes.append(process)
        process.start()

    for i in range(2, 4):
        parent_conn, child_conn = mp.Pipe()
        parent_connections.append(parent_conn)
        process = mp.Process(target=tfidf_n, args=(f"tfidf_{i}", child_conn, i))
        processes.append(process)
        process.start()

    for parent_conn in parent_connections:
        method_name, values = parent_conn.recv()[0]
        parent_conn.close()
        similarities[method_name] = values

    #print(similarities)
    result = {}
    for method_name in similarities:
        values = similarities[method_name]
        indexes = list(range(len(names)))
        indexes.sort(key=lambda x: (values[x], counts[x]), reverse=True)
        meet_minimum_similarity = lambda x: x >= 0.5
        most_similar = []
        for i in indexes[:top_n]:
            if meet_minimum_similarity(values[i]) and gender == genders[i]:
                most_similar.append(names[i])
        result[method_name] = most_similar
    return result


if __name__ == '__main__':
    import time
    start = time.time()
    NAME = "Cathlean"
    N = 50
    print(sm(NAME, 1))
    print(time.time()-start,"s", sep="")