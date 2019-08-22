import os
import json
import math
import collections
from data.infection.Read_timetable import *
import numpy as np
#import matplotlib.pyplot as plt
import random
#from scipy import optimize

global AirportNodes_Sorted
AirportNodes_Sorted = []

# 确定机场节点小时流量最大值
def Cal_MaxHourTotalFlow():
    for key_node in AirportNodes:
        Max_HourTotalFlow = -1
        for hour_id in range(24):
            if AirportNodes[key_node]["Hours"][str(hour_id)] != {}:
                #HourTotalFlow = AirportNodes[key_node]["Hours"][str(hour_id)]["HourTotalFlow"]
                HourTotalFlow = AirportNodes[key_node]["Hours"][str(hour_id)]["HourArr"]
                if HourTotalFlow > Max_HourTotalFlow:
                    Max_HourTotalFlow = HourTotalFlow
        # print(key_node + "  " + "Max_HourTotalFlow" + "  " + str(Max_HourTotalFlow))
        AirportNodes[key_node]['Max_HourTotalFlow'] = Max_HourTotalFlow


# 计算机场节点的度数
def Cal_Degree():
    for key_node in AirportNodes:
        AirportNodes[key_node]['Connected'] = {}
        Connected_Node = []
        in_degree = 0
        out_degree = 0
        for key_edge in AirportEdges:
            if AirportEdges[key_edge]["ARR"] == key_node:
                in_degree += 1
                if AirportEdges[key_edge]["DEP"] not in Connected_Node:
                    Connected_Node.append(AirportEdges[key_edge]["DEP"])
            if AirportEdges[key_edge]["DEP"] == key_node:
                out_degree += 1
                if AirportEdges[key_edge]["ARR"] not in Connected_Node:
                    Connected_Node.append(AirportEdges[key_edge]["ARR"])
        AirportNodes[key_node]['in_degree'] = in_degree
        AirportNodes[key_node]['out_degree'] = out_degree
        AirportNodes[key_node]['max_degree'] = max(in_degree, out_degree)
        AirportNodes[key_node]['Connected'] = Connected_Node
        AirportNodes[key_node]['degree'] = len(AirportNodes[key_node]['Connected'])

# 分析机场节点的度分布
def Degree_Distr():
    node_num  = 0
    distriburtion = {}
    degree_arr = []
    for key_node in AirportNodes:
        node_num += 1
        degree_arr.append(AirportNodes[key_node]['degree'])

    for id in set(degree_arr):
        distriburtion[id] = degree_arr.count(id)
        distriburtion[id] = round(distriburtion[id]/node_num, 4)
    distriburtion = sorted(distriburtion.items(), key=lambda x:x[0], reverse=False) #以度数升序
    #print("度分布中 节点个数： " +  str(len(degree_arr)))
    #print(distriburtion)
    #区间统计
    # labels = []
    # fracs = []
    # num = 0
    # rate = 0
    # x = 0
    # for node in distriburtion:
    #     num += 1
    #     if node[0] > x*10 and node[0] <=(x+1)*10:
    #         rate += node[1]
    #     else:
    #         rate += node[1]
    #         x += 1
    #         labels.append(x*10)
    #         fracs.append(rate)
    #         rate = 0
    #  # 画图
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.plot(labels, fracs)
    # plt.xlabel("Node Degree k")
    # plt.ylabel("Rate N(k)/N")
    # plt.show()

# added by Jinglei 06/19/2019
#直线方程函数
def f_1(x, A, B):
    return A*x + B

def Plt_InOutDegree():
    labels = []
    fracs = []
    for key_node in AirportNodes:
        in_degree = AirportNodes[key_node]['in_degree']
        out_degree = AirportNodes[key_node]['out_degree']
        labels.append(in_degree)
        fracs.append(out_degree)

    #画图
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.scatter(labels, fracs)
    # plt.xlabel("In Degree")
    # plt.ylabel("Out Degree")
#    A1, B1 = optimize.curve_fit(f_1, labels, fracs)
#    x1 = np.arange(0, 6, 0.01)
#    y1 = A1*x1 + B1
#    plt.plot(x1, y1)
    
   # plt.show()

