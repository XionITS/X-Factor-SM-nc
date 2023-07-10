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

    //--------------------------------------------------------------------------
    // OM - diskChart
    //--------------------------------------------------------------------------

    var om_disk_chartOptions = {
        series: [100],
        chart: {
          height: 280,
          type: 'radialBar',
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            }
          },
        },
        plotOptions: {

          radialBar: {
            hollow: {
              margin: -50,
              size: '50%',
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
              strokeWidth: '10%',
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
                  return  '95% 초과';
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
          colors: '#fe8c00',
          gradient: {
            shade: 'dark',
            type: 'horizontal',
            shadeIntensity: 0.5,
            gradientToColors: ['#f83600'],
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100]
          }
        },
        stroke: {
          lineCap: 'round'
        },
        labels: [ dataList.disk_donutData + ' 대']
    };
    var om_disk_chart = new ApexCharts(document.querySelector('#om_disk_chart'),om_disk_chartOptions);
    om_disk_chart.render();


    //--------------------------------------------------------------------------
    // OM - om_mem_chart
    //--------------------------------------------------------------------------
    var om_mem_chartOptions = {
        series: [100],
        chart: {
          height: 280,
          type: 'radialBar',
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            }
          },
        },
        plotOptions: {

          radialBar: {
            hollow: {
              margin: -50,
              size: '50%',
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
              strokeWidth: '10%',
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
                  return  '95% 초과';
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
          colors: '#fe8c00',
          gradient: {
            shade: 'dark',
            type: 'horizontal',
            shadeIntensity: 0.5,
            gradientToColors: ['#f83600'],
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100]
          }
        },
        stroke: {
          lineCap: 'round'
        },
        labels: [dataList.memory_donutData+ ' 대'],
    };
    var om_mem_chart = new ApexCharts(document.querySelector('#om_mem_chart'),om_mem_chartOptions);
    om_mem_chart.render();



    //--------------------------------------------------------------------------
    // OM- om_os_chart
    //--------------------------------------------------------------------------
    var os_pieDataItem = []
    var os_pieDataCount = []

    for (var i = 0; i < dataList.os_pieData.length; i++) {
        os_pieDataItem.push(dataList.os_pieData[i]['item']);
        os_pieDataCount.push(dataList.os_pieData[i]['count']);
    };

    var om_os_chartOptions = {
        chart: {
          height: 220,
          type: 'pie',
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            },
          },
        },
        plotOptions: {
          pie: {
            dataLabels: {
              offset: 8
            },
          },
        },
        dataLabels: {
          enabled: true,
          formatter(val, opts) {
            const name = opts.w.globals.labels[opts.seriesIndex]
            return [name+' ' + val.toFixed(1) + '%']
          },
          style: {
            fontSize: '16px',
            colors: [app.color.white],
            fontWeight: 400
          },
        },
        stroke: {
          show: false
        },
        legend: {
          show: false,
          position: 'left',
        },
        colors: ["#b76306", "#db7f08", "#ff9f0c", "#ffbe48", "#ffd16d", "#ffe49d", "#fff3ce"],
        labels: os_pieDataItem,
        series: os_pieDataCount,
        tooltip: {
          theme: 'dark',
          x: {
            show: true
          },
          y: {
            title: {
              formatter: function (val) {
                return '' + val + "<br>" + " Count:"
              }
            },
            formatter: (value) => { return '' + value },
          }
        }
    };
    var om_os_chart = new ApexCharts(document.querySelector('#om_os_chart'),om_os_chartOptions);
    om_os_chart.render();




    //--------------------------------------------------------------------------
    // OM- om_wire_chart
    //--------------------------------------------------------------------------
    var wire_pieDataItem = []
    var wire_pieDataCount = []

    for (var i = 0; i < dataList.wire_pieData.length; i++) {
        wire_pieDataItem.push(dataList.wire_pieData[i]['item']);
        wire_pieDataCount.push(dataList.wire_pieData[i]['count']);
    };

    var om_wire_chartOptions = {
        chart: {
          height: 220,
          type: 'pie',
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            },
          },
        },
        plotOptions: {
          pie: {
            dataLabels: {
              offset: 8
            },
          },
        },
        dataLabels: {
          enabled: true,
          formatter(val, opts) {
            const name = opts.w.globals.labels[opts.seriesIndex]
            return [name+' ' + val.toFixed(1) + '%']
          },
          style: {
            fontSize: '16px',
            colors: [app.color.white],
            fontWeight: 400
          },
        },
        stroke: {
          show: false
        },
        legend: {
          show: false,
          position: 'left',
        },
        colors: ["#db7f08", "#ff9f0c", "#ffbe48", "#ffd16d", "#ffe49d", "#fff3ce"],
        labels: wire_pieDataItem,
        series: wire_pieDataCount,
        tooltip: {
          theme: 'dark',
          x: {
            show: true
          },
          y: {
            title: {
              formatter: function (val) {
                return '' + val + "<br>" + " Count:"
              }
            },
            formatter: (value) => { return '' + value },
          }
        }
    };
    var om_wire_chart = new ApexCharts(document.querySelector('#om_wire_chart'),om_wire_chartOptions);
    om_wire_chart.render();




    //--------------------------------------------------------------------------
    // OM- om_vp_chart
    //--------------------------------------------------------------------------
    var virtual_pieDataItem = []
    var virtual_pieDataCount = []

    for (var i = 0; i < dataList.virtual_pieData.length; i++) {
        virtual_pieDataItem.push(dataList.virtual_pieData[i]['item']);
        virtual_pieDataCount.push(dataList.virtual_pieData[i]['count']);
    };

    var om_vp_chartOptions = {
        chart: {
          height: 220,
          type: 'pie',
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            },
          },
        },
        plotOptions: {
          pie: {
            dataLabels: {
              offset: 8
            },
          },
        },
        dataLabels: {
          enabled: true,
          formatter(val, opts) {
            const name = opts.w.globals.labels[opts.seriesIndex]
            return [name+' ' + val.toFixed(1) + '%']
          },
          style: {
            fontSize: '16px',
            colors: [app.color.white],
            fontWeight: 400
          },
        },
        stroke: {
          show: false
        },
        legend: {
          show: false,
          position: 'left',
        },
        colors: ["#db7f08", "#ff9f0c", "#ffbe48", "#ffd16d", "#ffe49d", "#fff3ce"],
        labels: virtual_pieDataItem,
        series: virtual_pieDataCount,
        tooltip: {
          theme: 'dark',
          x: {
            show: true
          },
          y: {
            title: {
              formatter: function (val) {
                return '' + val + "<br>" + " Count:"
              }
            },
            formatter: (value) => { return '' + value },
          }
        }
    };
    var om_vp_chart = new ApexCharts(document.querySelector('#om_vp_chart'),om_vp_chartOptions);
    om_vp_chart.render();

    //--------------------------------------------------------------------------
    // OM_관리자산 om_m_chart
    //--------------------------------------------------------------------------
    var allAsset_lineDataItem = []
    var allAsset_lineDataCount = []
    //console.log(dataList)
    for (var i = 0; i < dataList.allAsset_lineData.length; i++) {
        allAsset_lineDataItem.push(dataList.allAsset_lineData[i]['item']);
        allAsset_lineDataCount.push(dataList.allAsset_lineData[i]['count']);
    };
    var om_m_chartOptions = {
        chart: {
          height: 145,
          type: 'line',
          toolbar: {
            show: false
          },
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            }
          },
        },
        colors: ['rgba(' + app.color.themeRgb + ', .95)', 'rgba(' + app.color.themeRgb + ', .30)'],
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
          width: 3
        },
        grid: {
          row: {
            colors: ['rgba(' + app.color.whiteRgb + ', .25)', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          }
        },
        markers: {
          size: 1,
        },
        series: [{
            data: allAsset_lineDataCount
        }],
        xaxis: {
          categories: allAsset_lineDataItem,
          labels: {
            show: true,
          },
          tooltip: {
            enabled: false,
          },
        },
        yaxis: {
          labels: {
            show: true,
            formatter: function (val) {
              return Math.round(val);
            }
          }
        },
        tooltip: {
          theme: 'dark',
          x: {
            show: true,
          },
          y: {
            title: {
              formatter: function () {
                return 'Count'
              }
            },
            formatter: (value) => { return '' + value },
          }
        },
        legend: {
          show: false,
          position: 'top',
          offsetY: 1,
          horizontalAlign: 'right',
          floating: true,
        }
    };
    var om_m_chart = new ApexCharts(
    document.querySelector('#om_m_chart'),om_m_chartOptions);
    om_m_chart.render();

   //--------------------------------------------------------------------------
    // OM_미관리자산 om_um_chart
    //--------------------------------------------------------------------------
    var discover_lineDataItem = []
    var discover_lineDataCount = []
    //console.log(dataList)
    for (var i = 0; i < dataList.discover_lineData.length; i++) {
        discover_lineDataItem.push(dataList.discover_lineData[i]['item']);
        discover_lineDataCount.push(dataList.discover_lineData[i]['count']);
    };

    var om_um_chartOptions = {
        chart: {
          height: 145,
          type: 'line',
          toolbar: {
            show: false
          },
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            }
          },
        },
        colors: ['rgba(' + app.color.themeRgb + ', .95)', 'rgba(' + app.color.themeRgb + ', .30)'],
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
          width: 3
        },
        grid: {
          row: {
            colors: ['rgba(' + app.color.whiteRgb + ', .25)', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          }
        },
        markers: {
          size: 1,
        },
        series: [{
            data: discover_lineDataCount
        }],
        xaxis: {
          categories: discover_lineDataItem,
          labels: {
            show: true,
          },
          tooltip: {
            enabled: false,
          },
        },
        yaxis: {
          labels: {
            show: true,
            formatter: function (val) {
              return Math.round(val);
            }
          }
        },
        tooltip: {
          theme: 'dark',
          x: {
            show: true,
          },
          y: {
            title: {
              formatter: function () {
                return 'Count'
              }
            },
            formatter: (value) => { return '' + value },
          }
        },
        legend: {
          show: false,
          position: 'top',
          offsetY: 1,
          horizontalAlign: 'right',
          floating: true
        }
    };
    var om_um_chart = new ApexCharts(
    document.querySelector('#om_um_chart'),om_um_chartOptions);
    om_um_chart.render();












    //--------------------------------------------------------------------------
    // Total quantity of servers - apexTotalServerChart Virtual
    //--------------------------------------------------------------------------
    var idle_lineDataItem = []
    var idle_lineDataCount = []
