from typing import List
import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line
import re
import os
import pandas as pd

data = []
date_list = []
total_num = []
total1_num = []
time_list = []
minNum=0
maxNum=50
maxday = 0
minday = 0
date = ''
# 拿到每天的时间，生成提供下方使用的信息数据
def get_data():
    file_name = '中国每日本土新增确诊人数.xlsx'
    df = pd.read_excel(file_name)
    full_time_list = df.columns

    file_name = '中国每日本土新增确诊人数（转置版）.xlsx'
    df = pd.read_excel(file_name)
    province_list = list[df]
    i = 0

    # 遍历表格中的每一天，获取对应省份信息，并形成一定的格式
    for row in df.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据row来获取每一行指定的数据 并利用to_dict转成字典
        all_province_dic = df.loc[row, ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽',
                                        '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
                                        '四川', '贵州', '云南', '陕西', '甘肃', '青海', '北京', '天津',
                                        '上海', '重庆', '内蒙古', '广西', '西藏', '宁夏', '新疆']].to_dict()
        all_num_list = df.loc[row, ['中国大陆（无港澳台）']].to_list()
        # print(all_num_list)
        total_num.append(all_num_list[0])
        total1_num.append(int(all_num_list[0]))
        # test_data.append(all_province_dic)
        # print(all_province_dic)
        # print(all_num_list)
        data_list = []
        # 遍历一天的每一个城市
        for city in all_province_dic.keys():  # 获得
            each_city_dic = {}
            each_city_dic["name"] = city
            each_city_dic_value_list = []
            each_city_dic_value_list.append(all_province_dic[city])
            if (all_num_list[0] == 0):  # 被除数为0
                num = 0.00
            else:
                num = all_province_dic[city] / all_num_list[0]
            each_city_dic_value_list.append(num)
            each_city_dic_value_list.append(city)
            each_city_dic["value"] = each_city_dic_value_list
            data_list.append(each_city_dic)
            # print(each_city_dic)
        i += 1
        data_dic = {}
        data_dic["data"] = data_list
        data_dic["time"] = full_time_list[i].split('.')[1]
        data.append(data_dic)

    # 将得到的时间转化成list
    for num in full_time_list:
        if (num != "Unnamed: 0"):
            time_list.append(num.split('.')[1])
    return data

# 输入
def input_date():
    date = input("请输入查询月份（如2021-09）：")
    print("将会为您生成当月的可视化大屏数据!!!")
    print(date)

    # 形成数字与实践的对应关系
    path = r'D:\PycharmProjects\pachong\第一次作业\疫情详细信息'
    path_list = os.listdir(path)

    date_list.append('0')
    date_number = 0
    for file_list in path_list:
        date_number += 1
        ex = '(.*)\（.'
        date_needed = re.findall(ex, file_list)
        date_list.append(date_needed[0])
        # print(str(date_number)+' '+date_needed[0])

    # 画图 相关参数
    # print(date_list)
    num = -1
    global minday,maxday,minNum,maxNum
    minNum=0
    maxNum=50
    for i in date_list:
        num += 1
        if date in i:
            minday = num
            break
    num = len(date_list)
    for i in reversed(date_list):
        num -= 1
        if date in i:
            maxday = num
            break
    # print(str(minday)+' '+str(maxday))
    return date


# 获取基础表格，一天一张表格
def get_day_chart(day: str):
    # 获取到由data_mark生成的每日疫情总人数的list
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == day
    ][0]
    min_data, max_data = (minNum, maxNum)
    data_mark: List = []
    i = minday
    for x in time_list[minday:maxday]:
        if x == day:
            data_mark.append(total_num[i])
            # print(total_num[i],' ',str(i))
        else:
            data_mark.append("")
        i = i + 1
    # print(data_mark)
    # 生成地区图
    map_chart = (
        Map()
        .add(
            series_name="",
            data_pair=map_data,
            zoom=1,
            center=[119.5, 34.5],
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="" + str(day) + "中国每日本土新增确诊人数(单位:人） 数据来源：国家卫健委",
                subtitle="",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="30",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    # 绘制折线图
    line_chart = (

        Line()
        .add_xaxis(time_list[minday:maxday])
        .add_yaxis("", total1_num[minday:maxday])
        .add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="中国当月本土新增确诊人数(单位:人）", pos_left="72%", pos_top="5%"
            )
        )
    )
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
        .add_xaxis(xaxis_data=bar_x_data)
        .add_yaxis(
            series_name="",
            y_axis=bar_y_data,
            label_opts=opts.LabelOpts(
                # is_show=True, position="right", formatter="{b} : {c}"
                is_show=True, position="right%", formatter="{b} : {c}"
            ),
        )
        .reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="top",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    # 绘制饼图
    pie_data = [[x[0], x[1][0]] for x in map_data]
    pie = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["15%", "35%"],
            center=["80%", "82%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    # 绘制综合图
    grid_chart = (
        Grid()
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"

            ),
        )
        .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="10%", pos_bottom="50%"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        .add(map_chart, grid_opts=opts.GridOpts())
    )
    # print(map_data[0])

    # print(type(total_num[885]))
    return grid_chart


# if __name__ == "__main__":

def draw_new_infected():
    timeline = Timeline(
        init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
    )
    # print(time_list)
    data = get_data()  # Ok
    date = input_date()  # Ok
    print(date)
    # print(minday, maxday)
    # print(maxNum)
    for y in time_list[minday:maxday]:
        g = get_day_chart(day=y)
        timeline.add(g, time_point=str(y))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )
    timeline.render(date+"月份中国每日本土新增新确诊人数（可视化界面）.html ")
    print("已生成"+date+"月份中国每日本土新增确诊人数（可视化界面）.html！！")
    print(date+"月份动态可视化大屏生成成功,请点击查看！！!")


if __name__ == '__main__':
    draw_new_infected()
    #
    # print(data)
    # print(total_num)
    # print(total1_num)
    # print(time_list)
    # print(minday)
    # print(maxday)
    # print(minNum)
    # print(maxNum)
    # print(date)
