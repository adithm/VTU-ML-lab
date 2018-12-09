import pandas as pd
from math import *
from pprint import pprint

df = pd.read_csv('Tennis.csv')
data = df.values.tolist()
attributes = df.columns.values.tolist()

def entropy(pos, neg):
    if pos == 0 or neg == 0:
        return 0
    tot = pos + neg
    return -pos / tot * log(pos / tot, 2) - neg / tot * log(neg / tot, 2)

def gain(data, attr, pos, neg):
    d = {}
    for i in data:
        if i[attr] not in d:
            d[i[attr]] = {}
        d[i[attr]][i[-1]] = 1 + d[i[attr]].get(i[-1], 0)
    E, acu = entropy(pos, neg), 0
    for i in d:
        tot = d[i].get('Yes', 0) + d[i].get('No', 0)
        acu += tot / (pos + neg) * entropy(d[i].get('Yes', 0), d[i].get('No', 0))
    return E - acu


def build(data, attributes):
    sz = len(data[0]) - 1
    max_gain, root = -1, -1
    pos = len([x for x in data if x[-1] == 'Yes'])
    neg = len(data) - pos
    
    if neg == 0:
        return 'Yes'
    if pos == 0:
        return 'No'
    
    for i in range(sz):
        cur_gain = gain(data, i, pos, neg)
        if cur_gain > max_gain:
            max_gain, root = cur_gain, i
         
    fin, res = {}, {}
    uniq_attr = set([x[root] for x in data])
    for i in uniq_attr:
        res[i] = build([x[:root] + x[root + 1:] for x in data if x[root] == i], attributes[:root] + attributes[root+1:])

    fin[attributes[root]] = res
    return fin

tree = build(data, attributes)
pprint(tree)
