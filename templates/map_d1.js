function optionFactory(res,objS,objQ) {
    if(myChart){
        myChart.dispose();
    }
    var myChart = echarts.init(document.getElementById('chart_3'));

    var chinaGeoCoordMap = {
        0:[109.781327,39.608266],
        1:[114.31,30.52],
        2:[102.73,25.04],
        3:[106.54,29.59],
        4:[114.07,22.62],
        5:[121.48,31.22],
        6:[106.71,26.57],
        7:[116.46,39.92],
        8:[118.88,28.97],
        9:[116.7,39.53],
        10:[115.480656,35.23375],
        11:[101.718637,26.582347],
        12:[122.1,37.5],
        13:[117.93,40.97],
        14:[118.1,24.46],
        15:[110.479191,29.117096],
        16:[119.82,31.36],
        17:[109.12,21.49],
        18:[108.95,34.27],
        19:[125.35,43.88]
    };

    var chinaDatas = [
        [{
            name: '上海',
            value: 1
        }]
    ];

    var chinaName = {
        0:'鄂尔多斯',
        1:'武汉',
        2:'昆明',
        3:'重庆',
        4:'深圳',
        5:'上海',
        6:'贵阳',
        7:'北京',
        8:'衢州',
        9:'廊坊',
        10:'菏泽',
        11:'攀枝花',
        12:'威海',
        13:'承德',
        14:'厦门',
        15:'张家界',
        16:'宜兴',
        17:'北海',
        18:'西安',
        19:'长春'
    };

    var convertData = function(data) {
        var resdata = [];
        var length=0;
        for(var keyitem in data){
            length++;
        }
        for(var i = 0; i < length; i++) {
            var dataItem = data[i];
            var fromCoord = chinaGeoCoordMap[dataItem[0]];
            var toCoord = chinaGeoCoordMap[dataItem[1]];
            if(fromCoord && toCoord) {
                resdata.push([{
                    coord: fromCoord,
                    value: 0
                }, {
                    coord: toCoord,
                }]);
            }
        }
        return resdata;
    };

    var series = [];
    [res].forEach(function(item, i) {
        series.push({
                type: 'lines',
                zlevel: 2,
                effect: {
                    show: true,
                    period: 4, //箭头指向速度，值越小速度越快
                    trailLength: 0.02, //特效尾迹长度[0,1]值越大，尾迹越长重
                    symbol: 'arrow', //箭头图标
                    symbolSize: 5, //图标大小
                },
                lineStyle: {
                    normal: {
                        width: 1, //尾迹线条宽度
                        opacity: 1, //尾迹线条透明度
                        curveness: .1 //尾迹线条曲直度
                    }
                },
                data: convertData(item)
            }
        );
    });

    var set1 = new Set([]);
    for(var i = 0; i < 20; i++){
        // console.log(group);
        // console.log(offset);
        
        var list_length=0;
        for(var keyitem in res){
            list_length++;
        }

        for(var j=0; j < list_length; j++){
            if(i!=objQ && i!=objS && (i==res[j][0] || i==res[j][1])){
                set1.add(i);
            }
        }
        
        
        if(set1.has(i) && i!=objQ && i!=objS){
            series.push({
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 2,
                rippleEffect: { //涟漪特效
                    period: 4, //动画时间，值越小速度越快
                    brushType: 'stroke', //波纹绘制方式 stroke, fill
                    scale: 4 //波纹圆环最大限制，值越大波纹越大
                },
                label: {
                    normal: {
                        show: true,
                        position: 'right', //显示位置
                        offset: [5, 0], //偏移设置
                        formatter: chinaName[i],
                        fontSize: 13
                    },
                    emphasis: {
                        show: true
                    }
                },
                symbol: 'circle',
                symbolSize: function() {
                    return 5; //圆环大小
                },
                itemStyle: {
                    normal: {
                        show: false,
                        color: '#f00'
                    }
                },
                data: chinaDatas.map(function() {
                    return {
                        value: chinaGeoCoordMap[i].concat(0.3)
                    };
                }),
                
            });
        }
        else if(i==objS){
            series.push({
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 2,
                rippleEffect: { //涟漪特效
                    period: 4, //动画时间，值越小速度越快
                    brushType: 'stroke', //波纹绘制方式 stroke, fill
                    scale: 4 //波纹圆环最大限制，值越大波纹越大
                },
                label: {
                    normal: {
                        show: true,
                        position: 'right', //显示位置
                        offset: [5, 0], //偏移设置
                        formatter: chinaName[i],
                        fontSize: 13
                    },
                    emphasis: {
                        show: true
                    }
                },
                symbol: 'circle',
                symbolSize: function() {
                    return 5; //圆环大小
                },
                itemStyle: {
                    normal: {
                        show: false,
                        color: '#f00'
                    }
                },
                data: chinaDatas.map(function() {
                    return {
                        value: chinaGeoCoordMap[i].concat(0.8)
                    };
                }),
                
            });
        }
        else if(i==objQ){
            series.push({
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 2,
                rippleEffect: { //涟漪特效
                    period: 4, //动画时间，值越小速度越快
                    brushType: 'stroke', //波纹绘制方式 stroke, fill
                    scale: 4 //波纹圆环最大限制，值越大波纹越大
                },
                label: {
                    normal: {
                        show: true,
                        position: 'right', //显示位置
                        offset: [5, 0], //偏移设置
                        formatter: chinaName[i],
                        fontSize: 13
                    },
                    emphasis: {
                        show: true
                    }
                },
                symbol: 'circle',
                symbolSize: function() {
                    return 5; //圆环大小
                },
                itemStyle: {
                    normal: {
                        show: false,
                        color: '#f00'
                    }
                },
                data: chinaDatas.map(function() {
                    return {
                        value: chinaGeoCoordMap[i].concat(0.8)
                    };
                }),
                
            });
        }
        else{
            series.push({
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 2,
                rippleEffect: { //涟漪特效
                    period: 4, //动画时间，值越小速度越快
                    brushType: 'stroke', //波纹绘制方式 stroke, fill
                    scale: 4 //波纹圆环最大限制，值越大波纹越大
                },
                label: {
                    normal: {
                        show: true,
                        position: 'right', //显示位置
                        offset: [5, 0], //偏移设置
                        formatter: chinaName[i],
                        fontSize: 13
                    },
                    emphasis: {
                        show: true
                    }
                },
                symbol: 'circle',
                symbolSize: function() {
                    return 5; //圆环大小
                },
                itemStyle: {
                    normal: {
                        show: false,
                        color: '#f00'
                    }
                },
                data: chinaDatas.map(function() {
                    return {
                        value: chinaGeoCoordMap[i].concat(0)
                    };
                }),
                
            });
        }
    }

    option = {
        tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(166, 200, 76, 0.82)',
            borderColor: '#FFFFCC',
            showDelay: 0,
            hideDelay: 0,
            enterable: true,
            transitionDuration: 0,
            extraCssText: 'z-index:100',
            formatter: function(params, ticket, callback) {
                var res = "";
                var name = params.name;
                var value = params.value[params.seriesIndex + 1];
                res = "<span style='color:#fff;'>" + name + "</span><br/>数据：" + value;
                return res;
            }
        },
        backgroundColor:"#013954",
        visualMap: { //图例值控制
            min: 0,
            max: 1,
            calculable: true,
            show: true,
            color: ['#f44336', '#fc9700', '#ffde00', '#ffde00', '#00eaff'],
            textStyle: {
                color: '#fff'
            }
        },
        grid: {
            right: 15,
            top: 80,
            bottom: 30,
            width: '20%'
        },
        xAxis: {
            type: 'value',
            scale: true,
            position: 'top',
            splitNumber: 1,
            boundaryGap: false,
            splitLine: {
                show: false
            },
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                margin: 2,
                textStyle: {
                    color: '#aaa'
                }
            }
        },
        yAxis: {
            type: 'category',
            nameGap: 16,
            axisLine: {
                show: false,
                lineStyle: {
                    color: '#ddd'
                }
            },
            axisTick: {
                show: false,
                lineStyle: {
                    color: '#ddd'
                }
            },
            axisLabel: {
                interval: 0,
                textStyle: {
                    color: '#999'
                }
            },
            data: yData
        },
        geo: {
            map: 'china',
            zoom: 1.6,
            center: [115.98561551896913, 33.205000490896193],
            label: {
                emphasis: {
                    show: false
                }
            },
            roam: true, //是否允许缩放
            itemStyle: {
                normal: {
                    color: 'rgba(51, 69, 89, .5)', //地图背景色
                    borderColor: '#516a89', //省市边界线00fcff 516a89
                    borderWidth: 1
                },
                emphasis: {
                    color: 'rgba(37, 43, 61, .5)' //悬浮背景
                }
            }
        },
        series: series
        };

        myChart.setOption(option);

        var od_list=[];
        var clear_count=0;

        myChart.on('click', function (params) {
            if(params.componentSubType === 'effectScatter'){
                var item = params.componentIndex;
                var found = od_list.find(function(element) {return element == item;});
                if(found){
                    var aim_index=od_list.indexOf(item);
                    od_list.splice(aim_index,1);
                }
                else{
                    od_list.push(params.componentIndex);
                }  
            }
            console.log(od_list);
        })
}

$.ajax({
    type: 'get',
    url: 'http://127.0.0.1:5000/demo1/mapdata',
    dataType: "jsonp",  
    success: function (res) {
        console.log(res);
        relationshipGraph(res);
    },
    error: function (msg) {
        console.log(msg);
    }
});

