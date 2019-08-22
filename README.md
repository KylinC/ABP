# ATC-BigData-Platform 开发文档



>基于 python Flask + Jquery + Echarts 的前端可视化框架，支持点击事件，支持实时Neo4j数据交互。



## Content

[TOC]

## Developer

陈麒麟 (SJTU, k1017856853@icloud.com, https://github.com/KylinC)

王春晖 (SJTU, 554714511@qq.com, https://github.com/wangchunhala)



## DEpendencies

<img src='https://img.shields.io/badge/python-3.5.7-blue.svg'  align='left' style=' width:100px'/></br>

<img src='https://img.shields.io/badge/flask-1.1.1-brightgreen'  align='left' style=' width:100px'/></br>

<img src='https://img.shields.io/badge/neo4j-3.5.7-orange.svg'  align='left' style=' width:100px'/></br>

<img src='https://img.shields.io/badge/jquery-1.11.2-yellowgreen'  align='left' style=' width:100px'/></br>

<img src='https://img.shields.io/badge/jieba-0.39-blue'  align='left' style=' width:100px'/></br>



项目前端依赖 Python Flask 框架开发，依赖 Jquery 事件响应、Echarts页面渲染，后端依赖Python实时计算（如用Jieba做分词、用Sklearn构建支持向量机）或调用局域网内的Neo4j数据库。



## Launch

- 修改 **ATC-BigData-Platform/data/neo4j_database.py** 中的Neo4j数据库连接配置：

```python
from neo4j import GraphDatabase

def database(user = '用户名', pwd = '密码'):
    driver = GraphDatabase.driver("neobolt路径", auth=(user, pwd))
    return driver
```

其中用户名、密码为Python字符串， neobolt路径参见目标neo4jserver端命令行。

- 确保安装了相关依赖项，运行项目

```bash
cd ATC-BigData-Platform

python server.py
```



## View on Chrome



> 登陆界面

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-08-21-index1.jpg)



> Demo的选择界面

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-08-21-index2.jpg)



> 流控报文分析 (Demo1)

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-08-21-demo1.jpg)



> 气象报文分析 (Demo2)

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-08-21-demo2.jpg)



> 智能搜索

