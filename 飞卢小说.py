# 面向对象
import requests
from lxml import etree
import os

class Spider(object):
    # 1.请求首页拿到HTML，抽取小说名，小说链接，创建文件夹
    def index_request(self):
        response = requests.get('https://b.faloo.com/y/0/0/0/0/0/0/1.html')
        html = etree.HTML(response.text)
        Bigtit_list = html.xpath('//a[@class="a_16b"]/@title')
        Bigsrc_list = html.xpath('//a[@class="a_16b"]/@href')
        current_folder_path = os.getcwd()
        novel_folder_path = str(current_folder_path) + '\\novel\\'
        path_is_exist = os.path.exists(novel_folder_path)
        if path_is_exist == False:
            os.mkdir(novel_folder_path)

        for Bigtit, Bigsrc in zip(Bigtit_list, Bigsrc_list):
            print(Bigtit, Bigsrc)
            Bigtit = novel_folder_path + Bigtit
            if os.path.exists(Bigtit) == False:
                os.mkdir(Bigtit)
            self.chapter_request(Bigtit, Bigsrc)

    # 2.请求目录拿到HTML源代码，抽取章名，章链接
    def chapter_request(self, bigTit, bigSrc):
        response = requests.get('https:' + bigSrc)
        html = etree.HTML(response.text)
        chaTitle_list = html.xpath('//div[@class="ni_list"]/table[2]//td[@class="td_0"]/a/text()')
        chaSrc_list = html.xpath('//div[@class="ni_list"]/table[2]//td[@class="td_0"]/a/@href')
        print(chaTitle_list)
        if len(chaSrc_list) > 0:
            for chaTitle, chaSrc in zip(chaTitle_list, chaSrc_list):
                print(chaTitle, chaSrc)
                self.content_request(bigTit, chaTitle, chaSrc)

    # 3.请求文章拿到HTML源代码，抽取文章内容，保存数据
    def content_request(self, bigTit, chaTitle, chaSrc):
        response = requests.get('https:' + chaSrc)
        html = etree.HTML(response.text)
        content = '\n'.join(html.xpath('//div[@id="content"]/text()'))

        fileName = bigTit + '\\' + chaTitle + '.txt'
        print('正在保存小说文件：' + fileName)
        with open(fileName, 'a', encoding='utf-8') as f:
            f.write(content)

spider = Spider()
spider.index_request()