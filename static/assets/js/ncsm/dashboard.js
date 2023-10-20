var randomNo = function () {
    return Math.floor(Math.random() * 60) + 30
};
var handleRenderChartNCOMG = function () {
    // global apexchart settings
    Apex = {
        title: {
            style: {
                fontSize: "13px",
                fontWeight: "bold",
                fontFamily: app.font.family,
                color: app.color.white,
            },
        },
        legend: {
            fontFamily: app.font.family,
            labels: {
                colors: "#fff",
                show: true,
            },
        },
        tooltip: {
            style: {
                fontSize: "11px",
                fontFamily: app.font.family,
            },
        },
        grid: {
            borderColor: "rgba(" + app.color.whiteRgb + ", .25)",
        },
        dataLabels: {
            style: {
                fontSize: "12px",
                fontFamily: app.font.family,
                fontWeight: "bold",
                colors: undefined,
            },
        },
        xaxis: {
            axisBorder: {
                show: false,
                color: "rgba(" + app.color.whiteRgb + ", .25)",
                height: 1,
                width: "100%",
                offsetX: 0,
                offsetY: -1,
            },
            axisTicks: {
                show: false,
                borderType: "solid",
                color: "rgba(" + app.color.whiteRgb + ", .25)",
                height: 6,
                offsetX: 0,
                offsetY: 0,
            },
            labels: {
                style: {
                    colors: "#fff",
                    fontSize: "13px",
                    fontFamily: app.font.family,
                    fontWeight: 400,
                    cssClass: "apexcharts-xaxis-label",
                },
            },
        },
        yaxis: {
            labels: {
                style: {
                    colors: "#fff",
                    fontSize: "13px",
                    fontFamily: app.font.family,
                    fontWeight: 400,
                    cssClass: "apexcharts-xaxis-label",
                },
            },
        },
    };


//############################### 전체 자산 수 #######################################
    var assetAllChartInstance;
    function asset_all_chart(divId, notebook, desktop, other) {
        // 데이터 포인트의 총합을 계산
        const totalData1 = [
            notebook[0][0]['count'] + desktop[0][0]['count'] + other[0]['count']
        ];
        const totalData2 = [
            notebook[1][0]['count'] + desktop[1][0]['count'] + other[1]['count']
        ];

        document.getElementById('totalDataDiv').innerHTML = `Online : ${totalData1} &nbsp;&nbsp;&nbsp;&nbsp;Total : ${totalData2}`;

        var asset_all_chart_options = {
            series: [
                {
                    name: ['Desktop'],
                    data: [desktop[0][0]['count'], desktop[1][0]['count']]
                },
                {
                    name: ['Notebook'],
                    data: [notebook[0][0]['count'], notebook[1][0]['count']]
                },
                {
                    name: ['Other'],
                    data: [other[0]['count'], other[1]['count']]
                },
            ],
            chart: {
                type: 'bar',
                background: 'transparent',
                foreColor: 'rgba(255, 255, 255, 0.75)',
                height: 225,
                stacked: true,
                toolbar: {
                    show: false
                },
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'all_asset_detail1';
                        var dataPointIndex = config.dataPointIndex;
                        var seriesIndex = config.seriesIndex;
                        var selectedData = config.w.config.series[seriesIndex].data[dataPointIndex];
                        var categoryName = config.w.config.xaxis.categories[dataPointIndex];
                        var seriesName = config.w.config.series[seriesIndex].name;
                        document.getElementById('categoryName').value = categoryName;
                        document.getElementById('seriesName').value = seriesName;
                        document.getElementById('chartName').value = 'all_asset1';
                        $("#DashModal .modal-title").html(categoryName+' '+seriesName+' List');
                        all_asset_detail_list1(categoryName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                }
            },
            responsive: [{
                breakpoint: 480,
                options: {
                    legend: {
                        position: 'bottom',
                        offsetX: -10,
                        offsetY: 0
                    }
                }
            }],
            plotOptions: {
                bar: {
                    horizontal: true,
                },
            },
            grid: {
                borderColor: 'rgba(144, 164, 174, 0.5)'
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', 'rgba(0,0,0,0)'],
            xaxis: {
                categories: ['Online', 'Total'],
                labels: {
                    style: {
                        fontSize: '13px'
                    }
                },
            },

            dataLabels: {
                enabled: true,
                enabledOnSeries: [0, 1, 2],
                formatter: function (val, opt) {
                    let series = opt.w.config.series;
                    let idx = opt.dataPointIndex;
                    const total = series.reduce((total, self) => total + self.data[idx], 0);
                    return `${val}`;
                },
                style: {
                    fontSize: '13px',
                    colors: ["#fff"],
                }
            }
        };
        if (assetAllChartInstance) {
            assetAllChartInstance.destroy();
        }
        assetAllChartInstance = new ApexCharts(document.querySelector('#asset_all_chart'), asset_all_chart_options);
        assetAllChartInstance.render();
    }

    asset_all_notebook = dataList.asset_all_chart_list[0]
    asset_all_desktop = dataList.asset_all_chart_list[1]
    asset_all_other = dataList.asset_all_chart_list[2]

    asset_all_chart("asset_all_chart", asset_all_notebook, asset_all_desktop, asset_all_other);


//############################### 전체 자산 수(Online OS) #######################################
    function asset_all_os_chart1(divId, a, b, c) {
        // a, b, c 변수에서 각각의 카운트 값을 추출
        var countA = a.map(function (item) {
            return item.count;
        });

        var countB = b.map(function (item) {
            return item.count;
        });

        var countC = c.map(function (item) {
            return item.count;
        });

        var asset_all_os_chart_options1 = {
            series: [
                {
                    name: 'Desktop',
                    group: 'budget',
                    data: countA // a 변수의 카운트 값을 할당
                },
                {
                    name: 'Notebook',
                    group: 'budget',
                    data: countB // b 변수의 카운트 값을 할당
                },
                {
                    name: 'Other',
                    group: 'budget',
                    data: countC // c 변수의 카운트 값을 할당
                }
            ],
            //   chart: {
            //     type: 'bar',
            //     background: 'transparent',
            //     foreColor: 'rgba(255, 255, 255, 0.75)',
            //     height: 200,
            //       stacked: true,
            //     width: '100%',
            //     toolbar: {
            //         show: true,
            //         tools: {
            //             zoom: false,
            //             pan: false
            //         }
            //     }
            //   },
            //     plotOptions: {
            //   bar: {
            //     horizontal: true,
            //     // dataLabels: { position: 'top' }
            //   }
            // },
            //   stroke: {
            //     width: 3
            //   },
            //   grid: {
            //     borderColor: 'rgba(144, 164, 174, 0.5)'
            //   },
            chart: {
                type: 'bar',
                background: 'transparent',
                foreColor: 'rgba(255, 255, 255, 0.75)',
                height: 110,
                stacked: true,
                toolbar: {
                    show: false
                },
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'asset_os_detail1';
                        var dataPointIndex = config.dataPointIndex;
                        var seriesIndex = config.seriesIndex;
                        var selectedData = config.w.config.series[seriesIndex].data[dataPointIndex];
                        var categoryName = config.w.config.xaxis.categories[dataPointIndex];
                        var seriesName = config.w.config.series[seriesIndex].name;
                        document.getElementById('categoryName').value = categoryName;
                        document.getElementById('seriesName').value = seriesName;
                        document.getElementById('chartName').value = 'asset_os_detail1';
                        $("#DashModal .modal-title").html(categoryName+' '+seriesName+' List');
                        asset_os_detail_list1(categoryName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            responsive: [{
                breakpoint: 480,
                options: {
                    legend: {
                        position: 'top',
                        offsetX: -10,
                        offsetY: 0
                    }
                }
            }],
            plotOptions: {
                bar: {
                    horizontal: true,
                },
            },
            grid: {
                borderColor: 'rgba(144, 164, 174, 0.5)'
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', 'rgba(0,0,0,0)'],

            dataLabels: {
                enabled: true,
                style: {
                    fontSize: '9px',
                    colors: ["#fff"],
                }
            },
            xaxis: {
                type: 'category',
                categories: ['Other', 'Mac', 'Windows'],
                labels: {
                    show: false,
                    style: {
                        fontSize: "8px",
                    },
                },
            },
            yaxis: {
                labels: {
                    fontSize: "8px",
                },
            },
            legend: {
                fontSize: '10px',
                markers: {
                    fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A',]
                },
                itemMargin: {
                    horizontal: 20
                },
                labels: {
                    colors: 'rgba(255, 255, 255, 0.75)',
                },
                position: 'top'
            }
        };
        var asset_all_os_chart1 = new ApexCharts(document.querySelector('#asset_all_os_chart1'), asset_all_os_chart_options1);
        asset_all_os_chart1.render();
    }

    desk_online_list = dataList.desk_online_list
    note_online_list = dataList.note_online_list
    other_online_list = dataList.other_online_list

    asset_all_os_chart1("asset_all_os_chart", desk_online_list, note_online_list, other_online_list);



//#######################################전체 자산 수(Total OS)#################################
    function asset_all_os_chart2(divId, a, b, c) {
        // a, b, c 변수에서 각각의 카운트 값을 추출
        var countA = a.map(function (item) {
            return item.count;
        });

        var countB = b.map(function (item) {
            return item.count;
        });

        var countC = c.map(function (item) {
            return item.count;
        });

        var asset_all_os_chart_options2 = {
            series: [
                {
                    name: 'Desktop',
                    group: 'budget',
                    data: countA // a 변수의 카운트 값을 할당
                },
                {
                    name: 'Notebook',
                    group: 'budget',
                    data: countB // b 변수의 카운트 값을 할당
                },
                {
                    name: 'Other',
                    group: 'budget',
                    data: countC // c 변수의 카운트 값을 할당
                }
            ],
            chart: {
                type: 'bar',
                background: 'transparent',
                foreColor: 'rgba(255, 255, 255, 0.75)',
                height: 112,
                stacked: true,
                toolbar: {
                    show: false
                },
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'asset_os_detail2';
                        var dataPointIndex = config.dataPointIndex;
                        var seriesIndex = config.seriesIndex;
                        var selectedData = config.w.config.series[seriesIndex].data[dataPointIndex];
                        var categoryName = config.w.config.xaxis.categories[dataPointIndex];
                        var seriesName = config.w.config.series[seriesIndex].name;
                        document.getElementById('categoryName').value = categoryName;
                        document.getElementById('seriesName').value = seriesName;
                        document.getElementById('chartName').value = 'asset_os_detail2';
                        $("#DashModal .modal-title").html(categoryName+' '+seriesName+' List');
                        asset_os_detail_list2(categoryName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            responsive: [{
                breakpoint: 480,
                options: {
                    legend: {
                        position: 'bottom',
                        offsetX: -10,
                        offsetY: 0
                    }
                }
            }],
            plotOptions: {
                bar: {
                    horizontal: true,
                },
            },
            grid: {
                borderColor: 'rgba(144, 164, 174, 0.5)'
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', 'rgba(0,0,0,0)'],
            dataLabels: {
                enabled: true,
                style: {
                    fontSize: '9px',
                    colors: ["#fff"],
                }
            },
            xaxis: {
                type: 'category',
                categories: ['Other', 'Mac', 'Windows',],
                labels: {
                    show: false,
                    style: {
                        fontSize: "8px",
                    },
                },
            },
            yaxis: {
                labels: {
                    fontSize: "8px",
                }
            },

            legend: {
                fontSize: '8px',
                markers: {
                    fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A',]
                },
                itemMargin: {
                    horizontal: 20
                },
                labels: {
                    colors: 'rgba(255, 255, 255, 0.75)',
                },
                position: 'bottom'
            }
        };
        var asset_all_os_chart2 = new ApexCharts(document.querySelector('#asset_all_os_chart2'), asset_all_os_chart_options2);
        asset_all_os_chart2.render();
    }

    desk_total_list = dataList.desk_total_list
    note_total_list = dataList.note_total_list
    other_total_list = dataList.other_total_list

    asset_all_os_chart2("asset_all_os_chart2", desk_total_list, note_total_list, other_total_list);


    //--------------------------------------------------------------------------
    // 자산 관리 현황 미니도넛, 프로그레스 바 - DISK 사용률 초과 서버, MEMORY 사용률 초과 서버
    //--------------------------------------------------------------------------

    // var disk_widthPercentage = (dataList.disk_donutData / dataList.allOnline_donutData) * 100;
    // document.querySelector("#disk-bar").style.width = disk_widthPercentage + "%";
    // var mem_widthPercentage = (dataList.memory_donutData / dataList.allOnline_donutData) * 100;
    // document.querySelector("#mem-bar").style.width = mem_widthPercentage + "%";
    // var cpu_widthPercentage = (dataList.cpu_donutData / dataList.allOnline_donutData) * 100;
    // document.querySelector("#cpu-bar").style.width = cpu_widthPercentage + "%";
    // var om_disk_chartOptions = {
    //     series: [20, 20, 20, 20, 20],
    //     chart: {
    //         width: 100,
    //         height: 100,
    //         type: 'donut',
    //         toolbar: {
    //             show: false
    //         }
    //     },
    //     colors: ['rgba(223, 224, 223, .2)', 'rgba(223, 224, 223, .4)', 'rgba(223, 224, 223, .5)', 'rgba(223, 224, 223, .8)', 'rgba(223, 224, 223, 1)'],
    //     plotOptions: {
    //         pie: {
    //             donut: {
    //                 labels: {
    //                     show: false
    //                 }
    //             }
    //         }
    //     },
    //     dataLabels: {
    //         enabled: false
    //     },
    //     legend: {
    //         show: false
    //     },
    //     stroke: {
    //         show: false
    //     },
    //     tooltip: {
    //         enabled: false
    //     }
    // };
    // var chartContainers = document.querySelectorAll('.om_disk_chart');
    // chartContainers.forEach(function (container) {
    //     var chart = new ApexCharts(container, om_disk_chartOptions);
    //     chart.render();
    // });

    //--------------------------------------------------------------------------
    // windows 버전별 자산목록 - windowAsset_pie 차트
    //--------------------------------------------------------------------------
     function oslistPieChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'pie',
                width: '100%',
                height: 200,
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'oslistPieChart';
                        var dataPointIndex = config.dataPointIndex;
                        var labelsName = config.w.config.labels[dataPointIndex];
                        document.getElementById('categoryName').value = labelsName;
                        document.getElementById('chartName').value = 'oslistPieChart';
                        $("#DashModal .modal-title").html(labelsName+' List');
                        oslistPieChart_list(labelsName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858', '#4B778D'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
                    fontSize: '13px',
                    fontWeight: '300'
                },
                formatter(val, opts) {
                    const name = opts.w.globals.labels[opts.seriesIndex];
                    return [val.toFixed(1) + '%'];
                }
            },
            stroke: {
                width: 0
            },
            fill: {
                type: 'gradient'
            },
            legend: {
                show: false
            }
        };
        var os_list_pie_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        os_list_pie_chart.render();
    }

    // createDonutChart("os_donut", os_pieDataCount, os_pieDataItem);
    oslistPieChart("windowAsset_pie", dataList.os_asset_data_count_list[0], dataList.os_asset_data_count_list[1]);


    //--------------------------------------------------------------------------
    // os 설치 현황, 유/무선 연결 현황, 물리/가상 자산 현황
    //--------------------------------------------------------------------------
    // var os_pieDataItem = []
    // var os_pieDataCount = []
    // for (var i = 0; i < dataList.os_pieData.length; i++) {
    //     os_pieDataItem.push(dataList.os_pieData[i]['item']);
    //     os_pieDataCount.push(dataList.os_pieData[i]['count']);
    // };
    //
    // var wire_pieDataItem = []
    // var wire_pieDataCount = []
    // for (var i = 0; i < dataList.wire_pieData.length; i++) {
    //     wire_pieDataItem.push(dataList.wire_pieData[i]['item']);
    //     wire_pieDataCount.push(dataList.wire_pieData[i]['count']);
    // };
    //
    // var virtual_pieDataItem = []
    // var virtual_pieDataCount = []
    // for (var i = 0; i < dataList.virtual_pieData.length; i++) {
    //     virtual_pieDataItem.push(dataList.virtual_pieData[i]['item']);
    //     virtual_pieDataCount.push(dataList.virtual_pieData[i]['count']);
    // };

    function osVerPieChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'pie',
                width: '100%',
                height: 240,
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#osVerPieChart').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'osVerPieChart';
                        var dataPointIndex = config.dataPointIndex;
                        var labelsName = config.w.config.labels[dataPointIndex];
                        document.getElementById('categoryName').value = labelsName;
                        document.getElementById('chartName').value = 'osVerPieChart';
                        $("#DashModal .modal-title").html(labelsName+' List');
                        osVerPieChart_list(labelsName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
                    fontSize: '13px',
                    fontWeight: '300'
                },
                formatter(val, opts) {
                    const name = opts.w.globals.labels[opts.seriesIndex];
                    return [name + ' ' + val.toFixed(1) + '%'];
                }
            },
            stroke: {
                width: 0
            },
            fill: {
                type: 'gradient'
            },
            legend: {
                position: 'bottom',
                formatter: function (val, opts) {
                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
                    return val;
                }
            }
        };
        if (seriesData.length === 0) {
            donutOptions.legend.show = false;
        }
        var os_pie_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        os_pie_chart.render();
    }

    // createDonutChart("os_donut", os_pieDataCount, os_pieDataItem);
    osVerPieChart("os_pie", dataList.os_up_data_list, ['업데이트 완료', '업데이트 필요']);


//##################################장기 접속/미접속 차트 #################################################
    //console.log(dataList.discover_data_list[0])
    //alert(dataList.discover_data_list.0)
//
//    function createDonutChart(divId, seriesData, labelsData) {
//        var donutOptions = {
//            series: seriesData,
//            chart: {
//                type: 'donut',
//                width: '100%',
//                height: 220
//            },
//            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
//            labels: labelsData,
//            dataLabels: {
//                enabled: true,
//                style: {
//                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
//                    fontWeight: '300'
//                },
//                formatter(val, opts) {
//                    const name = opts.w.globals.labels[opts.seriesIndex];
//                    return [name + ' ' + val.toFixed(1) + '%'];
//                }
//            },
//            stroke: {
//                width: 0
//            },
//            fill: {
//                type: 'gradient'
//            },
//            legend: {
//                position: 'bottom',
//                formatter: function(val, opts) {
//                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
//                    return val + ": " + seriesValue + "대";
//                }
//            }
//        };
//        var donut_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
//        donut_chart.render();
//    }
//
//    discover_counts = dataList.discover_data_list[1]
//    discover_items = dataList.discover_data_list[0]
//    createDonutChart("discover_donut", discover_counts, discover_items);


    var discover_data = dataList.discover_data_list;
    var discover_data_day_obj = discover_data.find(item => item[0] === '150_day_ago_day');
    var discover_data_min_obj = discover_data.find(item => item[0] === '150_day_ago_min');
    var discover_data_day = discover_data_day_obj ? discover_data_day_obj[1] : 0;
    var discover_data_min = discover_data_min_obj ? discover_data_min_obj[1] : 0;

    var discover_sub = parseInt(discover_data_min) - parseInt(discover_data_day);
    var discover_per = (parseInt(discover_data_min) - parseInt(discover_data_day)) / parseInt(discover_data_day) * 100;

    var discover_per_round = Math.abs(discover_per.toFixed(2));
    if (isNaN(discover_sub) || isNaN(discover_per_round)) {
        discover_sub = '0';
        discover_per_round = '0%';
    } else if (discover_sub > 0) {
        discover_sub = '+ ' + discover_sub;
        discover_per_round = '▲ ' + discover_per_round + '%';
    } else if (discover_sub < 0) {
        discover_sub = '- ' + Math.abs(discover_sub);
        discover_per_round = '▼ ' + discover_per_round + '%';
    } else {
        discover_per_round += '%';
    }
    var discover_sub_data = document.querySelector('#apexnotconChart_sub');
    discover_sub_data.textContent = discover_sub;

    var discover_per_data = document.querySelector('#apexnotconChart_per');
    discover_per_data.textContent = discover_per_round;

    var apexnotconChartOptions = {
		chart: {
			width: '100%',
			height: 200,
			type: 'bar',
			toolbar: {
				show: false
			},
            events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#discoverChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'discoverChart';
                        var dataPointIndex = config.dataPointIndex;
                        var labelsName = config.w.config.labels[dataPointIndex];
                        document.getElementById('categoryName').value = labelsName;
                        document.getElementById('chartName').value = 'discoverChart';
                        $("#DashModal .modal-title").html(labelsName+' List');
                        osVerPieChart_list(labelsName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
		},
		plotOptions: {
			bar: {
				horizontal: false,
				columnWidth: '70%',
				distributed: true,
				endingShape: 'rounded'

			},
		},
		dataLabels: {
            enabled: true,
            formatter: function (value) {
                return value;
            },
            style: {
                colors: ['#ffffff']
            }
        },
		legend: {
			show: false
		},
		stroke: {
			show: true,
			width: 1,
			colors: ['transparent']
		},
		colors: [app.color.orange],
		series: [{
			data: [discover_data_day, discover_data_min]
		}],
		grid: {
			show: true
		},
		xaxis: {
			categories: [
				'1일 전', '현재'
			],
			labels: {
				show: true,

			},
			crosshairs: {
                show: false
            }
		},
		yaxis: {
			labels: {
				show: true,
				formatter: function (value) {
                    return value;
                }
			}
		},
		fill: {
			opacity: 1
		},
		tooltip: {
			theme: 'dark',
			x: {
				show: true
			},
			y: {
				title: {
					formatter: function (seriesName) {
						return ''
					}
				},
				formatter: function (value) {
                    return value;
                }
			}
		},
	};
	var apexnotconChart = new ApexCharts(document.querySelector('#apexnotconChart'), apexnotconChartOptions);
    apexnotconChart.render();

//############################# 보안패치 차트#################################################
    function createPieChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'pie',
                width: '100%',
                height: 240,
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#hotfix_chart').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'hotfix_chart';
                        var dataPointIndex = config.dataPointIndex;
                        var labelsName = config.w.config.labels[dataPointIndex];
                        document.getElementById('categoryName').value = labelsName;
                        document.getElementById('chartName').value = 'hotfix_chart';
                        $("#DashModal .modal-title").html(labelsName+' List');
                        hotfix_chart_list(labelsName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
                    fontSize: '13px',
                    fontWeight: '300'
                },
                formatter(val, opts) {
                    const name = opts.w.globals.labels[opts.seriesIndex];
                    return [name + ' ' + val.toFixed(1) + '%'];
                }
            },
            stroke: {
                width: 0
            },
            fill: {
                type: 'gradient'
            },
            legend: {
                position: 'bottom',
                formatter: function (val, opts) {
                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
                    return val;
                }
            }
        };
        var donut_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        donut_chart.render();
    }

    hotfix_counts = dataList.hotfix_data_list[1]
    hotfix_items = dataList.hotfix_data_list[0]

    // 순서를 조정합니다.
    const order = ['보안패치 불필요', '보안패치 필요'];

    const sortedItems = [];
    const sortedCounts = [];

    order.forEach(label => {
        const idx = hotfix_items.indexOf(label);
        if(idx !== -1) {
            sortedItems.push(hotfix_items[idx]);
            sortedCounts.push(hotfix_counts[idx]);
        }
    });

    createPieChart("hotfix_donut", sortedCounts, sortedItems);



    //--------------------------------------------------------------------------
    // 자산 관리 현황 관리 자산, 미관리 자산, 예상 유휴 자산 라인차트
    //--------------------------------------------------------------------------
    // var asset_counts = dataList.allAsset_lineData.map(function(item) {
    //     return {x: item.item, y: item.count};
    // });
    // var discover_counts = dataList.discover_lineData.map(function(item) {
    //     return {x: item.item, y: item.count};
    // });
    // var idle_counts = dataList.idle_lineData.map(function(item) {
    //     return {x: item.item, y: item.count};
    // });


