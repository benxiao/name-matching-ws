
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import partial


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


def feature_analyser(string, n=4):
    lst = []
    for i in range(2, n + 1):
        lst.extend(string[j:j + i] for j in range(len(string) - (i - 1)))
    return lst


def tf_idf(names, name, ng=2):
    analyser = partial(feature_analyser, n=ng)
    vectorizer = TfidfVectorizer(min_df=1, analyzer=analyser)
    tf_idf_matrix = vectorizer.fit_transform(names)
    lst = cosine_similarity(vectorizer.transform([name]), tf_idf_matrix)[0]
    return lst


if __name__ == '__main__':
    data = read_csv("unique_names_with_count.csv")
    names = [r[0] for r in data]
    print(tf_idf(names, 'David'))