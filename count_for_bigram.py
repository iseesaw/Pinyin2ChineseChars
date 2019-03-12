# -*- coding: utf-8 -*-
'''
计算bigram参数
bigram拼音二元词典用于动态规划计算最优子串
bigram拼音表用于构建字典树
'''
import pypinyin
import json
import math
import re

# bigram参数保存文件夹
dirname = 'files'
'''
加载语料库
语料集包括：搜狗词库（短句）、人民日报2018（长句）
'''
def load():
    file1 = 'corpus/peoplenews2018.txt'
    file2 = 'corpus/sougouwords.txt'
    with open(file2, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')[:-1]
    # with open(file2, 'r', encoding='utf-8') as f:
    #     lines.extend(f.read().split('\n'))[:-1]

    return lines

'''
计算拼音二元词典
{
    post:{
        pre1: p1,
        pre2: p2
        ....
    }
    ...
}
'''
def count_bidic():
    lines = load()
    chinese = re.compile(r'^[\u4e00-\u9fa5]{2,}$')
    bidic = {}
    all_pinyin = {}
    num = 0
    total = len(lines)
    for line in lines:
        if not re.match(chinese, line):
            continue

        pinyin = pypinyin.lazy_pinyin(line)
        for py in pinyin:
            all_pinyin[py] = all_pinyin.get(py, 0) + 1
        pinyin.insert(0, 'BOS')
        pinyin.append('EOS')
        for index, py in enumerate(pinyin):
            # 从第二个开始
            if index:
                # 不能存在则建立
                if not bidic.get(py, None):
                    bidic[py] = {}
                # 计算
                bidic[py][pinyin[index-1]] = bidic[py].get(pinyin[index-1], 0) + 1
        num += 1
        if not num % 10000:
            print('{}/{}'.format(num, total))

    # 归一化
    # TODO： 对谁归一化？？
    for key in bidic.keys():
        s = sum(bidic[key].values())
        for k in bidic.get(key).keys():
            bidic[key][k] = math.log(bidic[key][k] / s)

    s = sum(all_pinyin.values())
    for key in all_pinyin.keys():
        all_pinyin[key] = all_pinyin.get(key) / s


    with open(dirname+ '/bidic.json', 'w') as f:
        json.dump(bidic, f, indent=2)

    with open(dirname + '/pinyin.json', 'w') as f:
        json.dump(all_pinyin, f, indent=2)


if __name__=='__main__':
    count_bidic()