#主函数
from 模块1_爬取子页面url import get_kids_links     # 爬取1-41页的各个网址的url，并保存到yqing.txt
from 模块2_爬取子页面内容 import get_urls    # 读取yiqing.txt文件，得到子页面urls
from 模块2_爬取子页面内容 import create_pool     # 创建线程池，爬取子页面内容，并存入到疫情详细信息文件中
from 模块3_1正则获取每日新增确诊 import get_daily_infected  # 通过正则表达式获取每日新增确诊，并存入到中国每日本土新增无症状人数.html中
from 模块3_2正则获取每日新增无症状 import get_daily_asymptomatic     # 通过正则表达式获取每日新增无症状，并存入到中国每日本土新增无症状人数.html中
from 模块4_1可视化处理每日新增确诊 import draw_new_infected      # 生成一个月的可视化新增确诊人数大屏
from 模块4_2可视化处理每日新增无症状 import draw_new_asymptomatic   # 生成一个月的可视化无症状确诊人数大屏


# 主函数
if __name__ == '__main__':
    # 模块1：爬取1-41页的各个网址的url，并保存到yqing.txt
    get_kids_links()

    # 模块2：爬取子页面的内容（使用了线程池），存入到疫情详细信息文件中
    create_pool(get_urls())

    # 模块3_1：通过正则表达式获取每日新增确诊，并存入到中国每日本土新增确诊人数.html中
    path = r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'
    get_daily_infected(path)

    # 模块3_2：通过正则表达式获取每日新增无症状，并存入到中国每日本土新增无症状人数.html中
    path = r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'
    get_daily_asymptomatic(path)

    # 模块4：生成可视化数据大屏
    data = []
    date_list = []
    total_num = []
    total1_num = []
    time_list = []
    minNum = 0
    maxNum = 50
    maxDay = 0
    minDay = 0
    date = ''
    selected_result=input("输入您想查询的种类（1为每日新增确诊，2为新增无症状）：")
    if selected_result == '1':
        draw_new_infected()     # 生成中国每日本土新增确诊人数（可视化界面）
    else:
        draw_new_asymptomatic()     # 生成中国每日本土新增无症状人数（可视化界面）