![](http://kylinhub.oss-cn-shanghai.aliyuncs.com/2019-08-21-demo3.jpg)





# File Structure

**ATC-BigData-Platform**

- **data**（该部分为后端，包含数据的实时计算、Neo4j库提取，后端API的所在位置）
- **extract_weather**（气象报文分析程序包）
    - addtoKG（气象报文分析API）
    - ...
  - **infection**（容量下降计算程序包）
    - KGInfect.py （容量下降程序API）
    - ...
  
- **prediction**（航班延误预测SVM程序包）
    - svm_call.py（SVM模型API）
    - ...
  - neo4j_database.py（Neo4j连接程序API）
  - ...
  
- **demo**

  - demo1.py（Flask子路由1）
  - demo2.py（Flask子路由2）
  - demo3.py（Flask子路由3）

- **static**

  - **css** (CSS格式文件)
  - **images** (CSS所需图片)
  - **img** (CSS所需图片)
  - **js** (JavaScript交互脚本及依赖第三方库)

- **templates**
- 404.html (防止进入不存在路由的异常捕获html)
  - demo1.html (Demo1-流控报文的默认界面)
  - demo2.html (Demo2-气象报文的默认界面)
  - demo3.html (Demo3-智能搜索的默认界面)
  - index.html (登陆界面-输入账号密码)
  - index1.html (Demo选择界面)
  
- serve.py（Flask根路由）



# Demo

> 对三个模块实现细节的介绍（按文件结构进行介绍，可直接用Ctrl+F进行目标函数搜索）



## 登陆界面

### sever.py

- index()

```python
@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')
```

定义了根路由的默认显示界面。

- not_found(Exception error)

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',result=404)
```

异常捕获，若不存在路由则跳转 404.html。

- py_login()

```python
@app.route('/py_login',methods=['GET','POST'])
def py_login():
    if request.method == 'GET':

        print(request.form)
        txtname = request.args.get('username')
        txtpswd = request.args.get('userpswd')

        if(txtname=="neo4j" and txtpswd=="123"):
            return "SUCCESS!"  # get可以到这里
            print(url_for('/index1'))
            # return redirect(url_for('/testhtm'))
        else:
            return "FAIL!"
```

登陆用户名密码比对，支持拓展(接入MongoDB、MySql等后端数据库进行比对)。

- f_infor()

```python
@app.route('/index1')
def f_infor():
    return render_template('index1.html')
```

登陆成功跳转，指定跳转界面 index1.html。

- 路由部署

```python
from demo import demo1
app.register_blueprint(demo1.mod1)
from demo import demo2
app.register_blueprint(demo2.mod2)
from demo import demo3
app.register_blueprint(demo3.mod3)
```

定义了 sever.py 与三个子路由的父子节点关系。

### templates/index.html

```html
<html>
<body>
    
    ......
    
<input type="text" name="username" id="username" placeholder="Account"/>
				 
<input type="password" name="password" id="password" placeholder="Password"/>

    ......

</body>

<script type="text/javascript">
    function Login() {
        var login = false;
        var  txtname = $("#username").val();
        var txtpsw = $("#password").val();

        $.ajax({
            url:"/py_login",
            data:{"username":txtname,"userpswd":txtpsw},
            type: 'GET',
            contentType: 'json',
            async: false,
            success: function (d) {
                alert(d)
                var status = d.status;
                if (d != "undefined" && d=="SUCCESS!")
                {
                     window.location.href="/index1";
                }

            }
        });
        return login;
    }
</script>

</html>
```

用Jquery提供的方法实现获取输入用户名、密码的功能。

### templates/index1.html

```html

      ......

                    <input type="button" name="register" value ="流控报文分析" onclick="window.location.href='/demo1'"/>

                      <input type="button" name="register" value ="气象报文分析" onclick="window.location.href='/demo2'"/>

                      <input type="button" name="register" value ="智能搜索" onclick="window.location.href='/demo3'"/>

      ......

```

用路由定义的三个demo的简单跳转。

## 流控报文分析（Demo1）

### data/prediction/svm_call.py

- get_info(string route_point)

```python
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
```

该函数获取结果RoutePoint的所有航班，利用SVM模型进行受影响判定。

对每一个航班，从Neo4j数据库获取SVM的五个输入特征。

- getFlightInfo(string FlightNO)

```python
def getFlightInfo(FlightNO):
    match_FlightNO = "MATCH (n:FlightObject) WHERE n.name=~\"" + FlightNO + ".*\" RETURN n LIMIT 1"
    result_list = []
    with driver.session() as session:
        results = session.run(match_FlightNO).values()
        for result in results:
            result_list.append(result[0]._properties)
    return result_list[0]
```

获取航班运行时间、离开时间两个SVM特征。

- load_model()

```python
def load_model():
    svm_model = joblib.load("data/prediction/svm_model.m")
    # c = svm_model.predict([[9, 101, 38, 31, 590]])
    return svm_model
```

获取已训练好的SVM模型。

- getFlightList(string RouteNo)

```python
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
```

获取经过RoutePoint的所有航班的列表。

- getControlInfo(string RouteNo)

```python
def getControlInfo(RouteNo):
    RouteNo = "'" + RouteNo + "'"
    order = "match (w) -[r:FlowControlRoutePoint]->(a:RoutePoint {code:%s}) return a" % (RouteNo)
    with driver.session() as session:
        results = session.run(order).values()
        return len(results)
```

获取生效的流控报文数量（与RoutePoint已建立关系的流控报文数量）。

### data/prediction/learning2.py

- save_model()

```python
def save_model():
	clf = SVMTrain()
	joblib.dump(clf,"svm_model.m")
```

将训练得到的svm模型保存在当前目录下，便于路由调用。

- SVMTrain()

```python
def SVMTrain():
	file_read_flow = open('analysis.csv')

	x_test = []
	y_test = []
	index1 = 0
	index2 = 0
	threshhold = 20
	for line in file_read_flow:
    ......
```

利用同目录下csv文件训练一个sklearn.svm模型并返回。

### data/prediction/svm_model.m

由 **data/prediction/learning2.py** 训练得到的SVM模型，每次验证均由当前目录下的 **data/prediction/svm_call.py** 调用。该模型不会自主更新，在更新训练集后需要手动运行**learning2.py** :

```bash
cd data/prediction

python learning2.py
```

### data/data_init.py

- buildNodes(neo4jnode_struct nodeRecord)

```python
def buildNodes(nodeRecord):
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15} #将集合元素变为list，然后取出值
        if(data['label'] == 'FlowControl'):
            data.update({'category': 1})
        else:
            data.update({'category': 0})
    else:
        data = {"id": nodeRecord._id}
    data.update(dict(nodeRecord._properties))
    if('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data
```

对单一的Neo4j Node数据体(eg: \<Node id=…, properties={...} \>)进行整理，成为字典格式，便于索引相关信息。并添加"category"标签，用于点的颜色渲染分类。添加"detail"标签，作为将鼠标置于点上的信息显示。

该函数仅用于对报文语义分解的Node处理，即Demo1右下角部分。

- buildNodesforroute(neo4jnode_struct nodeRecord)

```python
def buildNodesforroute(nodeRecord):
    if(len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15}
        data_property = dict(nodeRecord._properties)
        if(data['label'] == 'FlightObject'):
            data.update({'category': 0})
        elif(data['label'] == 'RoutePoint'):
            data.update({'category': 3})
        elif(data['label'] == 'RouteSegment'):
            data.update({'category': 1})
        else:
            data.update({'category': 2})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 20}
    data.update(dict(nodeRecord._properties))
    if ("bbox" in nodeRecord._properties.keys()):
        del nodeRecord._properties["bbox"]
    if('title' in data):
        data["name"] = data["title"]
    data["detail"] = str(nodeRecord._properties)
    return data
