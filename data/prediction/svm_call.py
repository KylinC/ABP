from sklearn import svm
from sklearn.externals import joblib
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://192.168.15.150:7687", auth=('neo4j', '123'))

def load_model():
    svm_model = joblib.load("data/prediction/svm_model.m")
    # c = svm_model.predict([[9, 101, 38, 31, 590]])
    return svm_model

def getFlightList(RouteNo):
    res_list = []
    RouteNo = "'" + RouteNo + "'"
    order = "match (w)-[r:PASS]->(a:RoutePoint {code:%s}) return w" % (RouteNo)
    with driver.session() as session:
        results = session.run(order).values()
        for item in results:
            res_list.append(item[0]._properties)
    for item in res_list:
        ave_time = item["AveFlyTime"]
        ave_time = float(ave_time)/(100.0*60)
        item.update({"AveFlyTime": ave_time})
        dep_time = item["DepTime"]
        dep_time_list = dep_time.split(":")
        dep_time = int(dep_time_list[0])*60+int(dep_time_list[1])
        item.update({"DepTime": dep_time})
    return res_list

def getControlInfo(RouteNo):
    RouteNo = "'" + RouteNo + "'"
    order = "match (w) -[r:FlowControlRoutePoint]->(a:RoutePoint {code:%s}) return a" % (RouteNo)
    with driver.session() as session:
        results = session.run(order).values()
        return len(results)

def getFlightInfo(FlightNO):
    match_FlightNO = "MATCH (n:FlightObject) WHERE n.name=~\"" + FlightNO + ".*\" RETURN n LIMIT 1"
    result_list = []
    with driver.session() as session:
        results = session.run(match_FlightNO).values()
        for result in results:
            result_list.append(result[0]._properties)
    return result_list[0]

def get_info(route_point):
    demo_list = []
    control_num = getControlInfo(route_point)
    flight_list = getFlightList(route_point)
    svm_model = load_model()

    for item in flight_list:
        flight_name = "'"+item["name"]+"'"

        order = "match (w:FlightObject{name:%s})-[r:DEPARTURE]->(a) return a.name" % (flight_name)
        with driver.session() as session:
            results = session.run(order).values()
        item.update({"Departure": results[0][0]})

        order = "match (w:FlightObject{name:%s})-[r:ARRIVAL]->(a) return a.name" % (flight_name)
        with driver.session() as session:
            results = session.run(order).values()
        item.update({"Arrival": results[0][0]})

    for item in flight_list:
        result = svm_model.predict([[0, item["AveFlyTime"], 0, control_num, item["DepTime"]]])
        if (result[0] > 0.9):
            demo_list.append([item["Departure"], item["Arrival"]])
    return demo_list

def test_this_file():
    example = getFlightInfo("CSN6228 ZUCK1045ZJSY180605")
    print(example)

if __name__ == '__main__':
    a = get_info("BEMAG")
    list_tmp = []
    list_tmp.append({1:1, 2:2})
    list_tmp.append([1, 2])
    print(list_tmp)
    print(a)