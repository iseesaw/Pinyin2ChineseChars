# -*- coding: utf-8 -*-
import json
from bigram import Bigram

class HMM:
    def __init__(self):
        self.load_param()
        self.bigram = Bigram()
    
    def load_param(self):
        self.init_prob = self.read('init_prob')
        self.emiss_prob = self.read('emiss_prob')
        self.trans_prob = self.read('trans_prob')
        self.pinyin_states = self.read('pinyin_states')
        
    def read(self, filename):
        with open('model_params/' + filename + '.json', 'r') as f:
            return json.load(f)
        
    # Viterbi process
    def trans(self, strs):

        # 切分
        seq = self.bigram.dp_search(strs)
        
        # smooth
        self.min_f = -3.14e+100
        length = len(seq)
        
        viterbi = {}
        for i in range(length):
            viterbi[i] = {}
        
        # initize
        for s in self.pinyin_states.get(seq[0]):
            viterbi[0][s] = (self.init_prob.get(s, self.min_f) + 
                   self.emiss_prob.get(s, {}).get(seq[0], self.min_f) + 
                   self.trans_prob.get(s, {}).get('BOS', self.min_f), -1)
        
        # DP 
        # look trans_prob = {post1:{pre1:p1, pre2:p2}, post2:{pre1:p1, pre2:p2}}
        for i in range(length - 1):
            for s in self.pinyin_states.get(seq[i+1]):
                viterbi[i + 1][s] = max([ ( viterbi[i][pre][0] + self.emiss_prob.get(s, {}).get(seq[i+1], self.min_f)
                + self.trans_prob.get(s, {}).get(pre, self.min_f) ,pre) for pre in self.pinyin_states.get(seq[i])])
        
        for s in self.pinyin_states.get(seq[-1]):
            viterbi[length-1][s] = (viterbi[length-1][s][0] + self.trans_prob.get('EOS', {}).get(s, self.min_f),
                   viterbi[length-1][s][1] )
    
    
        words = [None] * length

        words[-1] = max(viterbi[length - 1], key=viterbi[length - 1].get)
        
        for n in range(length-2, -1, -1):
            words[n] = viterbi[n+1][words[n+1]][1]
        
        return ''.join(w for w in words)


'''
HMM只考虑上一个字
jiaohuaqiao
xidazhijie
'''
# 测试
# hmm = HMM()
# print(hmm.trans('zhongwenxinxichuli'))