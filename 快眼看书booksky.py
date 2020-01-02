# 面向对象
import requests
from lxml import etree
import os
import time

class Spider(object):
    novel_title = ''
    novel_url = ''
    root_path = '快眼看书booksky\\'
    website_url = 'http://www.booksky.cc'
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

        for num in range(283, 284): # 2123
            chaSrc = self.novel_url + 'read_' + repr(num) + '.html'
            self.content_request(chaSrc)
            time.sleep(0.4)

    # 3.请求文章拿到HTML源代码，抽取文章内容，保存数据
    def content_request(self, chaSrc):
        print(chaSrc)
        response = requests.get(chaSrc, headers=self.header)
        response.encoding = 'utf8'
        html = etree.HTML(response.text)
        chaTitle = html.xpath('//div[@class="title"]/h1/a/text()')
        print(chaTitle)
        content = ''.join(html.xpath('//div[@id="chaptercontent"]/text()'))

        fileName = self.root_path + self.novel_title + '\\' + self.novel_title + '.txt'
        print('正在保存小说文件：' + fileName)
        with open(fileName, 'a', encoding='utf8') as f:
            f.write('\n\n        ' + chaTitle[0].replace('最后的风水先生', '') + '\n\n' + content)

title = '最后的风水先生' #到273
url = 'http://www.booksky.cc/novel/307710/'
spider = Spider()
spider.init_spider(title, url)