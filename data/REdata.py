# -*- coding: utf-8 -*-
#from py2neo import *
import re

# 匹配限流航点
def retrieve_point(sstring):
    if '出' not in sstring and '全部方向' not in sstring:
        return 'null'
    if '出' in sstring:
        match_location = re.search('出', sstring).span()
        answer1 = ''
        begin = match_location[1]
        s = sstring[begin]
        while (s >= u'\u0041' and s <= u'\u005a') or (s >= u'\u0061' and s <= u'\u007a') or s.isdigit():
            begin = begin + 1
            answer1 = answer1 + s
            s = sstring[begin]
        return str(answer1)
    if '全部方向' in sstring:
        match_location = re.search('全部方向', sstring).span()
        answer2 = ''
        begin = match_location[0] - 1
        s = sstring[begin]
        while (s >= u'\u0041' and s <= u'\u005a') or (s >= u'\u0061' and s <= u'\u007a') or s.isdigit():
            begin = begin - 1
            answer2 = s + answer2
            s = sstring[begin]
        return str(answer2)


# 匹配航路
def retrieve_flight(sstring):
    if (re.search('航路', sstring) != None):
        match_location = re.search('航路', sstring).span()
    else:
        return 'null'
    answer = ''
    begin = match_location[0] - 1
    s = sstring[begin]
    while (s >= u'\u0041' and s <= u'\u005a') or (s >= u'\u0061' and s <= u'\u007a') or s.isdigit():
        begin = begin - 1
        answer = s + answer
        s = sstring[begin]
    return str(answer)


# 匹配距离间隔
def retrieve_min_distance(sstring):
    if (re.search('公里', sstring) != None):
        match_location = re.search('公里', sstring).span()
    else:
        return 'null'
    answer = ''
    begin = match_location[0] - 1
    s = sstring[begin]
    while s.isdigit():
        begin = begin - 1
        answer = s + answer
        s = sstring[begin]
    return str(answer)


def retrieve_min_time2(sstring):
    if '最小间隔' not in sstring:
        return 'null'
    match_location = re.search('最小间隔', sstring).span()
    answer = ''
    begin = match_location[1]
    s = sstring[begin]
    while s.isdigit():
        begin = begin + 1
        answer = answer + s
        s = sstring[begin]
    if s == '分':
        return answer
    else:
        return 'null'


# 匹配时间间隔
def retrieve_min_time(sstring):
    if (re.search('分钟一架', sstring) != None):
        match_location = re.search('分钟一架', sstring).span()
    else:
        return 'null'
    answer = ''
    begin = match_location[0] - 1
    s = sstring[begin]
    while s.isdigit():
        begin = begin - 1
        answer = s + answer
        s = sstring[begin]
    return str(answer)


# 匹配飞机总量
def retrieve_total_airplane(sstring):
    if (re.search('总量', sstring) != None):
        match_location = re.search('总量', sstring).span()
        answer1 = ''
        begin = match_location[1]
        s = sstring[begin]
        while s.isdigit():
            begin = begin + 1
            answer1 = answer1 + s
            s = sstring[begin]
        return str(answer1)

    if (re.search('60分钟', sstring) != None):
        match_location = re.search('60分钟', sstring).span()
        answer2 = ''
        begin = match_location[1]
        s = sstring[begin]
        while s.isdigit():
            begin = begin + 1
            answer2 = answer2 + s
            s = sstring[begin]
        return str(answer2)

    return 'null'


# 匹配落地点
def retrieve_land_location(sstring):
    if (re.search('落地', sstring) != None):
        match_location = re.search('落地', sstring).span()
        if '落地不受限' in sstring:
            i = match_location[0] - 1
            while i >= 0 and sstring[i] != ',':
                i = i - 1
            sstring1 = sstring[i + 1:match_location[0]]
            answer1 = sstring1.replace('、', ',')
            return answer1
        if '落地不受限' not in sstring:
            if '方向' in sstring:
                i = re.search('方向', sstring).span()
                if i[1] < match_location[0]:
                    sstring2 = sstring[i[1]:match_location[0]]
                    answer2 = sstring2
                    return answer2
            if '限' in sstring:
                i = re.search('限', sstring).span()
                if i[1] < match_location[0]:
                    sstring2 = sstring[i[1]:match_location[0]]
                    answer2 = sstring2
                    return answer2
            answer2 = sstring[:match_location[0]]
            return answer2
    return 'null'


