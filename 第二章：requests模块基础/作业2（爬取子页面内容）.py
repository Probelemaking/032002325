#使用selenium模块访问子页面，获取其中文本信息，并存到文件夹中
import random
from time import sleep
from selenium import webdriver
from lxml import etree
from selenium.webdriver.firefox.options import Options  # 显示无可视化界面
import os
from multiprocessing.dummy import Pool

# 创建文件夹
file = '疫情详细信息'
if not os.path.exists(file):
    os.mkdir(file)

#读取文件并保存
f = open("yiqing.txt", "r", encoding='utf-8')
urls = f.readlines()
for i in range(len(urls)):
    urls[i] = urls[i].rstrip('\n')

# 显示无可视化界面
options = Options()
options.headless = True

#用于获取每一天公告的具体内容
def get_name(url):
    bro = webdriver.Firefox(options=options)
    bro.get(url)
    page_text = bro.page_source        #直接返回源码
    while ('疫情通报' not in page_text):        #如果访问失败，重复访问
        sleep(random.randint(0, 3) * 0.1 / 100)
        bro.get(url)
        page_text = bro.page_source

    #内容定位
    tree = etree.HTML(page_text)
    r = tree.xpath('//div[@class="con"]//text()')
    filecontents = ''.join(r)                   #获取文本内容
    r=str(tree.xpath('//div[@class="source"]/span[1]/text()')[0])  #获取发布时间
    release_time = r.split('发布时间：\n')[1].strip()
    title = tree.xpath('//div[@class="tit"]/text()')[0] #获取标题
    filename = release_time + '（发布时间）' + title + '.html' #定义文件名
    with open(file + '/' + filename, 'w', encoding='utf8') as fp:
        fp.write(filecontents)
    print(filename + "保存成功！！！")
    bro.quit()

#创建线程池，并启动
pool = Pool(7)
pool.map(get_name,urls)
pool.close()
pool.join()
print("所有数据爬取完成")