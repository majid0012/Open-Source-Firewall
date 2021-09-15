import pandas as pd

df = pd.read_csv('ht.csv')
bad_chars = ["[", "'", "]"]
nodes = []

df = df.fillna(0)

for i in range(0, len(df)):
    hashtags = df['hashtags'][i]
    urls = df['urls'][i]
    if hashtags != 0:
        hashtags_string = ''.join(i for i in hashtags if i not in bad_chars)
        hashtags_string = hashtags_string.replace(' ', '')
        hashtags_string = hashtags_string.lower()
        hashtags_list = hashtags_string.split(',')

    if urls != 0:
        urls_string = ''.join(i for i in urls if i not in bad_chars)
        urls_string = urls_string.replace(' ', '')
        urls_list = urls_string.split(',')

    if urls != '':
        results = [(i, j) for i in hashtags_list for j in urls_list if j != '' and i != '']

    if results:
        for res in results:
            nodes.append(res)

print(nodes)