```

功能同函数 buildNodes(neo4jnode_struct nodeRecord)，可参见上文，对RoutePoint图的Node进行数据清洗。

该函数仅用于对报文RoutePoint关系图的Node处理，即Demo1正中部分。

### data/REdata.py

该部分即原 **Zhengze.py**,对报文进行解析操作，不做赘余解释。

### data/KGexpand.py

- KGgenerate(string aim_statement)

```python
def KGgenerate(aim_statement):
    driver = database()

    aim_dict = addFlowControlToKG(aim_statement)
    aim_dict_list = list(aim_dict.keys())

    with driver.session() as session:
        aim_embed_state="'"+aim_statement+"'"
        aim_embed_code="'"+aim_dict["限流点"]+"_"+aim_dict["发布时间"]+"'"
        aim_embed_routepoint="'"+aim_dict["限流点"]+"'"
        aim_embed_route="'"+aim_dict["航路"]+"'"
        state="merge (n:FlowControl{name:'FlowControl',code:%s,content:%s})"%(aim_embed_code,aim_embed_state)
        session.run(state)
        relation_state1="match (n:FlowControl{code:%s}),(m:RoutePoint{code:%s}) merge (n)-[r:FlowControlRoutePoint]->(m)"%(aim_embed_code,aim_embed_routepoint)
        relation_state2="match (n:FlowControl{code:%s}),(m:Route{code:%s}) merge (n)-[r:FlowControlRoute]->(m)"%(aim_embed_code,aim_embed_route)
        session.run(relation_state1)
        session.run(relation_state2)
        for relation in aim_dict_list:
            if(relation == "备注"):
                continue
            embed_state = aim_dict[relation]
            embed_state = "'"+embed_state+"'"
            state="match (n:FlowControl{content:%s}) merge (n)-[r:%s]->(b:Element{name:%s})"%(aim_embed_state,relation,embed_state)
            session.run(state)
    return aim_dict
```

根据 data/REdata.py 返回的报文分析字典，进行Neo4j数据的添加操作（如构建报文与航路点的关系等），并返回报文分析字典，便于路由端获取每次添加报文的信息。

### data/neo4j_database.py

- database(string user, string pwd)

```python
def database(user = 'neo4j', pwd = '123'):
    driver = GraphDatabase.driver("bolt://192.168.15.150:7687", auth=(user, pwd))
    return driver
```

连接Neo4j数据库，可以通过修改局域网址、用户名和密码连接不同的数据库。

tips：与py2neo不同的是，此处的局域网址为neobolt的地址，默认端口是7687（py2neo连接brouser，端口是7474）详细信息查看启动server版neo4j时的命令行返回信息。

### static/js/stateanalyse.js

- Graph1(jsonstruct graph)

```javascript
function Graph1(graph) {
    var myChart = echarts.init(document.getElementById('chart_3'));
  
    ......(echarts部分)
    
    myChart.setOption(option);
}
```

该函数用于渲染右上角的预测受影响航班路线，

该函数获取参数graph为一个json的数据体(通过python的json.dump得到)，

该数据体在python端的格式如下：

```python
json_struct= [
        [{'name': '北京'}, {'name': '上海'}],
        [{'name': '北京'}, {'name': '广州'}],
        [{'name': '北京'}, {'name': '大连'}],
        [{'name': '北京'}, {'name': '南宁'}],
        [{'name': '北京'}, {'name': '南昌'}]
    ];
