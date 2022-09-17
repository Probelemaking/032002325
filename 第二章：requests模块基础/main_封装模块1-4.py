#主函数
from 模块1_爬取子页面url import get_kids_links #爬取1-41页的各个网址的url，并保存到yqing.txt
from 模块2_爬取子页面内容 import get_urls    #读取yiqing.txt文件，得到子页面urls
from 模块2_爬取子页面内容 import create_pool #创建线程池，爬取子页面内容，并存入到疫情详细信息文件中
from 模块3_正则获取每日新增确诊 import get_daily_infected #通过正则表达式获取每日新增确诊，并存入到中国每日本土新增无症状人数.html中
from 模块4_正则获取每日新增无症状 import get_daily_asymptomatic #通过正则表达式获取每日新增无症状，并存入到中国每日本土新增无症状人数.html中



#主函数
if __name__ == '__main__':
    # 模块1：爬取1-41页的各个网址的url，并保存到yqing.txt
    get_kids_links()

    #模块2：爬取子页面的内容（使用了线程池），存入到疫情详细信息文件中
    create_pool(get_urls())

    #模块3：通过正则表达式获取每日新增确诊，并存入到中国每日本土新增确诊人数.html中
    path = r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'
    get_daily_infected(path)

    # 模块4：通过正则表达式获取每日新增无症状，并存入到中国每日本土新增无症状人数.html中
    path = r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'
    get_daily_asymptomatic(path)




