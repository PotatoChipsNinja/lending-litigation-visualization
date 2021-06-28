# coding=utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
import json
import jieba
import re
import pickle

with open('data/Task4-private-lending-case-data.json', 'r', encoding='utf8') as f:
    raw = json.load(f)

corpus = []
for i, article in enumerate(raw):
    print('%d / %d\r' % (i+1, len(raw)), end='')
    cut = jieba.lcut(re.sub(r'\W*', '', '%s %s' % (article['title'], article['content'])))
    cut.append(article['caseNO'])
    cut.extend(article['label']['level1'])
    cut.extend(article['label']['level2'])
    cut.extend(article['label']['level3'])
    corpus.append(' '.join(cut))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

save = {
    'feature': vectorizer.get_feature_names(),
    'matrix': X
}
with open('data/tf-idf.pickle', 'wb') as f:
    pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
