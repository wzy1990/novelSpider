# 面向对象
import requests
from lxml import etree
import os
import time

class Spider(object):
    novel_title = ''
    novel_url = ''
    root_path = '四五小说网45xs\\'
    website_url = 'https://www.45xs.org'
    header = {
        'Referer': website_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
    }

    # 1.创建文件夹
    def init_spider(self, title, url):
        self.novel_title = title
        self.novel_url = url
        current_folder_path = os.getcwd()
        novel_folder_path = str(current_folder_path) + '\\' + self.root_path

        if os.path.exists(novel_folder_path) == False:
            os.mkdir(novel_folder_path)

        novel_path = novel_folder_path + self.novel_title
        if os.path.exists(novel_path) == False:
            os.mkdir(novel_path)
        self.chapter_request()

    # 2.请求目录拿到HTML源代码，抽取章名，章链接
    def chapter_request(self):
        response = requests.get(self.novel_url, headers=self.header)
        response.encoding = 'gbk'
        html = etree.HTML(response.text)
        chaTitle_list = html.xpath('//div[@id="chapterlist"]//li/a/text()')
        chaSrc_list = html.xpath('//div[@id="chapterlist"]//li/a/@href')

        if len(chaSrc_list) > 0:
            for chaTitle, chaSrc in zip(chaTitle_list, chaSrc_list):
                print(chaTitle, chaSrc)
                self.content_request(chaTitle, chaSrc)

    # 3.请求文章拿到HTML源代码，抽取文章内容，保存数据
    def content_request(self, chaTitle, chaSrc):
        print(self.website_url + chaSrc)
        response = requests.get(self.website_url + chaSrc, headers=self.header)
        response.encoding = 'gbk'
        html = etree.HTML(response.text)
        content = ''.join(html.xpath('//div[@id="content"]/text()'))

        fileName = self.root_path + self.novel_title + '.txt'
        print('正在保存小说文件：' + chaTitle)
        with open(fileName, 'a', encoding='utf8') as f:
            f.write('\n\n        ' + chaTitle + '\n\n' + content)

title = '女权之姐姐饶命'
url = 'https://www.45xs.org/txt/77720/'
spider = Spider()
spider.init_spider(title, url)