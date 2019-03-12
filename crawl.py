# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor

def crawl():
    '''
    |year | 2017-2018|
    |month | 01-12 |
    |day | 01-30 | 
    |page | 1-6 |
    |index | 01-10 |
    '''
    url = 'http://paper.people.com.cn/rmrb/html/{year}-{month:02d}/{day:02d}/nw.D110000renmrb_{year}{month:02d}{day:02d}_{page}-{index:02d}.htm'
    pool = ThreadPoolExecutor(128)
    # 遍历所有
    for year in [2017]:
        # 创建文件夹
        dirname = str(year)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        for month in range(1, 13):
            # 创建文件夹
            dirname = '{}/{}'.format(year, month)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            print('begining {} {}'.format(year, month))
            for day in range(1, 32):
                # 创建文件夹
                dirname = '{}/{}/{}'.format(year, month, day)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                print('begining {} {} {}'.format(year, month, day))
                # 版面
                for page in range(1, 7):
                    # 文章
                    for index in range(1, 13):
                        # 请求URL
                        addr = url.format(year=year, month=month, day=day, page=page, index=index)
                        # 请求并保存
                        filename = '{year}/{month}/{day}/{page}{index:02d}.txt'.format(year=year, month=month, day=day, page=page, index=index)
                        #article = request(addr, filename)
                        pool.submit(request, addr, filename)
                print('ending {} {} {}'.format(year, month, day))
            print('ending {} {}'.format(year, month))


def request(url, filename):
    try:
        html = requests.get(url).content
        parse = BeautifulSoup(html,'lxml')
        text = parse.find('div', attrs={'class' : 'text_c'})
        title = text.find('h1').get_text()
        sents = text.find_all('p')
        article = title + '\n'
        for sent in sents:
            article += sent.get_text()
            article += '\n'
        # 保存
        with open(filename, 'w', newline='\n', encoding='gb18030') as f:
            f.write(article)
    except Exception as e:
        print('wrong, {}'.format(filename))
        print(e)
        pass

if __name__=='__main__':
    crawl()

