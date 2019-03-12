# -*- coding: utf-8 -*-
'''
输入拼音串文件进行转换
'''
from hmm import HMM
import pypinyin


# 测试集语料库文件夹
root = 'corpus'
# 测试集所选语料
'''
sougou
news2017
weibo
'''
file = 'weibo'

'''
对语料库进行标注
'''
def trans():
    with open('{}/{}_gold.txt'.format(root, file) ,'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    with open('{}/{}_test.txt'.format(root, file), 'w', encoding='utf-8', newline='\n') as f:
        for line in lines:
            line = ''.join(w for w in pypinyin.lazy_pinyin(line))
            f.write(line + '\n')

'''
拼音转汉字
'''
def predict():
    hmm = HMM()
    with open('{}/{}_test.txt'.format(root, file), 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    trans_lines = []
    total = len(lines)
    num = 0
    for line in lines:
        try:
            trans_lines.append(hmm.trans(line))
        except:
            print(line)
        num += 1
        if not num % 100:
            print('{}/{}'.format(num, total))

    with open('{}/{}_pred.txt'.format(root, file), 'w', encoding='utf-8', newline='\n') as f:
        for line in trans_lines:
            f.write(line + '\n')

'''
评测结果
'''
def evaluate():
    with open('{}/{}_pred.txt'.format(root, file), 'r', encoding='utf-8') as f:
        pred_lines = f.read().split('\n')
    with open('{}/{}_gold.txt'.format(root, file), 'r', encoding='utf-8') as f:
        gold_lines = f.read().split('\n')
    total_g = 0
    total_p = 0
    right = 0
    for pred_line, gold_line in zip(pred_lines, gold_lines):
        total_g += len(gold_line)
        total_p += len(pred_line)
        # 对位检测
        for i in range(min(len(gold_line), len(pred_line))):
            if gold_line[i] == pred_line[i]:
                right += 1
    print('total gold words: {}'.format(total_g))
    print('total pred words: {}'.format(total_p))
    print('right words: {}'.format(right))
    print('accuracy: {:.4f}%'.format(right*100.0/total_p))

if __name__=='__main__':
    # 测试集转换
    #trans()
    # 预测输出到文件
    predict()
    # 测试代码
    evaluate()

'''
-----------
train news2018 + sougouwords
test news2017 86.4%
test weibo 68.5%
test sougou 57.3%
----------
train news2018
test news2017 86.6%
test weibo 64.5%
test sougou 16.7%
-----------
train sougouwords
test news2017 57.5%
test weibo 53.48%
test sougou 60.5%
'''