def retrieve_departure_location(sstring):
    if '起飞申请' in sstring:
        return 'null'
    if '杭州0800前起飞不限' in sstring:
        return '杭州'
    if '大连起飞' in sstring:
        return '大连'
    if '乌鲁木齐起飞' in sstring:
        return '乌鲁木齐'

    if (re.search('起飞', sstring) != None):
        match_location = re.search('起飞', sstring).span()
        if '、' in sstring:
            i = match_location[0] - 1
            while i >= 0 and sstring[i] != '，':
                i = i - 1
            sstring1 = sstring[i + 1:match_location[0]]
            answer1 = sstring1.replace('、', ',')
            return answer1
        if '、' not in sstring:
            if '方向' in sstring:
                i = re.search('方向', sstring).span()
                if i[1] < match_location[0]:
                    sstring2 = sstring[i[1]:match_location[0]]
                    answer2 = sstring2
                    return answer2
                i = re.search('限', sstring).span()
                sstring2 = sstring[i[1]:match_location[0]]
                answer2 = sstring2
                return answer2

    return 'null'


# 匹配飞行高度
def retrieve_height(sstring):
    if 'S' not in sstring:
        return ['null', 'null']

    match_location = []
    for i in range(len(sstring)):
        if sstring[i] == 'S':
            match_location.append(i)
    answer1 = []
    for i in range(len(match_location)):
        answer1.append('')

    for i in range(len(match_location)):
        begin = match_location[i]
        s = sstring[begin + 1]

        while s.isdigit() and begin + 2 < len(sstring):
            begin = begin + 1
            answer1[i] = answer1[i] + s
            s = sstring[begin + 1]
    if ('禁用' in sstring):
        answer1.append('禁用')
    if ('含以下' in sstring):
        answer1.append('含以下')
    if ('含以上' in sstring):
        answer1.append('含以上')
    if '禁用' not in sstring and '含以下' not in sstring and '含以上' not in sstring:
        answer1.append('只用')
    a = ''
    if len(answer1) - 1 > 1:
        for i in range(len(answer1) - 2):
            if answer1[i] != '':
                a = a + answer1[i]
                a = a + ','

        a = a + answer1[len(answer1) - 2]
        return [a, answer1[len(answer1) - 1]]

    return answer1


def retrieve_area(sstring):
    if '区域' not in sstring:
        return 'null'
    match_location = []
    for i in range(len(sstring) - 1):
        if sstring[i] == '区' and sstring[i + 1] == '域':
            match_location.append(i)
    answer = []
    for i in range(len(match_location)):
        answer.append('')
    for i in range(len(match_location)):
        begin = match_location[i]
        s = sstring[begin - 1]
        while s >= u'\u4e00' and s <= u'\u9fa5' and s != '向' and s != '越':
            answer[i] = s + answer[i]
            begin = begin - 1
            s = sstring[begin - 1]
    string = ''
    for i in range(len(answer) - 1):
        string = string + answer[i]
        string = string + ','
    if (len(answer) > 1):
        string = string + answer[len(answer) - 1]
    return string


# 落地不受限
def retrieve_bool_land(sstring):
    if '落地不受限' in sstring:
        return 'true'
    else:
        return 'false'


# 起飞不限
def retrieve_bool_departure(sstring):
    if '起飞不限' in sstring:
        return 'true'
    else:
        return 'false'


# 高低合算
def retrieve_bool_both(sstring):
    if '高低合算' in sstring:
        return 'true'
    else:
        return 'false'


# 禁航
def retrieve_bool_forbid(sstring):
    if '禁航' in sstring:
        return 'true'
    else:
        return 'false'