//#################################위치별 자산현황###########################################
    function location_chart(divId, seriesData, labelsData) {
        var asset_location_chart_options = {
            chart: {
                type: 'bar',
                background: 'transparent',
                foreColor: 'rgba(255, 255, 255, 0.75)',
                height: 200,
                width: '100%',
                toolbar: {
                    show: false,
                    tools: {
                        zoom: false,
                        pan: false
                    }
                },
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#subnet_chart').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'subnet_chart';
                        var dataPointIndex = config.dataPointIndex;
                        var seriesIndex = config.seriesIndex;
                        var selectedData = config.w.config.series[seriesIndex].data[dataPointIndex];
                        var categoryName = config.w.config.xaxis.categories[dataPointIndex];
                        // var seriesName = config.w.config.series[seriesIndex].name;
                        document.getElementById('categoryName').value = categoryName;
                        // document.getElementById('seriesName').value = seriesName;
                        document.getElementById('chartName').value = 'subnet_chart';
                        $("#DashModal .modal-title").html(categoryName+' List');
                        subnet_chart_list(categoryName, '');
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '50%',
                    distributed: true,
                    endingShape: 'rounded',
                    dataLabels: {
                        total: {
                            enabled: true,
                        },
                    }
                },
            },
            legend: {
                show: false
            },
            dataLabels: {
                enabled: true,
                style: {
                    fontSize: '13px',
                    colors: ["#fff"],
                }
            },
            stroke: {
                width: 3
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            series: [{
                name: '',
                data: seriesData
            }],
            grid: {
                borderColor: 'rgba(144, 164, 174, 0.5)'
            },
            xaxis: {
                categories: labelsData,
                labels: {
                    show: true,
                    style: {
                        fontSize: '13px'
                    }
                },
                crosshairs: {
                    show: false
                }
            },
            yaxis: {
                labels: {
                    show: true,
                    formatter: function (val) {
                        return parseInt(val);
                    }
                }
            }
        };
        var asset_location_chart = new ApexCharts(document.querySelector('#location_bar'), asset_location_chart_options);
        asset_location_chart.render();
    }

    location_counts = dataList.location_data_list[1]
    location_items = dataList.location_data_list[0]
    location_chart("location_bar", location_counts, location_items);


