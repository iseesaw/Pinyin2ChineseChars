# -*- coding: utf-8 -*-
'''
字典树保存拼音用于搜索
'''
class  Trie(object):
    def __init__(self):
        self.root = {}
        self.end = '/'

    # 添加字典树
    def add(self, s):
        node = self.root
        for c in s:
            node = node.setdefault(c, {})
        node[self.end] = None

    # 搜索字典树
    def contain(self, s):
        node = self.root
        for c in s:
            if c not in node:
                return False
            node = node[c]
        return self.end in node

    # 扫描字典树
    # seq = origin_seq[index:]
    def scan(self, seq, index):
        cnt = index - 1
        # 当前字母
        result = [index]
        node = self.root
        for i, c in enumerate(seq):
            if c not in node:
                return result
            node = node[c]
            cnt += 1
            if self.end in node and i:
                result.append(cnt)
        return result

'''
Uage
trie = Trie()
seq = 'zhong wen xin xi chu li en guo zong ren'
for s in seq.split(' '):
    trie.add(s)

seq = 'zhongguoren'
for i in range(len(seq)):
    result = trie.scan(seq[i:], i)
    for res in result:
        print(seq[i:(res+1)])
'''