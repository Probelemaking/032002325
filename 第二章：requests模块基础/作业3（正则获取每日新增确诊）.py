import re
import os
import pandas as pd
#1. 统计中国大陆每日本土新增确诊人数及新增无症状感染人数，境外输入类型和疑似病例等无需统计。
#2. 统计所有省份包括港澳台每日本土新增确诊人数及新增无症状感染人数，境外输入类型和疑似病例等无需统计。
#3. 将统计的数据利用编程工具或开发包自动写入Excel表中。


path = r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'
path_list = os.listdir(path)


time_city_dic={}    #用于导入表格
date_number=0       #用于编写序号
xianggang_list=[0]  #用于计算香港每日新增而创建的列表
aomen_list=[0]      #用于计算澳门每日新增而创建的列表
taiwan_list=[0]     #用于计算台湾每日新增而创建的列表


for file_list in path_list:

    date_number= date_number + 1
    province_list = {'河北': 0, '山西': 0, '辽宁': 0, '吉林': 0, '黑龙江': 0, '江苏': 0, '浙江': 0, '安徽': 0, '福建': 0,
           '江西': 0,'山东': 0, '河南': 0, '湖北': 0, '湖南': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0, '云南': 0,
           '陕西': 0, '甘肃': 0, '青海': 0, '台湾': 0, '内蒙古': 0, '广西': 0, '西藏': 0, '宁夏': 0, '新疆': 0,'北京': 0,
           '天津': 0, '上海': 0, '重庆': 0, '香港': 0, '澳门': 0,'兵团':0,'中国大陆（无港澳台）':0}
    ex = '(.*)\（.'
    date = re.findall(ex, file_list)    #从文件名中找到发布的时间

    path=r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'+'\\'+file_list
    with open(path, "r", encoding='utf-8') as f:    #打开具体页面
        file = f.readlines()
    filecontent=''.join(file)       #得到本文信息
    ex='(本土病例.*)'
    str1=re.findall(ex,filecontent,re.M)    #定位目标段落

    for item in str1:
        if('解除' not in item):   #排除掉其余不是目标的段落
            # jishu=0
            ex='本土病例(\d.*?)例'   #找到中国大陆每日本土新增确诊人数
            all_person_number = re.findall(ex, item)
            # print(all_person_number)
            if (len(all_person_number) != 0):
                # print(all_person_number)
                province_list["中国大陆（无港澳台）"]=int(all_person_number[0])
            ex = '(\（.*?\）)?[，；。].*'                #用于找到各个省份信息
            all_province_txt = re.findall(ex, item)
            # print(all_province_txt)

            if (all_province_txt[0]== '' or len(all_province_txt)==0):
                ex = '([\（，].*?[\）；]?)?[，；。].*'     # 特例：本土病例均在某地且无括号，如2020-6-23日 本土病例13例，均在北京；
                all_province_txt = re.findall(ex, item)

            #在省份信息找到每个省份的数据
            for city in province_list.keys():
                if (len(all_province_txt) != 0):
                    if (city in all_province_txt[0]):
                        ex = city + '(\d*)例'        #用于到找省份后的数字
                        num = re.findall(ex, all_province_txt[0])
                        if (len(num) != 0):
                            province_list[city] += int(num[0])
                            # jishu+= int(num[0])
                            # print(jishu)
                        else:
                            ex = '.*?(\d.*?)例.*?'   #特例，疫情均在某地且省份后无数字，如本土病例x例（在山西）
                            num = re.findall(ex, item)
                            if (len(num)!= 0):
                                #-----------------------------------
                                if(city=='河北' and "河北区" in all_province_txt[0]):  #天津有个叫河北区的地方，特判
                                        continue                                     #如，2022-02-03 天津:河北区三例（特例）
                                #--------------------------------------
                                province_list[city] += int(num[0])
                                # jishu += int(num[0])
                            else:
                                province_list[city]+=1   #数字在本土病例（只有一天这样）前面，如2020-05-03 1例为本土病例（在山西）
                                province_list["中国大陆（无港澳台）"]+=1
            # if(len(all_person_number) != 0 and jishu!=int(province_list["中国大陆（无港澳台）"])):
            #     print("no!!!!!!!!!!!!!!!")
            #     print(province_list["中国大陆（无港澳台）"])
            #     print(jishu)

    #下列统计港澳台每日新增
    ex='(香港特别行政区.*)' #匹配目标段落，如['香港特别行政区401942例（出院79100例，死亡9820例），澳门特别行政区793例（出院787例，死亡6例），台湾地区5754683例（出院13742例，死亡10329例）。']
    str2=re.findall(ex,filecontent,re.M)
    # print(str2)
    yesterday_number= date_number - 1
    if (len(str2) != 0):
        if("香港特别行政区" in str2[0]):
            ex ='香港特别行政区(\d*)例'     #找到香港后面感染人数
            num = re.findall(ex, str2[0])
            if (len(num) != 0):
                xianggang_list.append(int(num[0]))
                province_list["香港"] += xianggang_list[date_number] - xianggang_list[yesterday_number] #今天与昨天相减即为新增

        if("澳门特别行政区" in str2[0]):
            ex ='澳门特别行政区(\d*)例'     #找到澳门后面感染人数
            num = re.findall(ex, str2[0])
            if (len(num) != 0):
                aomen_list.append(int(num[0]))
                province_list["澳门"] += aomen_list[date_number] - aomen_list[yesterday_number]      #今天与昨天相减即为新增

        if("台湾地区"or"中国台湾" in str2[0]):
            ex ='台湾.*?(\d*)例'       #找到台湾后面感染人数
            num = re.findall(ex, str2[0])
            if (len(num) != 0):
                taiwan_list.append(int(num[0]))
                province_list["台湾"] += taiwan_list[date_number] - taiwan_list[yesterday_number]     #今天与昨天相减即为新增
    else:
        #特例，当天发的不是平时的疫情通告，2020-04-17（发布时间）[武汉发布] 武汉市新冠肺炎确诊病例数确诊病例死亡数订正情况答记者问.html
        xianggang_list.append(int(xianggang_list[yesterday_number]))
        taiwan_list.append(int(taiwan_list[yesterday_number]))
        aomen_list.append(int(aomen_list[yesterday_number]))

    time_specific= str(date_number) + '.' + date[0]
    time_city_dic[time_specific]=province_list
    print(str(date[0])+'日信息录入完毕！！！')

#创建表格
df=pd.DataFrame.from_dict(time_city_dic, orient='index')
df.to_excel('中国每日本土新增确诊人数（转置版）.xlsx')
df=df.T
df.to_excel('中国每日本土新增确诊人数.xlsx')
print("中国每日本土新增确诊人数已完成！！！")