//####################################오피스버전별#########################################
    function office_chart(divId, seriesData, labelsData) {
        var asset_office_chart_options = {
            chart: {
                type: 'bar',
                background: 'transparent',
                foreColor: 'rgba(255, 255, 255, 0.75)',
                height: 200,
                width: '100%',
                toolbar: {
                    show: false,
                    tools: {
                        zoom: false,
                        pan: false
                    }
                },
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#office_chart').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        $('#tcpuChart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'office_chart';
                        var dataPointIndex = config.dataPointIndex;
                        var seriesIndex = config.seriesIndex;
                        var selectedData = config.w.config.series[seriesIndex].data[dataPointIndex];
                        var categoryName = config.w.config.xaxis.categories[dataPointIndex];
                        var seriesName = config.w.config.series[seriesIndex].name;
                        document.getElementById('categoryName').value = categoryName;
                        document.getElementById('seriesName').value = seriesName;
                        document.getElementById('chartName').value = 'office_chart';
                        $("#DashModal .modal-title").html(categoryName+' '+seriesName+' List');
                        office_chart_list(categoryName, seriesName);
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '50%',
                    distributed: true,
                    endingShape: 'rounded',
                    dataLabels: {
                        total: {
                            enabled: true,
                        },
                    }
                },
            },
            legend: {
                show: false
            },
            dataLabels: {
                enabled: true,
                style: {
                    fontSize: '13px',
                    colors: ["#fff"],
                }
            },
            stroke: {
                width: 3
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            series: [{
                name: '',
                data: seriesData,
            }],
            grid: {
                borderColor: 'rgba(144, 164, 174, 0.5)'
            },
            xaxis: {
                categories: labelsData,
                crosshairs: {
                    show: false
                  },
                labels: {
                    show: true,
                    style: {
                        fontSize: '13px'
                    }
                }
            },
            yaxis: {
                labels: {
                    show: true,
                    formatter: function (val) {
                        return parseInt(val);
                    }
                }
            }
        };
        var asset_office_chart = new ApexCharts(document.querySelector('#office_donut'), asset_office_chart_options);
        asset_office_chart.render();
    }

    office_counts = dataList.office_data_list[1]
    office_items = dataList.office_data_list[0]
    office_chart("office_donut", office_counts, office_items);

