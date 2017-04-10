import networkx as nx
import numpy as np
import math
import re

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

def main():
    path = 'C:\\Users\\geeta\\PycharmProjects\\summarizer\\new_complete_corpus\\'
    for x in range(1, 76):
        # fileName = path + 'machine_output\\tokenized' + str(x) + ".txt"

        initFileName = path + 'input\\input' + str(x) + ".txt"
        initSentences = []
        with open(initFileName, 'r', encoding='utf-8') as initDoc:
            initDocData = initDoc.read().replace('\n', '')
            initDocData = initDocData.replace(u'?', u'\u0964')
            initSentences = initDocData.split(u'\u0964')

        tokenizedFileName = path + 'machine_output\\tokenized' + str(x) + ".txt"
        # tokenizedFileName = path + 'input\\input' + str(x) + ".txt"
        machineFileName = path + 'machine_output\\article' + str(x) + "_system1.txt"
        # machineFileName = path + 'machine_output\\machine' + str(x) + ".txt"
        rankedSentencesDoc = open(machineFileName, 'w',encoding='utf-8')

        with open(tokenizedFileName, 'r', encoding='utf-8') as document1:
            docData = document1.read().replace('\n', '')
            docData = docData.replace(u'?', u'\u0964')
            data = docData.split(u'\u0964')
            rankedSentences = textrankTfIdf(data)
            orderedSentences = orderSentences(rankedSentences, data, initSentences)
            for ordered in orderedSentences:
                if ordered != "":
                    rankedSentencesDoc.write(str(ordered) + u'\u0964' + "\n")



def textrankTfIdf(document):
    # sentence_tokenizer = PunktSentenceTokenizer()
    # sentences = sentence_tokenizer.tokenize(document, 'hindi')

    sentences = document
    bow_matrix = CountVectorizer().fit_transform(sentences)
    # normalized = TfidfTransformer(norm='l2', use_idf=True, use_bm25idf=True, smooth_idf=True,
    #              delta_idf=False, sublinear_tf=False, bm25_tf=True).fit_transform(bow_matrix)

    normalized = TfidfTransformer().fit_transform(bow_matrix)
    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    return sorted(((scores[i], s) for i, s in enumerate(sentences)),
                  reverse=True)



def orderSentences(rankedList, data, initSentences):
    index = ['']*len(data)
    # print(rankedList)
    for eachRanked in rankedList[0:int(math.ceil(0.3*len(rankedList)))]:
        sen = eachRanked[1]
        index[data.index(sen)] = initSentences[data.index(sen)]
        # print(data.index(sen))
    return index

if __name__ == "__main__": main()