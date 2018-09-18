#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import csv
import sys
import MeCab
import codecs
mecab = MeCab.Tagger("-Ochasen")
mecab.parse("")
terms = set([])
documents = []
usernames = []
stoplist = []
filename = 'Amazon.csv'
result_filename = filename[0:-4] + '.tfidf.csv'

with codecs.open('Japanese.txt', 'r', 'utf-8') as f:
    for line in f.readlines():
        stoplist.append(line.rstrip('\r\n'))

with codecs.open(filename, 'r', 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        node = mecab.parseToNode(row[5]).next
        documents.append(row[5])
        usernames.append(row[1])
        while node:
            if node.feature.split(",")[0] == u"名詞":
                word = node.surface
                if word not in stoplist:
                    terms.add(word)
            node = node.next


def tf(terms, document):
    """
    for word in document.lower().split():
    :param terms:
    :param document:
    :return:
    """
    sys.stdout.write(".")
    sys.stdout.flush()
    tf_values = [document.count(term) for term in terms]
    return list(map(lambda x: float(x)/sum(tf_values), tf_values))

def idf(terms, documents):
    """
    :param terms:
    :param documents:
    :return:
    """
    import math
    print("start idf")
    return [math.log10(float(len(documents)+1)/sum([bool(term in document) for document in documents])) for term in terms]


def tf_idf(terms, documents):
    """
    :param terms:
    :param documents:
    :return:
    """
    idf_result = idf(terms, documents)
    return [[_tf*_idf for _tf, _idf in zip(tf(terms, document), idf_result)] for document in documents]


terms = list(terms)
print("terms count: %d" % (len(terms)))
print("documents count: %d" % (len(documents)))

tf_idf_result = tf_idf(terms, documents)

result_file = codecs.open(result_filename, 'w', 'utf-8-sig')
line = ""
for term in terms:
    line += term + ","
result_file.write("userID,"+line.strip(",")+"\n")

user_counter = 0
for term_result in tf_idf_result:
    line = ""
    for num in term_result:
       line += str(num) + ","
    result_file.write(usernames[user_counter] + "," + line.strip(",") + "\n")
    user_counter += 1
result_file.close()