//#######월별 자산 변화 수##############################
    var MonthlyDesktopData = [];
    var MonthlyNotebookData = [];
    var Months = [];

    dataList.monthly_asset_data_list.forEach(function(entry) {
        if (entry.item === 'Desktop') {
            MonthlyDesktopData.push(entry.item_count);
            Months.push(entry.date);
        } else if (entry.item === 'Notebook') {
            MonthlyNotebookData.push(entry.item_count);
        }
    });

    var asset_ch_chart_options = {
        series: [
            {
                name: 'Desktop',
                data: MonthlyDesktopData
            },
            {
                name: 'Notebook',
                data: MonthlyNotebookData
            }
        ],
        chart: {
            type: 'line',
            background: 'transparent',
            foreColor: 'rgba(255, 255, 255, 0.75)',
            height: 200,
            width: '100%',
            toolbar: {
                show: false,
                tools: {
                    zoom: false,
                    pan: false
                }
            }
        },
        stroke: {
            width: 3
        },
        grid: {
            borderColor: 'rgba(144, 164, 174, 0.5)'
        },
        colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A',],
        dataLabels: {
            enabled: true,
            background: {
                enabled: true,
                // foreColor: 'rgba(29, 40, 53, 0.95)'
                foreColor: ["#fff"]
            },
            dropShadow: {
                enabled: false,
            },
            style: {
                fontSize: '13px',
            }
        },
        xaxis: {
            type: 'category',
            categories: Months
        },
        yaxis: {
            title: {
                text: ''
            }
        },
        legend: {
            markers: {
                fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A',]
            },
            itemMargin: {
                horizontal: 20
            },
            labels: {
                colors: 'rgba(255, 255, 255, 0.75)',
            },
            position: 'top'
        }
    };
    var asset_overview_chart = new ApexCharts(document.querySelector('#chAsset_line'), asset_ch_chart_options);
    asset_overview_chart.render();