def retrieve_nofar(sstring):
    if '不含以远' not in sstring:
        return 'null'
    match_location = re.search('不含以远', sstring).span()
    begin = match_location[0] - 1
    s = sstring[begin]
    answer = ''
    while s >= u'\u4e00' and s <= u'\u9fa5':
        answer = s + answer
        begin = begin - 1
        s = sstring[begin]
    return answer


def retrieve_beizhu(sstring):
    if '备注' not in sstring:
        return 'null'
    match_location = re.search('备注', sstring).span()
    begin = match_location[1] + 1
    end = len(sstring) - 1
    if end - begin > 5:
        return sstring[begin:end]
    return ''


def str2time(str):
    year = str[0:4]
    month = str[4:6]
    day = str[6:8]
    hour = str[8:10]
    min = str[10:12]
    timeresult = year + "-" + month + "-" + day + " " + hour + ":" + min
    # print(timeresult)
    return timeresult


def retrieve_flowcontrol(inputstr):
    command = []
    a = inputstr.split('",')
    for i in range(len(a)):
        a[i] = a[i].replace('"', '')
    command.append(a)
    command = command[0]
    # print(command[2])
    sstring = "限制上海方向南苑,天津落地出UDINO H104航路 30分钟一架"
    result = {}
    result["发出区域"] = command[0]
    result["接收区域"] = command[1]
    result["报文区域"] = retrieve_area(sstring)
    result["起飞点"] = retrieve_departure_location(sstring)
    result["落地点"] = retrieve_land_location(sstring)
    result["限流点"] = retrieve_point(sstring)
    result["航路"] = retrieve_flight(sstring)
    tmp = retrieve_height(sstring)
    result["流控高度"] = tmp[0]
    result["高度类型"] = tmp[1]
    result["发布时间"] = command[4]
    result["开始时间"] = command[5]
    result["结束时间"] = command[6]
    result["时间间隔"] = retrieve_min_time(sstring)
    result["距离间隔"] = retrieve_min_distance(sstring)
    result["最小总量"] = retrieve_total_airplane(sstring)
    result["最小时间间隔"] = retrieve_min_time2(sstring)
    result["流控原因"] = command[3]
    result["起飞不限"] = retrieve_bool_departure(sstring)
    result["落地不受限"] = retrieve_bool_land(sstring)
    result["高低合算"] = retrieve_bool_both(sstring)
    result["禁航"] = retrieve_bool_forbid(sstring)
    result["不含以远的地点"] = retrieve_nofar(sstring)
    result["备注"] = retrieve_beizhu(sstring)
    return result


def addFlowControlToKG(inputstr):
    # graph = Graph("http://192.168.15.150:7474/browser/", username="neo4j", password="123")
    result = retrieve_flowcontrol(inputstr)
    cypherstr = ""
    cypherdict = {}
    for key, value in result.items():
        cypherstr = cypherstr + key + ":\"" + value + "\","
    for key, value in result.items():
        cypherdict[key] = value
    FlowControl = "MERGE (n:FlowControl{code:\"" + result["限流点"] + "_" + result["发布时间"].replace(" ",
                                                                                                "") + "\"," + cypherstr[
                                                                                                              0:-1] + "})"
    FlowControlRoutePointRelationship = "MATCH (n:FlowControl{code:\"" + result["限流点"] + "_" + result["发布时间"].replace(
        " ", "") + "\"}), (m:RoutePoint{code:\"" + result[
                                            "限流点"] + "\"})" + " merge (n)-[r:FlowControlRelationship]->(m)"
    FlowControlRouteRelationship = "MATCH (n:FlowControl{code:\"" + result["限流点"] + "_" + result["发布时间"].replace(" ",
                                                                                                                 "") + "\"}), (m:Route{code:\"" + \
                                   result["航路"] + "\"})" + " merge (n)-[r:FlowControlRelationship]->(m)"
    #graph.run(FlowControl)
    #graph.run(FlowControlRoutePointRelationship)
    #graph.run(FlowControlRouteRelationship)
    return cypherdict


def file_test():
    # str2time("201810172200")
    inputstr = r'"北京区管","上海","限制上海方向南苑,天津落地出UDINO H104航路 30分钟一架","军事活动","201810171657 ","201810172000 ","201810172200 "'
    result = addFlowControlToKG(inputstr)
    print(result)


