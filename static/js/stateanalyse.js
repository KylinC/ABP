function RelationGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_4'), 'chalk');
    var categories = [];
    categories[0] = {name: 'Massage'};
    categories[1] = {name: 'Elements'};

    graph.edges.forEach(function (edge) {
        edge.lineStyle = {
            width:2,
            color:"#FFFAFA"
        };
        edge.type = 'dashed';
    });
    console.log(graph.edges);
    var option = {
        title: {
            text: 'Flow Control',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right',
            textStyle : {
                color: '#fff'
            }
        },
        tooltip: {
            formatter: function(param){
                if(param.dataType === 'edge'){
                    return param.data.relationship;
                }
                else{
                    if(param.data.name != undefined){
                        return param.data.name;
                    }
                    else{
                        return param.data.title
                    }
                }    
                
            }
        },
        toolbox: {
            show : true,//是否显示工具箱
            feature : {
                magicType: ['line', 'bar'], // 图表类型切换，当前仅支持直角系下的折线图、柱状图转换，上图icon左数6/7，分别是切换折线图，切换柱形图
                restore: true, // 还原，复位原始图表，
                saveAsImage: true  // 保存为图片，
            }
        },
        legend: [{
            // selectedMode: 'single',
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        label: {//图形上的文本标签，可用于说明图形的一些数据信息
            normal: {
                show : true,//显示
                position: 'right',//相对于节点标签的位置，默认在节点中间
                //回调函数，你期望节点标签上显示什么
                formatter: function(params){
                    return params.data.label;
                },
            }
        },
        animation: true,
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.edges,
                categories: categories,
                roam: true,
                draggable: true,
                focusNodeAdjacency: true,
                label: {
                    normal: {
                        position: 'right',
                        formatter: function(params){
                            return params.data.name;
                        }
                    }
                },
                force: {
                    repulsion: 100
                }
            }
        ]
    };
    myChart.setOption(option);
}

function RouteGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_2'), 'chalk');
    var categories = [];
    categories[0] = {name: 'Pass'};
    categories[1] = {name: 'End_to'};
    categories[2] = {name: 'Start_from'};
    categories[3] = {name: 'Massage'};
    var option = {
        title: {
            text: 'Route Point Relation',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right',
            textStyle : {
                color: '#fff'
            }
        },
        tooltip: {
            formatter: function(param){
                if(param.dataType === 'edge'){
                    return param.data.relationship;
                }
                else{
                    if(param.data.name != undefined){
                        return param.data.name;
                    }
                    else{
                        return param.data.title
                    }
                }    
                
            }
        },
        toolbox: {
            show : true,//是否显示工具箱
            feature : {
                magicType: ['line', 'bar'], // 图表类型切换，当前仅支持直角系下的折线图、柱状图转换，上图icon左数6/7，分别是切换折线图，切换柱形图
                restore: true, // 还原，复位原始图表，
                saveAsImage: true  // 保存为图片，
            }
        },
        legend: [{
            // selectedMode: 'single',
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        label: {//图形上的文本标签，可用于说明图形的一些数据信息
            normal: {
                show : true,//显示
                position: 'right',//相对于节点标签的位置，默认在节点中间
                //回调函数，你期望节点标签上显示什么
                formatter: function(params){
                    return params.data.label;
                },
            }
        },
        animation: true,
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.edges,
                categories: categories,
                roam: true,
                draggable: true,
                focusNodeAdjacency: true,
                label: {
                    normal: {
                        position: 'right',
                        formatter: function(params){
                            return params.data.name;
                        }
                    }
                },
                force: {
                    repulsion: 100
                }
            }
        ]
    };
    myChart.setOption(option);
}

function StateAnalyse(){
    var tmp_text = $("#statetext").val()
    console.log(tmp_text)

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:5000/demo1/statelyse',
        data: JSON.stringify(tmp_text),
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
            RelationGraph(res[0]);
            RouteGraph(res[1]);
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}