console.log(dataList.idle_lineData);
    for (var i = 0; i < dataList.idle_lineData.length; i++) {
        idle_lineDataItem.push(dataList.idle_lineData[i]['item']);
        idle_lineDataCount.push(dataList.idle_lineData[i]['count']);
    };


    //console.log(dataList.idle_lineData);
    var idle_chart = {
        chart: {
          height: 145,
          type: 'line',
          toolbar: {
            show: false
          },
          events: {
            mounted: (chart) => {
              chart.windowResizeHandler();
            }
          },
        },
        colors: ['rgba(' + app.color.themeRgb + ', .95)', 'rgba(' + app.color.themeRgb + ', .30)'],
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
          width: 3
        },
        grid: {
          row: {
            colors: ['rgba(' + app.color.whiteRgb + ', .25)', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          }
        },
        markers: {
          size: 1,
        },
        series: [{
            data: idle_lineDataCount
        }],
        xaxis: {
          categories: idle_lineDataItem,
          labels: {
            show: true,
          },
          tooltip: {
            enabled: false,
          },
        },
        yaxis: {
          labels: {
            show: true,
            formatter: function (val) {
              return Math.round(val);
            }
          }
        },
        tooltip: {
          theme: 'dark',
          x: {
            show: true,
          },
          y: {
            title: {
              formatter: function (val) {
                return '' + val
              }
            },
            formatter: (value) => { return '' + value },
          }
        },
        legend: {
          show: false,
          position: 'top',
          offsetY: 1,
          horizontalAlign: 'right',
          floating: true
        }
    };
    var idle_line_chart = new ApexCharts(
    document.querySelector('#idle_chart'),idle_chart);
    idle_line_chart.render();
};
$(document).ready(function () {
handleRenderChartNCOMG();
});