```

每一个子列表内是一个OD（出发地、目的地）。

### demo/demo1.py 

- home1()

```python
@mod1.route("/demo1")
def home1():
    return render_template('demo1.html')
```

定义了demo1的默认界面。

- state_analyse()

```python
@mod1.route("/demo1/statelyse",methods = ['POST'])
def state_analyse():
    data = request.get_data()
    str_input = json.loads(data)
    
    ......
```

以Post方法获取报文信息，此路由的Js端位于 **static/js/stateanalyse.js**, 之后对报文进行处理，处理函数 KGgenerate(aim_statement) 位于 **data/KGexpand.py** 

> Ggenerate(aim_statement) 为项目zhengze.py的调用文件，旨在对解析对句子进行添Neo4j库的操作。

在完成添库操作之后，state_analyse()完成从Neo4j数据库取出RoutePoint、句子解析等信息显示在界面上。

对受影响的航路进行显示是调用 get_info(str_routepoint) 函数进行的，该 SVM 处理函数位于**data/prediction/svm_call.py**

> get_info(str_routepoint)调用了项目利用 Sklearn.svm 实现的支持向量机模型，训练文件为**data/prediction/learning2.py**，该训练文件不会由路由调用，需要手动运行。运行成功后会在同目录下产生 **svm_model.m** 模型文件，该文件才是 **get_info()** 的实际调用文件。

以上三个任务完成后，将数据打包成 result_list 列表，回传到 **stateanalyse.js** (见上文) 进行渲染任务。

- csv_approach()

```python
@mod1.route("/demo1/csvload",methods = ['POST'])
def csv_approach():
    data = request.get_data()
    data_input = json.loads(data)
    
     ......
```

以Post方式获取前端加载的csv报文列表(request得到的数据类型为Python list)，之后批量处理csv文件内的报文，单条报文处理方式同state_analyse()。

- graph_click()

```python
@mod1.route("/demo1/click",methods = ['POST'])
def graph_click():
    data = request.get_data()
    data_input = json.loads(data)
    
     ......
```

获取点击事件，将点击获得的点进行Neo4j匹配，将相关的点(存在Relation)加入渲染队列。

### templates/demo1.html

```html
<html>
<body>
##########################################
 最左部分功能选框的html文件，button通过Jquery的ajax方法在js中触发，底部引用了用到的Javascript脚本
##########################################
                          <input class="right_input" id='statetext' class="input" type="text" placeholder="请输入流控报文">
						   <button class="right_button" type="submit" onclick='StateAnalyse()'>Enter</button>
                           <input class="right_input" class="input" type="text" id="textfield" placeholder="请选择CSV文件">
                           <button class="right_button" type="submit" id="upload">Select</button>
						   <input class="input" type="file" id="csvfile" style="display: none;" name="csvfile" onchange="document.getElementById('textfield').value=this.files[0].name">
						   <input class="right_input" type="button" onclick="csv()" value="Upload">
						   <input class="right_input" id='neotext' class="input" type="text" placeholder="请输入Neo4j匹配语句">
						   <button class="right_button" type="submit" onclick='NeoSearch()'>Match</button>

##########################################
 三个显示框由id进行绑定，绑定方式由第三方库Echarts提供，在相关Javascript脚本中绑定，底部引用了用到的Javascript脚本
  tips：每个id框的id只运行一个函数进行id绑定
##########################################
    ......
  <div id="chart_2" style="width:100%;height:610px;"></div>
    ......
  <div id="chart_3" class="echart t_btn7" style="width:100%;height: 280px;"></div>
    ......
  <div id="chart_4" class="echart fl t_btn4" style="width:100%;height: 280px;cursor: pointer;"></div>

</body>
##########################################
  引用文件由注释self-defined function分割，以上为第三方库引用，以下为自定义Js脚本