//################################# 태니엄 프로스세 cpu 초과######################################################
//    function asset_cpu_chart_options(divId, seriesData, labelsData) {
//        var asset_cpu_chart = {
//            series: seriesData,
//            chart: {
//                type: 'donut',
//                width: '100%',
//                height: 220
//            },
//            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
//            labels: labelsData,
//            dataLabels: {
//                enabled: true,
//                style: {
//                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
//                    fontWeight: '300'
//                },
//                formatter(val, opts) {
//                    const name = opts.w.globals.labels[opts.seriesIndex];
//                    return [val.toFixed(1) + '%'];
//                }
//            },
//            stroke: {
//                width: 0
//            },
//            fill: {
//                type: 'gradient'
//            },
//            legend: {
//                position: 'bottom',
//                formatter: function(val, opts) {
//                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
//                    return val + ": " + seriesValue + "대";
//                }
//            }
//        };
//        var asset_cpu_chart1 = new ApexCharts(document.querySelector("#" + divId), asset_cpu_chart);
//        asset_cpu_chart1.render();
//    }
//    asset_cpu_chart_options("cpu_donut", dataList.cpu_data_list, ['20% 이상', '20% 이하']);
    function apexcpuChart(divId, seriesData, labelsData) {
        var apexcpuOptions = {
            series: [100],
            chart: {
                height: 250,
                type: 'radialBar',
                events: {
                    mounted: (chart) => {
                        chart.windowResizeHandler();
                    }
                },
                events: {
                    dataPointSelection: function (event, chartContext, config) {
                        $('#tcpuChart').DataTable().destroy();
                        $('#subnet_chart').DataTable().destroy();
                        $('#all_asset_detail1').DataTable().destroy();
                        $('#asset_os_detail1').DataTable().destroy();
                        $('#asset_os_detail2').DataTable().destroy();
                        $('#oslistPieChart').DataTable().destroy();
                        $('#osVerPieChart').DataTable().destroy();
                        $('#office_chart').DataTable().destroy();
                        $('#hotfix_chart').DataTable().destroy();
                        document.getElementsByClassName('table m')[0].id = 'tcpuChart';
                        var dataPointIndex = config.dataPointIndex;
                        var seriesIndex = config.seriesIndex;
                        // var selectedData = config.w.config.series[seriesIndex].data[dataPointIndex];
                        var categoryName = config.w.config.plotOptions.radialBar.dataLabels.value.formatter()
                        // var seriesName = config.w.config.series[seriesIndex].name;
                        document.getElementById('categoryName').value = categoryName;
                        // document.getElementById('seriesName').value = seriesName;
                        document.getElementById('chartName').value = 'tcpuChart';
                        $("#DashModal .modal-title").html(categoryName+' List');
                        tcpuChart_list(categoryName, '');
                        // $("#DashModal .allAtbody").html("클릭한 부분의 리스트가 나와야 합니다."+ `<br>`+ "지금은 그냥 라벨값 : "+ categoryName + " " + selectedData + " " + seriesName );
                        $("#DashModal").modal("show");
                    }
                },
            },
            plotOptions: {
                radialBar: {
                    startAngle: -135,
                    endAngle: 225,
                    hollow: {
                        margin: 0,
                        size: '57%',
                        background: 'transparent',
                        image: undefined,
                        imageOffsetX: 0,
                        imageOffsetY: 0,
                        position: 'front',
                        dropShadow: {
                            enabled: true,
                            top: 3,
                            left: 0,
                            blur: 4,
                            opacity: 0.24
                        }
                    },
                    track: {
                        background: ['rgba(' + app.color.whiteRgb + ', .30)'],
                        strokeWidth: '100%',
                        margin: 0, // margin is in pixels
                        dropShadow: {
                            enabled: true,
                            top: -3,
                            left: 0,
                            blur: 4,
                            opacity: 0.35
                        }
                    },
                    dataLabels: {
                        show: true,
                        name: {
                            offsetY: -10,
                            show: true,
                            color: '#fff',
                            fontSize: '20px'
                        },
                        value: {
                            formatter: function (val) {
                                return 'Tanium CPU 10% 초과';
                            },
                            color: '#fff',
                            fontSize: '14px',
                            show: true,
                        }
                    }
                }
            },
            fill: {
                type: 'gradient',
                colors: 'rgba(' + app.color.themeRgb + ', 1)',
            },
            stroke: {
                lineCap: 'round'
            },
            labels: [seriesData + ' 대'],
        };
        var apexcpuChart = new ApexCharts(document.querySelector("#" + divId), apexcpuOptions);
        apexcpuChart.render();
    }

    // createDonutChart("os_donut", os_pieDataCount, os_pieDataItem);

    var cpu_value = dataList.cpu_data_list[0]
    apexcpuChart("apexcpuChart", cpu_value, ['']);


    //--------------------------------------------------------------------------
    // 금일 가장 많이 배포한 패키지 Top 5
    //--------------------------------------------------------------------------
    // var deployToday_barDataItem = []
    // var deployToday_barDataCount = []
    // for (var i = 0; i < dataList.deployToday_barData.length; i++) {
    //     deployToday_barDataItem.push(dataList.deployToday_barData[i]['item']);
    //     deployToday_barDataCount.push(dataList.deployToday_barData[i]['count']);
    // };
    // var today_deploy_chart_options = {
    //   series: [{
    //     name: "",
    //     data: 1
    //   }],
    //   chart: {
    //     height: 200,
    //     type: 'bar',
    //     events: {
    //       click: function(chart, w, e) {
    //       },
    //     }
    //   },
    //   colors: ['#009D83', '#ff9f0c', '#B8A89A', '#46537B', '#2F4858'],
    //   plotOptions: {
    //     bar: {
    //       columnWidth: '45%',
    //       distributed: true,
    //     }
    //   },
    //   dataLabels: {
    //     enabled: false
    //   },
    //   legend: {
    //     show: false
    //   },
    //   tooltip: {
    //     custom: function({ series, seriesIndex, dataPointIndex, w }) {
    //        var color = w.globals.colors[dataPointIndex];
    //        return '<div class="arrow_box" style="padding: 7px 10px; background-color: ' + color + ';">' +
    //            '<span style="font-weight: bold;">' + w.globals.labels[dataPointIndex] + ' : ' + series[seriesIndex][dataPointIndex] + '회' + '</span>' +
    //            '</div>';
    //     }
    //   },
    //   fill: {
    //     type: 'gradient',
    //     gradient: {
    //         type: 'horizontal',
    //         shadeIntensity: 0.8,
    //         gradientToColors: ['#009D83', '#ff9f0c', '#B8A89A', '#46537B', '#2F4858'],
    //         inverseColors: false,
    //         opacityFrom: 1,
    //         opacityTo: 0.8,
    //         stops: [0, 77]
    //     }
    //   },
    //   yaxis: {
    //     labels: {
    //       formatter: function (value) {
    //         return Math.round(value);
    //       }
    //     }
    //   },
    //   xaxis: {
    //     categories: deployToday_barDataItem,
    //     labels: {
    //       style: {
    //         colors: "rgba(" + app.color.whiteRgb + ", 1)",
    //         fontSize: '12px',
    //         fontWeight: '300'
    //       },
    //       formatter: function(val) {
    //         if (val.length > 10) {
    //             return val.substr(0, 10) + '...';
    //         } else {
    //             return val;
    //         }
    //       }
    //     }
    //   }
    // };
    //
    // var today_deploy_chart = new ApexCharts(document.querySelector("#today_deploy_chart"), today_deploy_chart_options);
    // today_deploy_chart.render();
    // document.querySelectorAll('#today_deploy_chart .apexcharts-text title').forEach(title => {
    //     title.remove();
    // });


};