def Plt_Degree_Degree():
    labels = []
    fracs = []
    for key_node in AirportNodes:
        degree_node = AirportNodes[key_node]['degree']
        adj_degree  = 0
        adj_nodes = AirportNodes[key_node]['Connected']
        adj_num = len(adj_nodes)
        for nnode in adj_nodes:
            adj_degree += AirportNodes[nnode]['degree']
        average_degree = adj_degree//adj_num
        labels.append(degree_node)
        fracs.append(average_degree)
    #画图
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.scatter(labels, fracs)
    # plt.xlabel("Node Degree K")
    # plt.ylabel("Knn")
    # plt.show()

def Degree_Cluster():
    labels = []
    fracs = []
    for key_node in AirportNodes:
        if len(AirportNodes[key_node]["Connected"]) <= 1:
            continue
        node_coeff = Node_Coeff(key_node)
        degree = AirportNodes[key_node]['degree']
        labels.append(degree)
        fracs.append(node_coeff)
    #画图
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.scatter(labels, fracs)
    # plt.xlabel("Node Degree K")
    # plt.ylabel("C(k)")
    # plt.show()

def Sorted_Degree():
    # node_outputFile_obj = open('airport_node_sort.json', 'w')
    # 根据度数，降序排列
    AirportNodes_Sorted=sorted(AirportNodes.items(), key=lambda x:x[1]['degree'], reverse=True)
    # json.dump(AirportNodes_sort, node_outputFile_obj, indent=4)

def Average_Degree():
    average_degree = 0
    average_indegree = 0
    average_outdegree = 0
    node_num = 0
    for key_node in AirportNodes:
        node_num += 1
        average_degree += AirportNodes[key_node]['degree']
        average_indegree += AirportNodes[key_node]['in_degree']
        average_outdegree += AirportNodes[key_node]['out_degree']
    average_d = round(average_degree/node_num, 2)
    average_ind = round(average_indegree/node_num, 4)
    average_outd = round(average_outdegree / node_num, 4)

    return (average_d, average_ind, average_outd)

# 计算聚类系数，
def Node_Coeff(key_node):
    adj_node_num = len(AirportNodes[key_node]["Connected"])
    adj_edge_num  = 0
    for adj_node_1 in AirportNodes[key_node]["Connected"]:
        for adj_node_2 in AirportNodes[key_node]["Connected"]:
            adj_edge = adj_node_1 + '->' + adj_node_2
            if adj_edge in AirportEdges:
                adj_edge_num += 1
    return adj_edge_num/((adj_node_num-1)*adj_node_num)

def Cluster_Coeff():
    Total_Coeff = 0
    for key_node in AirportNodes:
        if len(AirportNodes[key_node]["Connected"]) <= 1:
            continue
        node_coeff = Node_Coeff(key_node)
        Total_Coeff += node_coeff
    Node_Num = len(AirportNodes)
    Network_Cluster_Coeff = round(Total_Coeff/Node_Num, 2)
    # print("Network_Cluster_Coeff: " + str(Network_Cluster_Coeff))
    return Network_Cluster_Coeff

# 计算任意两个节点之间最短路径的最大值
global Node_Distance
Node_Distance= {}
global Betweenness
Betweenness = {}

def Cal_Distance():
    #初始化
    for key_node in AirportNodes:
        Betweenness[key_node] = 0

    #机场节点之间距离的初始化
    for key_node_1 in AirportNodes:
        for key_node_2 in AirportNodes:
            key_edge = key_node_1 + '->' + key_node_2
            if key_edge in AirportEdges:
                Node_Distance[key_edge] = {
                    'distance': 1,
                    'source': key_node_1,
                    'sink': key_node_2
                }
            else:
                Node_Distance[key_edge] = {
                    'distance': 1000,
                    'source': key_node_1,
                    'sink': key_node_2
                }

    for key_node_1 in AirportNodes:
        for key_node_2 in AirportNodes:
            for k in AirportNodes:
                key_edge = key_node_1 + '->' + key_node_2
                key_edge1 = key_node_1 + '->' + k
                key_edge2 = k + '->' + key_node_2
                flag = 0
                if (Node_Distance[key_edge]['distance'] > Node_Distance[key_edge1]['distance'] + Node_Distance[key_edge2]['distance']) and (key_node_1 != key_node_2):
                    Node_Distance[key_edge]['distance'] = Node_Distance[key_edge1]['distance'] + Node_Distance[key_edge2]['distance']
                    temp_k = k
                    flag = 1
                if flag == 1:
                    Betweenness[temp_k] += 1
    # print(Node_Distance)
    # print(Betweenness)

