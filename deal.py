# -*- coding: utf-8 -*-
import re
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.font_manager import FontProperties

'''
转换文件格式为utf-8
'''
def deal():
    filename = 'files/sougou_gold.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    p = re.compile(r'^[\u4e00-\u9fa5]{2,}$')
    newlines = []
    with open('files/trans_prob.json') as f:
        trans_prob = json.load(f)

    for line in lines:
        line = line.replace(' ', '')
        if line == '':
            continue
        if re.match(p, line):
            for w in line:
                if not w in trans_prob:
                    continue
            newlines.append(line)
    num = np.random.randint(0, len(newlines)-1, (3000))
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        for n in num:
            f.write(newlines[n] + '\n')


def load(isnews):
    if isnews:
        filename = 'corpus/peoplenews2018.txt'
    else:
        filename = 'corpus/sougouwords.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    return lines
'''
结果可视化分析
人民日报2018和搜狗词库语料库的长度分布
正态分布图条形图

对于人民日报2017结果分析
    各长度全对的比例以及正确率
柱状图、折线图
'''
def show_trainingset():
    sns.set()

    news_lines = load(isnews=True)
    newsx = [len(line) for line in news_lines]
    newsx = pd.Series(newsx, name='People Daily News2018')

    sougou_lines = load(isnews=False)
    sougoux = [len(line) for line in sougou_lines]
    sougoux = pd.Series(sougoux, name='Sougou Words')

    f, axes = plt.subplots(nrows=1, ncols=2, sharex=True)
    sns.despine(left=True)

    # params
    # False or True
    # kde=False - 变化折线
    # hist=False - 条形图
    sns.distplot(newsx, ax=axes[0])

    sns.distplot(sougoux, ax=axes[1])

    plt.suptitle('length of sentence in corpus')
    plt.show()

def load_result(filename):
    with open('corpus/'+filename, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    return lines

'''
各长度词、句的正确率
'''
def analysis(predseqs, goldseqs, maxlen):
    acc = {}
    for predseq, goldseq in zip(predseqs, goldseqs):
        right = 0
        alltrue = True
        for index in range(min(len(predseq), len(goldseq))):
            if predseq[index] == goldseq[index]:
                #right += 1
                alltrue = False
                break

        num = acc.get(len(goldseq), (0, 0))
        if alltrue:
            num = (num[0]+1, num[1]+1)
        else:
            num = (num[0], num[1]+1)
        # (num[0]+right, num[1]+len(goldseq))
        acc[len(goldseq)] = num

    result = np.zeros(maxlen)
    for key in acc.keys():
        num = acc.get(key)
        result[key] = num[0]/(num[1]+1)
    return result

def show_result():
    newspred = load_result('news2017_pred.txt')
    newsgold = load_result('news2017_gold.txt')

    weibopred = load_result('weibo_pred.txt')
    weibogold = load_result('weibo_gold.txt')

    sougoupred = load_result('sougou_pred.txt')
    sougougold = load_result('sougou_gold.txt')

    maxlen = max([
            max([max(len(s1), len(s2)) for s1,s2 in zip(newspred, newsgold)]),
            max([max(len(s1), len(s2)) for s1,s2 in zip(weibopred, weibogold)]),
            max([max(len(s1), len(s2)) for s1,s2 in zip(sougoupred, sougougold)])
        ]) + 1
    weiboresult = analysis(weibopred, weibogold, maxlen)
    newsresult = analysis(newspred, newsgold, maxlen)
    sougouresult = analysis(sougoupred, sougougold, maxlen)

    myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=14)
    sns.set(font=myfont.get_name())

    data = pd.DataFrame(data = {
        'news2017': newsresult,
        'weibo' : weiboresult,
        'sougou' : sougouresult
        },
        index = [i+1 for i in range(maxlen)])

    sns.lineplot(data=data, palette='tab10', linewidth=2.5)
    plt.title('各测试集上不同长度词/句的完全正确率')
    plt.show()
    
if __name__ == '__main__':
    #plt.style.use('ggplot')
    #deal()
    #show_trainingset()

    show_result()