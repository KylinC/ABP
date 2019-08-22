from data.infection.Proc_Funs import *

def infection(Affected_port, Affected_time = 23, Affected_cap = 33):
    read_file('data/infection/data/2019夏秋国内.txt')

    Cal_MaxHourTotalFlow()
    Cal_Degree()
    Sorted_Degree()

    Degree_Distr()
    Plt_InOutDegree()
    Plt_Degree_Degree()
    Degree_Cluster()

    result, information_dict = Alloc_Flights_Main(Affected_port, Affected_time, Affected_cap, 0)
    return result, information_dict

def simulator_infection():
    code = "ZBAA"
    test_result = infection(code)
    print(test_result)

if __name__ == '__main__':
    simulator_infection()