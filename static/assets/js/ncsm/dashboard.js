var randomNo = function () {
    return Math.floor(Math.random() * 60) + 30
};

var handleRenderChartNCOMG = function () {
    // global apexchart settings
    Apex = {
        title: {
          style: {
            fontSize: "12px",
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
            fontSize: "10px",
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
              fontSize: "9px",
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
              fontSize: "9px",
              fontFamily: app.font.family,
              fontWeight: 400,
              cssClass: "apexcharts-xaxis-label",
            },
          },
        },
    };

    var asset_all_chart_options = {
      series: [
        {
          name: ['Desktop'],
          data: [6456,8811]
        },
        {
          name: ['Laptop'],
          data: [123,223]
        }
      ],
      chart: {
        type: 'bar',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
            tools: {
                zoom: false,
                pan: false
            }
        }
      },
        plotOptions: {
      bar: {
        horizontal: true,
        dataLabels: { position: 'top' }
      }
    },
      stroke: {
        width: 3
      },
      grid: {
        borderColor: 'rgba(144, 164, 174, 0.5)'
      },
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: ['Online', 'Total']
      },
      yaxis: {
        title: {
          text: ''
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
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
    var asset_all_chart = new ApexCharts(document.querySelector('#asset_all_chart'), asset_all_chart_options);
    asset_all_chart.render();


    var asset_all_os_chart_options = {
      series: [
        {
          name: ['Desktop'],
          data: [6456,8811]
        },
        {
          name: ['Laptop'],
          data: [123,223]
        }
      ],
      chart: {
        type: 'bar',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
            tools: {
                zoom: false,
                pan: false
            }
        }
      },
        plotOptions: {
      bar: {
        horizontal: true,
        dataLabels: { position: 'top' }
      }
    },
      stroke: {
        width: 3
      },
      grid: {
        borderColor: 'rgba(144, 164, 174, 0.5)'
      },
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: ['Online', 'Total']
      },
      yaxis: {
        title: {
          text: ''
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
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
    var asset_all_os_chart = new ApexCharts(document.querySelector('#asset_all_os_chart'), asset_all_os_chart_options);
    asset_all_os_chart.render();


    //--------------------------------------------------------------------------
    // 자산 관리 현황 미니도넛, 프로그레스 바 - DISK 사용률 초과 서버, MEMORY 사용률 초과 서버
    //--------------------------------------------------------------------------

    // var disk_widthPercentage = (dataList.disk_donutData / dataList.allOnline_donutData) * 100;
    // document.querySelector("#disk-bar").style.width = disk_widthPercentage + "%";
    // var mem_widthPercentage = (dataList.memory_donutData / dataList.allOnline_donutData) * 100;
    // document.querySelector("#mem-bar").style.width = mem_widthPercentage + "%";
    // var cpu_widthPercentage = (dataList.cpu_donutData / dataList.allOnline_donutData) * 100;
    // document.querySelector("#cpu-bar").style.width = cpu_widthPercentage + "%";
    var om_disk_chartOptions = {
        series: [20, 20, 20, 20, 20],
        chart: {
          width: 100,
          height: 100,
          type: 'donut',
          toolbar: {
            show: false
          }
        },
        colors: ['rgba(223, 224, 223, .2)', 'rgba(223, 224, 223, .4)', 'rgba(223, 224, 223, .5)', 'rgba(223, 224, 223, .8)', 'rgba(223, 224, 223, 1)'],
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: false
              }
            }
          }
        },
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        stroke: {
          show: false
        },
        tooltip: {
          enabled: false
        }
    };
    var chartContainers = document.querySelectorAll('.om_disk_chart');
    chartContainers.forEach(function(container) {
        var chart = new ApexCharts(container, om_disk_chartOptions);
        chart.render();
    });
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

    function osPieChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'pie',
                width: '100%',
                height: 240
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
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
                formatter: function(val, opts) {
                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
                    return val;
                }
            }
        };
        var os_pie_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        os_pie_chart.render();
    }

    // createDonutChart("os_donut", os_pieDataCount, os_pieDataItem);
    osPieChart("os_pie", [2312, 4322], ['업데이트 필요', '업데이트 완료']);

    function createDonutChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'donut',
                width: '100%',
                height: 220
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
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
                formatter: function(val, opts) {
                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
                    return val + ": " + seriesValue + "대";
                }
            }
        };
        var donut_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        donut_chart.render();
    }

    function createPieChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'pie',
                width: '100%',
                height: 240
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
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
                formatter: function(val, opts) {
                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
                    return val;
                }
            }
        };
        var donut_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        donut_chart.render();
    }

    // createDonutChart("os_donut", os_pieDataCount, os_pieDataItem);
    createPieChart("sec_patch_pie", [2312, 4322], ['보안패치 필요', '보안패치 완료']);
    createDonutChart("notConnected_donut", [6234,111], ['접속', '미접속']);

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

    var asset_location_chart_options = {
      series: [
        {
          name: '',
          data: [6456,223,98]
        }
      ],
      chart: {
        type: 'bar',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
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
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: ['사내망', '외부망', 'VPN']
      },
      yaxis: {
        title: {
          text: ''
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
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
    var asset_location_chart = new ApexCharts(document.querySelector('#location_bar'), asset_location_chart_options);
    asset_location_chart.render();

    var office_version_chart_options = {
      series: [
        {
          name: '',
          data: [6456,223,98]
        }
      ],
      chart: {
        type: 'bar',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
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
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: ['Office 365', 'Office 2019', 'Office 2013']
      },
      yaxis: {
        title: {
          text: ''
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
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
    var office_version_chart = new ApexCharts(document.querySelector('#office_bar'), office_version_chart_options);
    office_version_chart.render();


    var asset_ch_chart_options = {
      series: [
        {
          name: 'Desktop',
          data: [3245,4561,5689,5690,5702,5720,5732,5750]
        },
        {
          name: 'Laptop',
          data: [700, 1332,1334,1454,1554,1556,1556,1559]
        }
      ],
      chart: {
        type: 'line',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
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
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월']
      },
      yaxis: {
        title: {
          text: ''
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
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


    var asset_cpu_chart_options = {
      series: [
        {
          name: '',
          data: [1,2,3,9,12,13,14,24,28,15,2,9]
        }
      ],
      chart: {
        type: 'line',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
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
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: ['28일', '29일', '30일', '31일', '1일', '2일', '3일', '4일', '5일', '6일', '7일', '8일']
      },
      yaxis: {
        title: {
          text: ''
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
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
    var asset_cpu_chart = new ApexCharts(document.querySelector('#cpu_line'), asset_cpu_chart_options);
    asset_cpu_chart.render();
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
    handleRenderChartNCOMG();
});