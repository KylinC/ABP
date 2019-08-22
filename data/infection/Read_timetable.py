import codecs
import os
import time


class PlanStruct:
    # 计划号
    PlanNo = ""

    # 航班号
    FlightNo = ""

    # 起飞机场
    DepAirport = ""

    # 降落机场
    ArrAirport = ""

    # 预计起飞时间
    EstDepTime = ""

    # 预计降落时间
    EstArrTime = ""


# 计划字典
PlanDict = {}

# 机场出现计数
global airport_dep_count, airport_arr_count
airport_dep_count = 0
airport_arr_count = 0

# 机场节点数据字典
global AirportNodes
AirportNodes = {}


# 更新机场节点数据
def update_airport_node(airport_code, is_dep, est_time):
    if airport_code in AirportNodes:
        airport_obj = AirportNodes.get(airport_code)

        # 总流量
        airport_obj['TotalFlow'] += 1

        # 起降流量
        if is_dep:
            airport_obj['DEP'] += 1
        else:
            airport_obj['ARR'] += 1

        time_obj = time.localtime(int(est_time))
        airport_obj['HourFlow'][time_obj.tm_hour] += 1
    else:
        airport_obj = {}

        # 总流量
        airport_obj['TotalFlow'] = 1

        # 起降流量
        if is_dep:
            airport_obj['DEP'] = 1
            airport_obj['ARR'] = 0
        else:
            airport_obj['DEP'] = 0
            airport_obj['ARR'] = 1

        # 每小时流量值
        hour_flow_obj = [0] * 24
        time_obj = time.localtime(int(est_time))
        hour_flow_obj[time_obj.tm_hour] += 1

        airport_obj['HourFlow'] = hour_flow_obj
        AirportNodes[airport_code] = airport_obj


# 创建一个航班对象
def create_flight_obj(dep_airport, dep_time, arr_airport, arr_time):
    flight_obj = {
        'DEP': dep_airport,
        'DEP_TIME': dep_time,
        'ARR': arr_airport,
        'ARR_TIME': arr_time
    }
    return flight_obj


# 创建一个小时流量统计对象
def create_hour_flow_obj():
    hour_flow_obj = {
        'HourTotalFlow': 1,
        'HourDep': 0,
        'HourDepFlights': [],
        'HourArr': 0,
        'HourArrFlights': []
    }

    return hour_flow_obj


# 更新一个机场节点的信息
def update_airport(airport, est_time, is_dep, flight_obj):
    if airport in AirportNodes:
        airport_obj = AirportNodes.get(airport)

        # 总流量
        airport_obj['TotalFlow'] += 1

        # 处理小时航班信息
        hours_obj = airport_obj['Hours']
        hour_flow_obj = hours_obj.get(str(int(est_time[0:2])))
        if hour_flow_obj.get('HourTotalFlow') != None:
            hour_flow_obj['HourTotalFlow'] += 1
        else:
            hour_flow_obj = create_hour_flow_obj()
            hours_obj[str(int(est_time[0:2]))] = hour_flow_obj

        if is_dep:
            airport_obj['DEP'] += 1
            hour_flow_obj['HourDep'] += 1
            hour_flow_obj['HourDepFlights'].append(flight_obj)
        else:
            airport_obj['ARR'] += 1
            hour_flow_obj['HourArr'] += 1
            hour_flow_obj['HourArrFlights'].append(flight_obj)
    else:
        airport_obj = {}
        AirportNodes[airport] = airport_obj

        # 总流量
        airport_obj['TotalFlow'] = 1

        # 每小时流量值
        hour_flow_obj = create_hour_flow_obj()

        airport_obj['Hours'] = {}

        index = 0
        hours_obj = airport_obj['Hours']
        while (index < 24):
            hours_obj[str(index)] = {}
            index += 1
        hours_obj[str(int(est_time[0:2]))] = hour_flow_obj

        if is_dep:
            airport_obj['DEP'] = 1
            airport_obj['ARR'] = 0
            hour_flow_obj['HourDep'] = 1
            hour_flow_obj['HourDepFlights'].append(flight_obj)
        else:
            airport_obj['DEP'] = 0
            airport_obj['ARR'] = 1
            hour_flow_obj['HourArr'] = 1
            hour_flow_obj['HourArrFlights'].append(flight_obj)

    return airport_obj


# 机场关联边数据字典
global AirportEdges
AirportEdges = {}


# 更新机场关联边数据
def update_airport_edge(dep_airport, arr_airport):
    edge_key = dep_airport + '->' + arr_airport
    if edge_key in AirportEdges:
        edge_obj = AirportEdges.get(edge_key)
        if edge_obj != 'N/A':
            edge_obj['NUM'] += 1
    else:
        # 新增机场节点关联边
        edge_obj = {
            'DEP': dep_airport,
            'ARR': arr_airport,
            'NUM': 1
        }
        AirportEdges[edge_key] = edge_obj


# 更新机场关联边数据,边的权重包括航班量和航线的飞行时长
def update_airport_edge(dep_airport, arr_airport, dep_time, arr_time):
    edge_key = dep_airport + '->' + arr_airport
    #计算此航班的航线飞行时间
    dep_hour = int(dep_time[0:2])
    dep_min  = int(dep_time[3:5])
    arr_hour = int(arr_time[0:2])
    arr_min  = int(arr_time[3:5])
    if dep_hour == 0:
        dep_hour = 24
    if arr_hour  == 0:
        arr_hour = 24
    flight_time = (arr_hour - dep_hour) * 60 + (arr_min - dep_min)
    if flight_time < 0:
        flight_time += 24*60

    if edge_key in AirportEdges:
        edge_obj = AirportEdges.get(edge_key)
        if edge_obj != 'N/A':
            edge_obj['NUM'] += 1
            edge_obj['Total_flight_time'] += flight_time
            edge_obj['flight_time'] = int(edge_obj['Total_flight_time']/edge_obj['NUM'])
    else:
        # 新增机场节点关联边
        edge_obj = {
            'DEP': dep_airport,
            'ARR': arr_airport,
            'NUM': 1,
            'Total_flight_time': flight_time,
            'flight_time': flight_time
        }
        AirportEdges[edge_key] = edge_obj





# 读取夏秋航班时刻表
def read_file(file_path):
      with open(file_path) as file_obj:
      #with open(file_path, encoding='utf-8') as file_obj:
        for line in file_obj:
            args = line.split(',')

            if len(args) < 20:
                continue

            # 星期
#            day = args[2]
#            if day.find('1') == -1:
#                continue

            # 起飞机场
            dep_airport = args[3]

            # 起飞时间
            dep_time = args[4]

            # 降落时间
            arr_time = args[5]

            # 降落机场
            arr_airport = args[6]

            # 过滤非国内机场
            if dep_airport[0] != 'Z' or arr_airport[0] != 'Z':
                continue

            # 新增一个航班对象
            flight_obj = create_flight_obj(dep_airport, dep_time, arr_airport, arr_time)

            # 更新起飞机场
            update_airport(dep_airport, dep_time, True, flight_obj)

            # 更新降落机场
            update_airport(arr_airport, arr_time, False, flight_obj)

            # 更新机场关联边数据
            #update_airport_edge(dep_airport, arr_airport)
            update_airport_edge(dep_airport, arr_airport, dep_time, arr_time)
