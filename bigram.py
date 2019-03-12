# -*- coding: utf-8 -*-
'''
实现bigram切分输入拼音串
'''
from trie import Trie
import json

class Bigram():
    def __init__(self):
        self.minfreq = -3.14e+100
        self.load()
        self.construct_Trie()

    def load(self):
        root = 'model_params'
        with open(root + '/bidic.json', 'r') as f:
            self.bidic = json.load(f)
        with open(root + '/pinyin.json', 'r') as f:
            self.pinyindic = json.load(f)

    def construct_Trie(self):
        self.trie = Trie()
        for key in self.pinyindic.keys():
            self.trie.add(key)

    def construct_DAG(self, seq):
        # {key: list}
        self.DAG = {}
        for i in range(1, len(seq) - 1):
            self.DAG[i] = self.trie.scan(seq[i:-1], i)
        # BOS EOS
        self.DAG[len(seq) - 1] = [len(seq) - 1]
        self.DAG[0] = [0]

    def dp_search(self, seq):
        seq = '^' + seq + '$'
        self.construct_DAG(seq)
        # prob max
        viterbi = {}
        for i in range(len(seq)):
            viterbi[i] = {}
        # { i :{ end1: (prob, next), end2 : (prob, next) }}
        viterbi[len(seq) - 1][len(seq) - 1] = (0., len(seq))
        # 反向DP
        for i in range(len(seq) - 2, -1, -1):
            # 对每个wi起始的词求最大概率
            for x in self.DAG[i]:
                # P(wx+1...wy | wi..wx)*viterbi[x+1][index][0]
                prob_index = max(
                    (self.bidic.get(seq[x + 1:y + 1], {}).get(seq[i:x + 1], self.minfreq) +
                     viterbi.get(x + 1)[y][0], y) for y in self.DAG[x + 1])
                viterbi[i][x] = prob_index

        # BOS
        end = max((self.bidic.get(seq[1:y + 1], {}).get(seq[0], self.minfreq) +
                   viterbi.get(1)[y][0], y) for y in self.DAG[1])[1]
        # 回溯*
        start = 1
        segs = []
        while start < len(seq) - 1:
            segs.append(seq[start:end + 1])
            temp = start
            start = end + 1
            # print(viterbi[temp][end][0])
            end = viterbi[temp][end][1]
        return segs