##########################################
<script type="text/javascript" src="static/js/jquery-1.11.2.min.js"></script>
<script type="text/javascript" src="static/js/echarts.min.js"></script>
<script type="text/javascript" src="static/theme/macarons.js"></script>
<script type="text/javascript" src="static/js/china.js"></script>
<script type="text/javascript" src="static/js/jquery-1.11.2.min.js"></script>
<script type="text/javascript" src="static/js/papaparse.js"></script>
<script type="text/javascript" src="static/js/jschardet.js"></script>
<!-- self-defined function -->
<script type="text/javascript" src="static/js/csv2arr.js"></script>
<script type="text/javascript" src="static/js/stateanalyse.js"></script>
<script type="text/javascript" src='static/js/neosearch.js'></script>
</html>
```

定义了Demo1的Javascript资源和简单的button/input交互。



## 气象报文分析 （Demo2）

### data/extract_weather/addtoKG.py

```python
def addWeatherToKG(content, airport, Affected_time=23, Affected_cap=33):
    dic = work(content) #调用work()分析气象报文
    driver = database()
    
    ......
    
    edge_list, information_dict = infection(airport, Affected_time, Affected_cap) #调用infection进行容量下降分析
    
    ......
    
    esult_list.append({"nodes": nodes, "edges": edges, "infection": infectionnode})
    return result_list
```

该函数为气象报文主接口程序，负责调用work()函数进行气象报文解析、调用infection()函数进行容量下降分析

> 此处可以修改infection参数的值

之后该函数对解析的报文内容添加Neo4j数据库，并将需要显示的内容打包为python list格式进行返回。

### data/infection/KGInfect.py

- infection(Affected_port, Affected_time = 23, Affected_cap = 33)

```python
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

```

此函数为容量下降的主程序，函数中定义了默认参数的值，即Affected_time = 23, Affected_cap = 33。

### data/neo4j_database.py

- database(string user, string pwd)

```python
def database(user = 'neo4j', pwd = '123'):
    driver = GraphDatabase.driver("bolt://192.168.15.150:7687", auth=(user, pwd))
    return driver
```

连接Neo4j数据库，可以通过修改局域网址、用户名和密码连接不同的数据库。

tips：与py2neo不同的是，此处的局域网址为neobolt的地址，默认端口是7687（py2neo连接brouser，端口是7474）详细信息查看启动server版neo4j时的命令行返回信息。

### data/cypher_script.py

- infect_delete()

```python
def infect_delete():
    driver = database()
    neoorder1 = "MATCH (p{delete:'instant'}) return p"
    neoorder2 = "MATCH (p{delete:'instant'}) detach delete p"
    with driver.session() as session:
        while(session.run(neoorder1).values()):
            session.run(neoorder2)
```

删除之前添加的天气信息，由于之前添加的点都有 **delete:"instant"** 标签，故可以特征匹配，利用detach delete删除。

### data/data_init.py

- buildweathernodes(neo4jnode_struct nodeRecord)

```python
def buildweathernodes(nodeRecord):
    if (len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 15}
        if (data['label'] == 'Airport'):
            data.update({'category': 0})
            data.update({"symbolSize": 30})
        elif (data['label'] == 'CurrentWeatherInformation'or data['label'] == 'FutureWeatherInformation'):
            data.update({'category': 3})
            data.update({"symbolSize": 15})
        elif (data['label'] == 'CurrentWeatherType'or data['label'] == 'FutureWeatherType'):
            data.update({'category': 1})
            data.update({"symbolSize": 20})
        elif (data['label'] == 'CurrentWeather'or data['label'] == 'FutureWeather'):
            data.update({'category': 2})
            data.update({"symbolSize": 25})
        else:
            data.update({'category': 4})
            data.update({"symbolSize": 15})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 20}
    data.update(dict(nodeRecord._properties))
    if ('title' in data):
        data["name"] = data["title"]
    if("delete" in nodeRecord._properties.keys()):
        del nodeRecord._properties["delete"]
    if ("bbox" in nodeRecord._properties.keys()):
        del nodeRecord._properties["bbox"]
    data["detail"] = str(nodeRecord._properties)
    return data
```

功能同函数 buildNodes(neo4jnode_struct nodeRecord)，可参见上文，对图的Node进行数据清洗。

- buildweathernodes_test(neo4jnode_struct nodeRecord, dict cata)

```python
def buildweathernodes_test(nodeRecord, cata):
    if (len(nodeRecord._labels) != 0):
        data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0], "symbolSize": 20}
        if (data['label'] in cata.keys()):
            data.update({'category': cata[data['label']]})
        else:
            length = len(cata)
            cata.update({data['label']: length})
            data.update({'category': length})
    else:
        data = {"id": nodeRecord._id, "symbolSize": 15}
    data.update(dict(nodeRecord._properties))
    if ('title' in data):
        data["name"] = data["title"]
    if("delete" in nodeRecord._properties.keys()):
        del nodeRecord._properties["delete"]
    if ("bbox" in nodeRecord._properties.keys()):
        del nodeRecord._properties["bbox"]
    data["detail"] = str(nodeRecord._properties)
    return data, cata