def Cal_Average_Dis():
    Total_Dis  = 0
    Total_path  = 0
    Max_Dis  = -1
    for key in Node_Distance:
        if Node_Distance[key]['distance'] != 1000:
            Total_path += 1
            Total_Dis += Node_Distance[key]['distance']
            if Node_Distance[key]['distance'] > Max_Dis:
                Diameter = Node_Distance[key]
    average_dis = round(Total_Dis/Total_path, 2)
    print("Total Path num:" + str(Total_path) + "  Diameter:" + str(Diameter['distance']))
    return (average_dis, Diameter)

def Mix_Coeff():
    E = len(AirportEdges)
    print("EdgeNum: " + str(E))
    a = 0
    b = 0
    c = 0
    for key_edge in AirportEdges:
        source = AirportEdges[key_edge]["DEP"]
        sink = AirportEdges[key_edge]["ARR"]
        j = AirportNodes[source]["degree"]
        k = AirportNodes[sink]["degree"]
        a += j*k
        b += (j+k)/2
        c += (j*j+k*k)/2

    mixCoeff = (a/E - (b/E)*(b/E))/((c/E)-(b/E)*(b/E))
    # print("Mix Coeff:" + str(mixCoeff))
    return round(mixCoeff, 2)

# def Analysis_Degree():
#     max_degree = -1
#     min_degree = 9999
#     for key_node in AirportNodes:
#         key_node_obj = AirportNodes.get(key_node)
#         if key_node_obj.get('degree') != NULL:

# 计算机场节点Adj_node的节点指数
def Cal_Index_Node(Affected_time, process_node, Adj_node, AllocF):
    # 获取节点Adj_node的度数
    degree = AirportNodes[Adj_node]['degree']
    # 获取节点Adj_node的小时最大流量，即正常情况下的容量信息
    Max_HourTotalFlow = AirportNodes[Adj_node]['Max_HourTotalFlow'] #修改为到达航班量

    # 获取航线的飞行时间
    Connected_Edge = Adj_node + '->' + process_node
    if Connected_Edge in AirportEdges:
        FT = AirportEdges[Connected_Edge]["flight_time"]
    FT = round(FT / 60)
    # 读取顶点Adj_node 在第（Affected_time - flight_time +1）个时段的信息
    TimeInterval = Affected_time - FT + 1
    if TimeInterval <= 0:
        TimeInterval = 24 + TimeInterval
    #HourTotalFlow = AirportNodes[Adj_node]["Hours"][str(TimeInterval-1)]["HourTotalFlow"]
    HourTotalFlow_obj = AirportNodes[Adj_node]["Hours"].get(str(TimeInterval))
    if HourTotalFlow_obj == None or HourTotalFlow_obj == {}:
        HourTotalFlow = 0
    else:
        #HourTotalFlow = HourTotalFlow_obj.get("HourTotalFlow")
        HourTotalFlow = HourTotalFlow_obj.get("HourArr")#修改为到达航班量
    #print(HourTotalFlow)
    Redundancy = Max_HourTotalFlow - HourTotalFlow
    Index = (Redundancy+1)*degree
    # print("冗余度：" + str(Redundancy) + "  指数： " + str(Index))
    return Index


        
