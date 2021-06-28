# coding=utf-8

import pickle
import json
import numpy
import jieba

with open('data/Task4-private-lending-case-data.json', 'r', encoding='utf8') as f:
    raw = json.load(f)
with open('data/tf-idf.pickle', 'rb') as f:
    tfidf = pickle.load(f)
print('finish init search')

def search(keywords, start, end):
    sum = numpy.zeros(tfidf['matrix'].shape[0])
    for keyword in keywords:
        if keyword in tfidf['feature']:
            idx = tfidf['feature'].index(keyword)
            sum += tfidf['matrix'][:, idx].toarray().squeeze()
    idx = numpy.argsort(-sum)
    ans = []
    for i in range(start, end):
        if sum[idx[i]] == 0:
            break
        ans.append(raw[idx[i]])
        ans[i-start]['tfidf'] = sum[idx[i]]
    return ans, numpy.count_nonzero(sum)

def query(keywords, start=0, end=10):
    kw_list = keywords.split()
    cut = []
    for kw in kw_list:
        cut.extend(jieba.lcut(kw))
    result, cnt = search(cut, int(start), int(end))
    ans = {
        'cnt': cnt,
        'items': result
    }
    return json.dumps(ans, ensure_ascii=False)