```

功能同函数 buildNodes(neo4jnode_struct nodeRecord)，可参见上文，对图的Node进行数据清洗。

相比 buildNodes(neo4jnode_struct nodeRecord)，该函数提供了自动根据Node在Neo4j中label的值进行自动分类的功能。

### static/js/weatherlyse.js

- WeatherGraph(json_datastruct graph)

```javascript
function WeatherGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_2'),"macarons");
    
    ......
    
    if(length!=0){
        counter_flag = 0;
        setInterval(function() {
            if(counter_flag<length){
                tmp_nodes.push(tmp_list[counter_flag]);
                counter_flag++;
                myChart.setOption({
                series: [{
                    type: 'graph',
                    roam:true,
                    data:tmp_nodes,
                    links:graph.edges,
                }]
            });
            }
        },2500);  # 2500
    }

    if (option && typeof option == "object"){
        myChart.setOption(option);
    }
}
```

Javascript的画图程序，同Graph1(jsonstruct graph)，可参见上文。不同之处在于添加了扩散的时间延迟动画，可修改代码中注释2500的地方修改每次扩散的延迟时间。

- WeatherAnalyse()

```javascript
function WeatherAnalyse(){
    var tmp_state = $("#statetext").val();
    var tmp_code = $("#codetext").val();

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:5000/demo2/weatherlyse',
        data: JSON.stringify([tmp_state, tmp_code]),
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
            WeatherGraph(res[0]);
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}
```

将两个输入框的内容传递到路由demo2.py，其中tmp_state为气象报文字符串，tmp_code为机场地名(进行模糊匹配)。

- ClearAll()

```javascript
function ClearAll(){
    var tmp_state = $("#statetext").val();
    var tmp_code = $("#codetext").val();

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:5000/demo2/clearall',
        data: JSON.stringify([tmp_state, tmp_code]),
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
//            console.log(res);
//            DeleteGraph(res[0]);
            location.reload();
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}
```

传递信息给路由，删除所有带有 **delete:"instant"** 标签的节点及相关关系。

### demo/demo2.py

- home2()

```python
@mod2.route("/demo2")
def home2():
    return render_template('demo2.html')
```

定义了demo2的默认界面。

- weather_analyse()

```python
@mod2.route("/demo2/weatherlyse",methods = ['POST'])
def weather_analyse():
    data = request.get_data()
    str_input = json.loads(data)
    
    result_list = addWeatherToKG(str_input[0], str_input[1])
    ......
```

该函数获取通过Post方法构建路由，通过request获取前端的输入信息，调用分析函数addWeatherToKG()对气象报文进行分析、对机场地名进行模糊匹配、调用机场影响分析函数、添加Neo4j数据库。

> addWeatherToKG() 位于 **data/extract_weather/addtoKG.py** 内，其中自140行起调用机场影响分析函数infection()，位于 **data/infection/KGInfect.py** 内，在此处可以修改机场影响函数infection(string airport, int affected_time, int affected_cap)的默认参数以到达不同的感染效果。

之后，weather_analyse() 获取回调的点、边信息，传回至 **static/js/weatherlyse.js** 进行图形渲染。

### templates/demo2.html

```html
<html>
<body>
    ......
##################################
  通过id定义的图形框
##################################
    <div id="chart_2" style="width:100%;height:610px;"></div>
    ......
</body>
##################################
  引用文件由注释package we write分割，以上为第三方库引用，以下为自定义Js脚本