# 判断相邻的节点是否处于感染状态，SIS模型：分段函数
def Check_SIS(Alloc_Result, que, process_node,Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, res_list):
        for Adj_node in Index_Dict:
            # 获取节点Adj_node的小时最大流量，即正常情况下的容量信息
            Max_HourTotalFlow = AirportNodes[Adj_node]['Max_HourTotalFlow']

            # 获取航线的飞行时间
            Connected_Edge = Adj_node + '->' + process_node
            if Connected_Edge in AirportEdges:
                FT = AirportEdges[Connected_Edge]["flight_time"]
            FT = round(FT / 60)
            # 读取顶点Adj_node 在第（Affected_time - flight_time ）个时段的信息
            TimeInterval = AnalysTime - FT
            #TimeInterval = AnalysTime
            if TimeInterval <= 0:
                TimeInterval = 24 + TimeInterval

            if AirportNodes[Adj_node].get("Hours") != None:
                HourTotalFlow_obj = AirportNodes[Adj_node]["Hours"].get(str(TimeInterval))
                if HourTotalFlow_obj == None or HourTotalFlow_obj =={}:
                    HourTotalFlow = 0
                else:
                    #HourTotalFlow = HourTotalFlow_obj.get("HourTotalFlow")
                    HourTotalFlow = HourTotalFlow_obj.get("HourArr")#修改为起飞航班量
            #print ("AllocF: " + str(AllocF))
            if HourTotalFlow + Alloc_Result[Adj_node]  > Max_HourTotalFlow:
                que.append(Adj_node)
                # 记录传播影响的节点
                SusNode_obj = {
                    'MoreFlight': HourTotalFlow + Alloc_Result[Adj_node] - Max_HourTotalFlow,
                    'AllocFlight': Alloc_Result[Adj_node],
                    'SUSTime': TimeInterval,
                }
                # SUS_Node.append(SusNode_obj)
                SUS_Node[Adj_node] = SusNode_obj
                res_list.append([str(process_node), str(Adj_node)])

                # print ("===>感染的节点：" + str(Adj_node) + " 容量：" + str(Max_HourTotalFlow) + " 流量： " + str(HourTotalFlow) + " 分配负荷： " + str(Alloc_Result[Adj_node]))

#根据相邻节点的指数进行分配
def Index_Alloc(More_Flight, que, process_node, Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, Total_Index, res_list):
        Alloc_Result = {}
        adj_node_num = len(Adj_node_Dict)
        total_alloc = 0
        for key_adj_node in Adj_node_Dict:
            Index_AdjNode = Index_Dict[key_adj_node]
            rate = Index_AdjNode/Total_Index
            alloc_flight = rate*More_Flight
            alloc_flight = min(alloc_flight, Adj_node_flight[key_adj_node]["flight"])
            Alloc_Result[key_adj_node] = round(alloc_flight)
            total_alloc += round(alloc_flight)
        # print("相邻边数：" + str(Count_adj_edge))
        left_flight = More_Flight - total_alloc
        while left_flight > 0:
            sel = random.randint(0, adj_node_num-1)
            #print("产生的随机数： " + str(sel))
            sel_node = Adj_node_Dict[sel]
            old_alloc = Alloc_Result[sel_node]
            Alloc_Result[sel_node] = old_alloc+1
            left_flight -= 1
        
    
        # print("相邻节点分配结果：" + str(Alloc_Result))
        Check_SIS(Alloc_Result, que, process_node, Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, res_list)

#平均分配到相邻节点
def Mean_Alloc(More_Flight, que, process_node, Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, res_list):
        Alloc_Result = {}
        adj_node_num = len(Adj_node_Dict)
        mean = round(More_Flight/adj_node_num)
        #print("平均分配的平均值： " + str(mean))
        total_alloc = 0
        for key_adj_node in Adj_node_Dict:
            alloc_flight = min(mean, Adj_node_flight[key_adj_node]["flight"])
            Alloc_Result[key_adj_node] = round(alloc_flight)
            total_alloc += round(alloc_flight)
        # print("相邻边数：" + str(Count_adj_edge))
        left_flight = More_Flight - total_alloc
        #print("首次分配后剩余航班量： " + str(left_flight))
        while left_flight > 0:
            sel = random.randint(0, adj_node_num-1)
            #print("产生的随机数： " + str(sel))
            sel_node = Adj_node_Dict[sel]
            old_alloc = Alloc_Result[sel_node]
            Alloc_Result[sel_node] = old_alloc+1
            left_flight -= 1
        # print("相邻节点分配结果：" + str(Alloc_Result))
        Check_SIS(Alloc_Result, que, process_node, Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, res_list)

