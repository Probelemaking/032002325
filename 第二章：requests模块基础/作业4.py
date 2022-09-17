import re
import os
import pandas as pd
import numpy as np
import openpyxl
#1. 统计中国大陆每日本土新增确诊人数及新增无症状感染人数，境外输入类型和疑似病例等无需统计。
#2. 统计所有省份包括港澳台每日本土新增确诊人数及新增无症状感染人数，境外输入类型和疑似病例等无需统计。
#3. 将统计的数据利用编程工具或开发包自动写入Excel表中。


path = r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'
path_list = os.listdir(path)
date_number=0
time_city_dic={}
for file_list in path_list:
    date_number+=1
    province_list = {'河北': 0, '山西': 0, '辽宁': 0, '吉林': 0, '黑龙江': 0, '江苏': 0, '浙江': 0, '安徽': 0,
                     '福建': 0,
                     '江西': 0, '山东': 0, '河南': 0, '湖北': 0, '湖南': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0,
                     '云南': 0,
                     '陕西': 0, '甘肃': 0, '青海': 0,  '内蒙古': 0, '广西': 0, '西藏': 0, '宁夏': 0,
                     '新疆': 0, '北京': 0,
                     '天津': 0, '上海': 0, '重庆': 0, '台湾': 0,'香港': 0, '澳门': 0, '兵团': 0, '中国大陆（无港澳台）': 0}
    ex = '(.*)\（.'
    date = re.findall(ex, file_list)
    path=r'C:\Users\86150\PycharmProjects\pachong\第二章：requests模块基础\疫情详细信息'+'\\'+file_list
    with open(path, "r", encoding='utf-8') as f:
        file = f.readlines()
    filecontent=''.join(file)
    if("无症状" in filecontent):
        ex="(新增无症状感染者.*)"
        str_test=re.findall(ex,filecontent)
        # print(str_test)
        # print(date)

        if(len(str_test)!=0):   #匹配目标段落
            ex = "新增无症状感染者(\d+)例" #匹配新增无症状感染者后的总人数
            all_infected_num_list=re.findall(ex,str_test[0])
            # if(len(all_infected_num_list)!=0):
                # print(all_infected_num_list)

            ex="新增无症状感染者\d+例[，]?(（.*?）)?"
            bracket_content=re.findall(ex,str_test[0])
            if(len(bracket_content)!=0 and bracket_content[0]!=''): #匹配括号
                # print(bracket_content)
                ex=".*?(\d+).+"
                input_num=re.findall(ex,bracket_content[0]) #匹配括号里是否有数字
                if(len(input_num)!=0):
                    # print(input_num)
                    province_list["中国大陆（无港澳台）"]=int(all_infected_num_list[0])-int(input_num[0])
                    print(str(date[0]) + '日无具体具体各省份信息！！！')
                # else:  #括号里如果没有数字代表全为境外输入


            else: #无括号
                ex = "本土(\d+)例"
                all_infected_num_list = re.findall(ex, str_test[0])
                # print(str_test[0])
                if(len(all_infected_num_list)!=0):
                    # print(all_infected_num_list)
                    province_list["中国大陆（无港澳台）"] = int(all_infected_num_list[0])
                    ex = "本土\d+例[，]?(（.*?）)?"       #匹配本土100例后的括号里的内容
                    every_province_list=re.findall(ex,str_test[0])
                    if(len(every_province_list)!=0and every_province_list[0]!=''):
                        # print(every_province_list)
                        jishu = 0
                        for city in province_list.keys():
                            # ----------------------------------
                            if (len(str_test) != 0):
                                if (city in str_test[0]):
                                    ex = city + '(\d*)例'
                                    num = re.findall(ex, str_test[0])
                                    if (len(num) != 0):  #正常找到多少例：如括号内的北京2例
                                        province_list[city] += int(num[0])

                                        jishu += int(num[0])
                                        # print(jishu)
                                    else:               # 本土病例x例（在山西）
                                        ex = '本土(\d.*?)例.*?'
                                        num = re.findall(ex, str_test[0])
                                        if (len(num) != 0):
                                            # -----------------------------------
                                            if (city == '河北' and "河北区" in str_test[0]):  # 2022-02-03 天津:河北区三例
                                                continue
                                            # --------------------------------------
                                            # print(city + "1111")
                                            province_list[city] += int(num[0])
                                            jishu += int(num[0])

                                        else:
                                            # print(city + "2222")
                                            province_list[city] += 1  # 2020-05-03 1例为本土病例（在山西）
                                            province_list["中国大陆（无港澳台）"] += 1
                        # if (len(all_infected_num_list[0]) != 0 and jishu != int(province_list["中国大陆（无港澳台）"])):
                        #     print("no!!!!!!!!!!!!!!!")
                        #     print(province_list["中国大陆（无港澳台）"])
                        #     print(jishu)
    time_specific = str(date_number) + '.' + date[0]
    time_city_dic[time_specific] = province_list
    print(str(date[0]) + '日信息录入完毕！！！')
df=pd.DataFrame.from_dict(time_city_dic, orient='index')
df.to_excel('中国每日本土新增无症状人数（转置版）.xlsx')
df=df.T
df.to_excel('中国每日本土新增无症状人数.xlsx')
print("中国每日本土新增无症状人数已完成！！！")