##################################
<script type="text/javascript" src="static/js/jquery-1.11.2.min.js"></script>
<script type="text/javascript" src="static/js/echarts.min.js"></script>
<script type="text/javascript" src="static/js/papaparse.js"></script>
<script type="text/javascript" src="static/theme/macarons.js"></script>
<script type="text/javascript" src="static/js/jschardet.js"></script>
<!--package we write-->
<script type="text/javascript" src="static/js/csv2arr.js"></script>
<script type="text/javascript" src="static/js/weatherlyse.js"></script>
</html>
```

定义了Demo2的Javascript资源和简单的button/input交互。



## 智能搜索 （Demo3）

大致流程：html里输入搜索内容传给javascript，javascript以post形式调用路由函数search(),在函数里查找了数据库拿到了点边数据，回传javascript，在javascript文件里以intellgraph1函数进行渲染。

### data/templates/demo3.html

```html
   <div class="data_main">
        <div class="main_left fl" >
             <div align="center">

                     <input class="right_input" id='sstext' class="input" type="text"                       placeholder="请输入搜索内容">
					<button class="right_button" type="submit"                                              onclick='Search()'>Enter</button>
                    <textarea disabled class="right_text" > &#10&#10输入格式如下:&#10具                      体名字 &#10&#10举例:&#10ZUUU
                    </textarea>
                 
        <div class="main_center2 fl">
              <div id="chart_2" style="width:100%;height:610px;"></div>
<script type="text/javascript" src="static/js/jquery-1.11.2.min.js"></script>
<script type="text/javascript" src="static/js/echarts.min.js"></script>
<script type="text/javascript" src="static/theme/echarts.min.j"></script>
<script type="text/javascript" src='static/js/Search.js'></script>
```

- **input** 

  搜索内容输入框  **placeholder**存放无输入时显示内容  输入内容传给字符串变量sstext

       其显示风格样式由 .right_input控制，width控制输入框宽度，height控制输入框高度，border-radius控制周边半径

- **button**  

  onclick='Search()' 点击按钮触发函数 Search()  

  函数Search()位于 static/js/Search.js 

  width控制输入框宽度，height控制输入框高度，border-radius控制周边半径。

- **textarea**  

  textarea>后为显示内容

- **id="chart_2"**

  echarts接口名字，其显示的内容由 static/js/Search.js 输出

- jquery-1.11.2.min.js，echarts.min.j，echarts.min.j均为第三方库的调用。

  


### data/demo/demo3.py

- click_node()

```python
@mod3.route("/demo3/click", methods=['POST'])
def click_node():
    data = request.get_data()
    data_input = json.loads(data)

    click_point_data = data_input[0]

    aim_name = "'" + click_point_data["name"] + "'"
    neoorder1 = 'MATCH (p1)-[r1]->(p2:%s{name:%s}) RETURN p1,p2,r1' % (click_point_data["label"], aim_name)
    neoorder2 = 'MATCH (p1:%s{name:%s})-[r1]->(p2) RETURN p1,p2,r1' % (click_point_data["label"], aim_name)

    nodeList = []
    edgeList = []
    with driver.session() as session:
        old_results = scatter_dict2["results"]
        results1 = session.run(neoorder1).values()
        results2 = session.run(neoorder2).values()
        results = results1 + results2 + old_results
        scatter_dict2.update({"results": results})
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList = list(set(nodeList))
            edgeList.append(result[2])
            edgeList = list(set(edgeList))

        tmp_nodeList = []
        tmp_nodeId = []
        tmp_edgeList = []
        tmp_edegId = []

        for item in nodeList:
            if item._id in tmp_nodeId:
                continue
            else:
                tmp_nodeList.append(item)
                tmp_nodeId.append(item._id)
        nodeList = tmp_nodeList

        for item in edgeList:
            if item._id in tmp_edegId:
                continue
            else:
                tmp_edgeList.append(item)
                tmp_edegId.append(item._id)
        edgeList = tmp_edgeList

        cata = {}
        nodes = []
        for node in nodeList:
            tmp_node, cata = buildweathernodes_test(node, cata)
            nodes.append(tmp_node)
        edges = []
        id_tmp = 0
        for edge in edgeList:
            data = {"id": id_tmp,
                    "source": str(edge.start_node._id),
                    "target": str(edge.end_node._id),
                    "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)

    json_data = json.dumps({"nodes": nodes, "edges": edges, "catas": list(cata.keys())})
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))
```

以json.loads(data)拿到输入点击点的所有信息，赋给 click_point_data，转化为neo4j语句链接neo4j数据库进行搜索，拿到的结果results共三类，前两类是点，最后一类是边。采用列表扩展append的方法获取点边数据。

因为点击之后新填了点，涉及到可能与之前已存在在nodelist，edgelist的重复。因此便利一遍id，如果之前已经存在id，则不再添加，之前没存在过添加。

最后的 for循环是对所有的边统一编号，这里主要是因为echarts要求边是连续的序号，而我们从neo4j数据库保存到本地时，其原来neo4j数据库赋值的id是不连续的随机的，因此我们将所有的点重新按序编号，以符合echarts的要求显示。

最后将nodes，edges，catas打包json数据回传到intellGraph1

- home3()


```python
@mod3.route("/demo3")
def home3():
    return render_template('demo3.html')
