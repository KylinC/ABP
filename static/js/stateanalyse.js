function RelationGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_4'),"macarons");
    var categories = [];
    console.log(graph.edges);
    categories[0] = {name: 'Elements'};
    categories[1] = {name: 'Massage'};

    graph.edges.forEach(function (edge) {
        edge.lineStyle = {
            width:2,
            color:"#FFFAFA"
        };
        edge.type = 'solid';
    });
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
                return param.data.detail;
            },
            textStyle:{
                fontSize:8
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
            textStyle:{color:'#fff'},
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
                        borderColor:"#fff",
                        fontSize: 5,
                        show:true,
                        formatter: function(params){
                            return params.data.name;
                        }
                    }
                },
                force: {
                    repulsion: 100,
                    length: 100,
                    layoutAnimation:false
                }
            }
        ]
    };
    myChart.setOption(option);
}

function RouteGraph(graph) {
    var myChart = echarts.init(document.getElementById('chart_2'),"macarons");
    var categories = [];
    categories[0] = {name: 'Pass'};
    categories[1] = {name: 'SegmentPoint'};
    categories[2] = {name: 'Massage'};
    categories[3] = {name: 'RoutePoint'}

    graph.edges.forEach(function (edge) {
        edge.lineStyle = {
            width:2,
            color:"#FFFAFA"
        };
        edge.type = 'dashed';
        edge.label={
            formatter:edge.name,
            position:'middle',
            show:true,
            fontSize:5
//            fontStyle:'italic'
        };
        edge.effect = {
            show:true,
            period:6,
            symbolSize: 3,
            color:"#fff",
            trailLength: 0.7
        };
    });

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
                        return param.data.detail;
                    }
                    else{
                        return param.data.detail;
                    }
                }    
                
            },
            position:"bottom",
            textStyle:{
                fontSize:10
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
            textStyle:{color:'#fff'},
            selected:{
                'Massage':false
            },
            data: categories.map(function (a) {
                return a.name;
            })
        }],
        animation: true,
        series : [
            {
                name: 'Les Miserables',
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.edges,
                categories: categories,
                edgeSymbol: ['','arrow'],
                edgeSymbolSize: [0,8],
                roam: true,
                draggable: true,
                focusNodeAdjacency: true,
                label: {
                    normal: {

                        show:true,

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
    var tmp_text = $("#statetext").val();

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

$("#upload").click(function(){
    $("#csvfile").click();
});

function csv(){
    $("input[name=csvfile]").csv2arr(function(arr){
        console.log( arr );
        //something to do here
        $.ajax({
            type: 'post',
            url: 'http://127.0.0.1:5000/demo1/csvload',
            data: JSON.stringify(arr),
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
    });
}