# 分配拥堵机场节点的航班流
def Alloc_Flights_Main(Affected_port, Affected_time, Affected_cap, Flag):

    res_list = []
    # 创建队列，并将第一个拥堵机场节点加入搜索队列，
    que = collections.deque()
    que.append(Affected_port)
    # print("QueLength: " + str(len(que)))
    # print (que)

    # 节点的信息字典
    information_dict = {}

    # 节点的感染状态
    SUS_Node = {}
    AnalysTime = Affected_time
    SusNode_obj = {
                    'MoreFlight': 0,
                    'AllocFlight': 0,
                    'SUSTime': AnalysTime
                  }
    SUS_Node[Affected_port] = SusNode_obj

    while que:
        # 队列不为空，读取队列中第一个节点
        process_node = que.popleft()
        AnalysTime = SUS_Node[process_node]["SUSTime"]
        AllocF = SUS_Node[process_node]["AllocFlight"]

       # 获取待处理节点process_node在受影响时间段内的流量信息（到达航班量）
        HourTotalFlights_obj = AirportNodes[process_node]["Hours"].get(str(AnalysTime))
        if HourTotalFlights_obj == {} or HourTotalFlights_obj == None:
            HourFlow_Analys = 0
        else:
            #HourFlow_Analys = HourTotalFlights_obj.get("HourTotalFlow")
            HourFlow_Analys = HourTotalFlights_obj.get("HourArr") #先修改为到达航班量
        
        # 获取待处理节点process_node的小时最大流量，即正常情况下的容量信息
        if process_node == Affected_port:
            cap = Affected_cap
        else:
            cap = AirportNodes[process_node]['Max_HourTotalFlow']

        # 计算待处理节点的超容量
        More_Flight = HourFlow_Analys + AllocF - cap

        SUS_Node[process_node]['MoreFlight'] = More_Flight

        information_dict[str(process_node)] = {}
        information_dict[str(process_node)].update({"capacity": str(cap)})
        information_dict[str(process_node)].update({"flow": str(HourFlow_Analys)})
        information_dict[str(process_node)].update({"distribution": str(AllocF)})
        information_dict[str(process_node)].update({"overleft": str(More_Flight)})
        # print("待处理机场：" + str(process_node) + "  容量：" + str(cap) + " 流量： " + str(HourFlow_Analys) + " 分配负荷： " + str(AllocF)+"  超量数：" + str(More_Flight))
        # print ("AnalysTime: " + str(AnalysTime))

        # 待处理节点的相邻节点指数的计算
        HourDep = 0
        HourArr = 0
        Count_adj_edge = 0
        Total_Index = 0
        Index_Dict = {}
        Adj_node_Dict = []
        
        Adj_node_flight = {}
                                             
        # 计算节点process_node的相邻节点（x -> process_node）                  
        for key_edge in AirportEdges:
            if AirportEdges[key_edge]["ARR"] == process_node:
                Count_adj_edge += 1

        # 计算节点process_node 的相邻节点, 但满足条件：在受影响的时段内有航班到达节点process_node
        HourArrFlights_obj = AirportNodes[process_node]["Hours"].get(str(AnalysTime))
        if HourArrFlights_obj != {}:
            HourArrFlights = HourArrFlights_obj.get("HourArrFlights")
            HourDep = HourArrFlights_obj.get("HourDep")
            HourArr = HourArrFlights_obj.get("HourArr")
            for HourArr_key in HourArrFlights:
                HourArr_node = HourArr_key["DEP"]
                if HourArr_node not in Adj_node_Dict:
                    Adj_node_Dict.append(HourArr_node)
        # print ("相邻节点集合：" +  str(Adj_node_Dict))

        assert Count_adj_edge >= len(Adj_node_Dict)


        for Adj_node in Adj_node_Dict:
            Index_AdjNode = Cal_Index_Node(Affected_time, process_node, Adj_node, AllocF)
            Index_Dict[Adj_node] = Index_AdjNode
            #print("相邻的节点：" + str(Adj_node) + " 指数： " + str(Index_AdjNode))
            Total_Index += Index_AdjNode

        for Adj_node in Adj_node_Dict:
            #字典初始化
            Adj_node_obj = {"flight": 0}
            Adj_node_flight[Adj_node] = Adj_node_obj
            
        HourArrFlights_obj = AirportNodes[process_node]["Hours"].get(str(AnalysTime))
        if HourArrFlights_obj != {}:
            HourArrFlights = HourArrFlights_obj.get("HourArrFlights")
            for HourArr_key in HourArrFlights:
                HourArr_node = HourArr_key["DEP"]
                Adj_node_flight[HourArr_node]["flight"] += 1
        # print(Adj_node_flight) #保存的是从相邻节点起飞的航班数
        
        if Flag == 1:
            # 按照节点指数的占比进行分配超容航班
            Index_Alloc(More_Flight, que, process_node, Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, Total_Index, res_list)
        else:
            # 平均分配到相邻节点
            Mean_Alloc(More_Flight, que, process_node, Adj_node_Dict, Index_Dict, Adj_node_flight, AnalysTime, SUS_Node, res_list)


    return res_list,information_dict