$(document).ready(function () {
    ///////////////////////Datepicker////////////////////
    var previousValue = "";
    var now = new Date();
    var defaultHour = now.getHours();
    var dateTimeSelected = false;
    var reportDate = document.getElementById('datepickerD').placeholder || "";
    $("#datepickerD").datetimepicker({
        format: 'Y-m-d H시',
        formatTime: 'H시',
        defaultDate: now,
        defaultTime: defaultHour + '시',
        closeOnWithoutClick: false,
        onGenerate:function(current_time, $input){
            if(!dateTimeSelected){
                $(".xdsoft_time").on("click", function(){
                    dateTimeSelected = true;
                });
            }
        },
        onChangeDateTime: function(dp, $input) {
            var currentValue = $input.val().replace(' ', '-').replace('시', '');
            if (previousValue !== currentValue && dateTimeSelected) {
                previousValue = currentValue;
                var newURL = "/home/?datetime=" + currentValue;
                window.location.href = newURL;
            }
        }
    });

    $("button.input-group-text").click(function() {
        $("#datepickerD").datetimepicker('show');
    });

    document.getElementById('reportPop').addEventListener('click', function() {
        window.open('../report?datetime=' + reportDate, 'PopupWindowName', 'width=1000,height=1000,scrollbars=no,resizable=no');
    });
        function exportToExcel() {
            var seriesName = document.getElementById('seriesName').value;
            var categoryName = document.getElementById('categoryName').value;
            var chartName = document.getElementById('chartName').value;
            var relativeUrl = "{% url 'export' model='Xfactor_Common' %}";
            var absoluteUrl = window.location.origin + relativeUrl;
            var url = new URL(absoluteUrl);
            url.searchParams.set('parameter_name', chartName);
            url.searchParams.set('seriesName', seriesName);
            url.searchParams.set('categoryName', categoryName);
            window.location.href = url.toString();
        };
///////////////////////Chart////////////////////
    handleRenderChartNCOMG();
    //console.log(dataList);

});