if __name__ == "__main__":
    file_test()

# print(result)
# #时间间隔，距离间隔，最小总量，最小时间间隔
# #流控原因，起飞不限，落地不受限，高低合算，禁航，不含以远的地点，备注
# result.append("1")
# result.append("d")

# file_read_flow = open('flowcontroltest.csv',encoding='gbk')
# command = []
# for line in file_read_flow:
#         a = str(line).split('",')
#         for i in range(len(a)):
#                 a[i]=a[i].replace('"','')
#         command.append(a)
# command=command[1:]
#
# #file_write_flow = open('analysistest.csv','w',encoding = 'gbk')
#
# result = []
# result1 = []
# #发出区域，接收区域，报文区域，起飞点，落地点，限流点，航路，流控高度，高度类型，发布时间，开始时间，结束时间
# #时间间隔，距离间隔，最小总量，最小时间间隔
# #流控原因，起飞不限，落地不受限，高低合算，禁航，不含以远的地点，备注
# for i in range (len(command)):
#         result.append([])
#         result1.append([])
#
# for i in range (len(command)):
#
#         sstring = command[i][2]
#         #发出区域：
#         result[i].append(command[i][0])
#         result1[i].append("发出区域;"+command[i][0])
#         #接收区域:
#         result[i].append(command[i][1])
#         result1[i].append("接收区域:"+command[i][1])
#         #报文区域:
#         result[i].append(retrieve_area(sstring))
#         result1[i].append("报文区域"+retrieve_area(sstring))
#         #起飞点:
#         result[i].append(retrieve_departure_location(sstring))
#         result1[i].append(retrieve_departure_location(sstring))
#         #落地点:
#         result[i].append(retrieve_land_location(sstring))
#         result1[i].append(retrieve_land_location(sstring))
#         #限流点:
#         result[i].append(retrieve_point(sstring))
#         result1[i].append(retrieve_point(sstring))
#         #航路:
#         result[i].append(retrieve_flight(sstring))
#         result1[i].append(retrieve_flight(sstring))
#         #流控高度，高度类型：
#         tmp = retrieve_height(sstring)
#         result[i].append(tmp[0])
#         result[i].append(tmp[1])
#         #发布时间，开始时间，结束时间
#         result[i].append(command[i][4])
#         result[i].append(command[i][5])
#         a = command[i][6].replace('\n','')
#         result[i].append(a)
#         #时间间隔
#         result[i].append(retrieve_min_time(sstring))
#         result1[i].append(retrieve_min_time(sstring))
#         #距离间隔
#         result[i].append(retrieve_min_distance(sstring))
#         result1[i].append(retrieve_min_distance(sstring))
#         #最小总量
#         result[i].append(retrieve_total_airplane(sstring))
#         result1[i].append(retrieve_total_airplane(sstring))
#         #最小时间间隔
#         result[i].append(retrieve_min_time2(sstring))
#         result1[i].append(retrieve_min_time2(sstring))
#         #流控原因：
#         result[i].append(command[i][3])
#
#         #起飞不限
#         result[i].append(retrieve_bool_departure(sstring))
#
#         #落地不受限
#         result[i].append(retrieve_bool_land(sstring))
#         #高低合算
#         result[i].append(retrieve_bool_both(sstring))
#         #禁航
#         result[i].append(retrieve_bool_forbid(sstring))
#         #不含以远的地点
#         result[i].append(retrieve_nofar(sstring))
#         #备注
#         result[i].append(retrieve_beizhu(sstring))
#
#
#
#
# index=5
# a = retrieve_height(command[index][2])
# print(a,command[index])
# print(result[index])
# print("发出区域 接收区域 报文区域 起飞点 落地点 限流点 航路 流控高度 高度类型 发布时间 开始时间 结束时间 时间间隔 距离间隔 最小总量 最小时间间隔 流控原因 起飞不限 落地不受限 高低合算 禁航 不含以远的地点 备注")


# CommandAnalyze("限制上海方向银川落地出FYG 20分钟一架(备注：转西安)")





