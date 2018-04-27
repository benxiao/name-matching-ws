from metaphone import doublemetaphone


def levenshtein_distance(s1, s2):
    m = len(s1) + 1
    n = len(s2) + 1
    tbl = [[0] * n for _ in range(m)]
    for i in range(n):
        tbl[0][i] = i
    for i in range(m):
        tbl[i][0] = i
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            tbl[i][j] = min(tbl[i][j - 1] + 1, tbl[i - 1][j] + 1, tbl[i - 1][j - 1] + cost)

    return tbl[m - 1][n - 1]


def damerau_levenshtein_distance(s1, s2):
    m = len(s1) + 1
    n = len(s2) + 1
    tbl = [[0] * n for _ in range(m)]
    for i in range(n):
        tbl[0][i] = i
    for i in range(m):
        tbl[i][0] = i
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            tbl[i][j] = min(tbl[i][j - 1] + 1, tbl[i - 1][j] + 1, tbl[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and s1[i - 2] == s2[j - 1] and s1[i - 1] == s2[j - 2]:
                tbl[i][j] = min(tbl[i][j], tbl[i - 1][j - 1])

    return tbl[m - 1][n - 1]


def lcs_sim(s1, s2):
    l1 = len(s1) + 1
    l2 = len(s2) + 1
    tbl = [([0] * l2) for _ in range(l1)]
    for i in range(1, l1):
        for j in range(1, l2):
            if s1[i - 1] == s2[j - 1]:
                tbl[i][j] = tbl[i - 1][j - 1] + 1
            else:
                tbl[i][j] = max(tbl[i][j - 1], tbl[i - 1][j])
    return tbl[l1 - 1][l2 - 1] / (max(l1, l2) - 1)


def soundex(name):
    lookup = dict(b=1, f=1, p=1,
                  v=1, c=2, g=2,
                  j=2, k=2, q=2,
                  s=2, x=2, z=2,
                  d=3, t=3, l=4,
                  m=5, n=5, r=6)
    characters = name[1:]
    characters = [lookup[c] for c in characters if c in lookup]
    previous = None
    result = []
    for c in characters:
        if previous != c:
            result.append(c)
            previous = c

    while len(result) < 3:
        result.append(0)

    return name[0] + "".join(str(c) for c in result[:3])


def soundex_sim(s1, s2):
    p1 = soundex(s1)
    p2 = soundex(s2)
    if p1[0] != p2[0]:
        return 0
    return sum(i == j for i, j in zip(p1, p2)) / 4


def levenshtein_sim(s1, s2):
    return 1 - levenshtein_distance(s1, s2) / max(len(s1), len(s2))


def damerau_levenshtein_sim(s1, s2):
    return 1 - damerau_levenshtein_distance(s1, s2) / max(len(s1), len(s2))


# this doesn't work well at the moment
# for example, it includes unlikely search terms
def double_metaphone_sim(s1, s2):
    h1 = doublemetaphone(s1)
    h2 = doublemetaphone(s2)
    if h1[0] == h2[0]:
        return 1

    # in case primary key and alternate key are equal
    if h1[0] == h2[1] or h1[1] == h2[0]:
        return 0.75

    # in case the alternate key is empty
    # check to see if one of the them is not empty
    if (h1[1] or h2[1]) and (h1[1] == h2[1]):
        return 0.5

    return 0

if __name__ == '__main__':
    print("christen", soundex("christen"))
    print("peter", soundex("peter"))
    print("alex", soundex("alex"))
    print("alexander", soundex("alexander"))
    print("stephen", soundex("stephen"))

    pairs = [
        ("Katherine", "Catherine"),
        ("Anna", "Ana"),
        ("Somchai", "Som Chai"),
        ("Somchai", "Somechay"),
        ("Somchai", "Someshai"),
        ("Somchai", "Somchia"),
        ("Somchai", "Somchair"),
        ("Somchai", "Somchaiy"),
        ("Somchai", "Somcai")
    ]

    for n0, n1 in pairs:
        print(n0, n1, f"dist:{levenshtein_sim(n0, n1)}")

    print(damerau_levenshtein_distance('soup', 'suop'))
    print(levenshtein_distance('soup', 'suop'))