```

flask路由框架主函数链接demo3.html

- /demo3/Search Search()


```python
@mod3.route("/demo3/Search", methods=['POST'])
def Search():

    data = request.get_data()
    raworder = json.loads(data)

    seaorder ="match (a)-[r]->(w) where a.name=~'.*" +  raworder + ".*'return a,w,r"
    seaorder2 = "match (w)-[r]->(a) where a.name=~'.*"+  raworder + ".*' return a,w,r"
    
  ...
    with driver.session() as session:

        results = session.run(seaorder).values()

        nodeList = []
        edgeList = []
        if(len(results)!=0):
         for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            edgeList.append(result[2])
         results1 = session.run(seaorder2).values()
         for result1 in results1:
                nodeList.append(result1[1])
                edgeList.append(result1[2])
        else:
              results1 = session.run(seaorder2).values()
              for result1 in results1:
                  nodeList.append(result1[0])
                  nodeList.append(result1[1])
                  edgeList.append(result1[2])
                    
        for nodelist in nodeList:
            nodes.append(intellNodes(nodelist, cata)[0])
            
        edges = []
        id_tmp = 0
        for edge in edgeList:
            data = {"id": str(id_tmp),
                    "source": str(edge.start_node._id),
                    "target": str(edge.end_node._id),
                    "name": str(edge.type)}
            id_tmp += 1
            edges.append(data)
    json_data = json.dumps({"nodes": nodes, "edges": edges, "catas": cata})
    callback = request.args.get('callback')
    return Response('{}({})'.format(callback, json_data))
```

以json.loads(data)拿到输入内容，赋给raworder，转化为neo4j语句链接neo4j数据库进行搜索，拿到的结果results共三类，前两类是点，最后一类是边。采用列表扩展append的方法获取点边数据。

因为涉及到指向该点和该点指向的所有点的添加，为了避免重复采取的方法是，先搜索第一句，如果搜索到结果，该点，指向该点的所有点都添加过了，第二句话则不再添加该点，只添加该点指向的即可。如果第一句话没有结果，第二句话直接全部添加即可。

最后的 for循环是对所有的边统一编号，这里主要是因为echarts要求边是连续的序号，而我们从neo4j数据库保存到本地时，其原来neo4j数据库赋值的id是不连续的随机的，因此我们将所有的点重新按序编号，以符合echarts的要求显示。

最后将nodes，edges，catas打包json数据回传到intellGraph1

### data/static/js/Search.js

- intellGraph1(graph)


```javascript
function intellGraph1(graph) {
    var myChart = echarts.init(document.getElementById('chart_2'),'macarons');
    var categories = [];
    for(i=0;i<graph.catas.length;i++){
      categories[i]={name:graph.catas[i]}
    }
    
    ...
    
    myChart.setOption(option);
    myChart.on('click', function(params){
        if(params.dataType == 'node'){
            $.ajax({
                type: 'post',
                url: 'http://127.0.0.1:5000/demo3/click',
                data: JSON.stringify([params.data]),
                dataType: "jsonp",
                contentType: "application/json; charset=utf-8",
                success: function (res) {
                    intellGraph1(res);
                },
                error: function (msg) {
                    console.log(msg);
                }
            });
        }
        else{
            console.log(params);
        }
    })
}
```

输入为demo3/Search的输出结果传给参数graph

graph数据体分成三类分别为nodes，edges，catas。

取其catas实现分类显示。

> myChart.on('click', function(params)

> echarts里的点击扩散效果

> 将点击点的[params.data]以post形式回传给http://127.0.0.1:5000/demo3/click

> 经过其函数click_node()处理后输出结果Json数据回传，传给函数intellGraph1显示。

- Search()

``` javascript
function Search(){
    var tmp_text = $("#sstext").val();

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:5000/demo3/Search',
        data: JSON.stringify(tmp_text),
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
           intellGraph1(res);
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}
    
```

   输入搜索内容后点击button，调用Search()函数

   将输入框中的内容sstext调用赋值给tmp_text，以post形式回传给  http://127.0.0.1:5000/demo3/Search

   经过处理后输出结果Json数据回传，传给函数intellGraph1显示。







