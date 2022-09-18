# 爬取1-41页的各个网址的url
import os
import random
from time import sleep
import requests
from bs4 import BeautifulSoup

# 爬取1-41页的各个网址的url
def get_kids_links():
    # 创建文件夹
    fp = 'yiqing.txt'
    if not os.path.exists(fp):
        os.mkdir(fp)

    # 初始化设置
    first_page = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"  # 卫健委第一页的网址
    next_page = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_%d.shtml"  # 卫健委第二页到四十一页通用的网址
    headers = {
        'User_Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
    }

    fp = open('./yiqing.txt', 'w', encoding='utf-8')

    # 爬取第一页到四十一页的每一天的url
    for page_num in range(1, 42):
        if page_num:
            new_url = first_page  # 第一天的url
        else:
            new_url = format(next_page % page_num)  # 后面的url，通过format给%d附带上页码
        res = requests.get(url=new_url, headers=headers)  # 请求网址
        page_text = res.text                             # 获取内容
        soup = BeautifulSoup(page_text, 'lxml')
        li_list = soup.select('.zxxx_list > li > a')  # 定位url部分
        while res.status_code != 200:  # 如果访问失败，就重复访问
            sleep(random.randint(0, 3) * 0.1 / 100)
            res = requests.get(url=new_url, headers=headers)    # 与上述相同
            page_text = res.text
            soup = BeautifulSoup(page_text, 'lxml')
            li_list = soup.select('.zxxx_list > li > a')

        # 存入yiqing.txt文件中
        for li in li_list:
            title = li.string
            detail_url = 'http://www.nhc.gov.cn' + li['href']  # 所需要的详细网址
            fp.write(detail_url + '\n')
            # fp.write(title + ':' + detail_url + '\n')
        print("第" + str(page_num) + "页爬取成功！！！")
    print("已生成yiqing.txt！！！")
    print("所有数据爬取完成！！！")


if __name__ == '__main__':
    get_kids_links()
