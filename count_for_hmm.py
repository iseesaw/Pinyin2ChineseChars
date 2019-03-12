# -*- coding: utf-8 -*-
'''
HMM参数计算
init - 汉字初始概率
trans - 汉字间转移概率
emiss - 拼音对多音汉字的发射概率
'''
import pypinyin 
import json
import math
from count_for_bigram import load

# 模型参数保存文件夹
dirname = 'files'
'''
计算汉字初始概率
初步计算每个汉字作为句首的概率
'''
def count_init(seqs):
    init_prob = {}
    num = 0
    len_ = len(seqs)
    for seq in seqs:
        init_prob[seq[0]] = init_prob.get(seq[0], 0) + 1
        
        num +=1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
    
    # normalize
    # log
    total = len(seqs)
    for key in init_prob.keys():
        init_prob[key] = math.log(init_prob.get(key) / total)
    
    save('init_prob', init_prob)

'''
计算拼音-汉字发射概率
调用pypinyin对每句话进行拼音标注
记录每个拼音对应的汉字以及次数（多音汉字即为拼音的状态）
********状态（汉字）的发射概率
观察序列 - 拼音串
emiss_prob = {
        word1 : {pinyin11: num11, pinyin12: num12, ...},
        word2 : {pinyin21: num21, pinyin22: num22, ...},
        ...
}
'''
def count_emiss(seqs):
    emiss_prob = {}
    num = 0
    len_ = len(seqs)
    for seq in seqs:
        # 句子转拼音
        pinyin = pypinyin.lazy_pinyin(seq)
        # 汉字-拼音 发射概率
        for py, word in zip(pinyin, seq):
            if not emiss_prob.get(word, None):
                emiss_prob[word] = {}
            emiss_prob[word][py] = emiss_prob[word].get(py, 0) + 1
            
        num +=1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
            
    # normalize
    # log
    for word in emiss_prob.keys():
        total = sum(emiss_prob.get(word).values())
        for key in emiss_prob.get(word):
            emiss_prob[word][key] = math.log(emiss_prob[word][key] / total)
     
    save('emiss_prob', emiss_prob)
'''
计算汉字（状态）间转移概率
计算每个句子中汉字转移概率
'''
def count_trans(seqs):
    trans_prob = {}
    num = 0
    len_ = len(seqs)
    for seq in seqs:
        seq = [w for w in seq]
        seq.insert(0, 'BOS')
        seq.append('EOS')
        
        for index, post in enumerate(seq):
            if index:
                pre = seq[index - 1]
                if not trans_prob.get(post, None):
                    trans_prob[post] = {}
                trans_prob[post][pre] = trans_prob[post].get(pre, 0) + 1
            
        num +=1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
            
    # normalize
    for word in trans_prob.keys():
        total = sum(trans_prob.get(word).values())
        for pre in trans_prob.get(word).keys():
            trans_prob[word][pre] = math.log(trans_prob[word].get(pre) / total)
     
    save('trans_prob', trans_prob)
    
'''
统计同音字
作为拼音的所有状态
'''
def count_pinyin_states():
    with open(dirname+'/emiss_prob.json') as f:
        emiss_prob = json.load(f)
    
    data = {}
    for key in emiss_prob.keys():
        for pinyin in emiss_prob.get(key):
            if not data.get(pinyin, None):
                data[pinyin] = []
            data[pinyin].append(key)
    
    with open(dirname+'/pinyin_states.json', 'w') as f:
        json.dump(data, f)
    
'''
概率句子写入json文件
'''
def save(filename, data):
    with open(dirname+'/' + filename + '.json', 'w') as f:
        json.dump(data, f, indent=2)
        

def count():
    seqs = load()

    print('Count init prob...')
    count_init(seqs)
    
    print('Count emiss prob...')
    count_emiss(seqs)
    
    print('Count trans prob...')
    count_trans(seqs)
    
    print('Count pinyin states...')
    count_pinyin_states()
    
    print('That is all...')


if __name__=='__main__':
    count()

    
    