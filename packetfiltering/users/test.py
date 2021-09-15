import pandas as pd

df = pd.read_csv('t.csv')

bad_chars = ["[", "'", "]"]

new_list = []


def check_pairs(source):
    result = []
    for p1 in range(len(source)):
        for p2 in range(p1+1, len(source)):
            result.append([source[p1], source[p2]])
    return result


for i in range(0, 6):
    data = df['hashtags'][i]

    test_string = ''.join(i for i in data if i not in bad_chars)
    test_string = test_string.replace(' ', '')
    test_string = test_string.lower()
    data_list = test_string.split(',')

    pairings = check_pairs(data_list)

    for j in pairings:
        if j != '':
            j.sort()
            new_list.append(j)

Edge = []
counter = []

for pair in new_list:
    count = 0
    for pairs in new_list:
        if pair == pairs:
            count += 1
    if pair not in Edge:
        Edge.append(pair)
        counter.append(count)

for edge, c in zip(Edge, counter):
    edge.append(c)

Edge_list = []

for edges in Edge:
    Edge_list.append(tuple(edges))

print(Edge_list)
