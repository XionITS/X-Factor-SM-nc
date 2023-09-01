// /*
// Template Name: HUD - Responsive Bootstrap 5 Admin Template
// Version: 1.8.0
// Author: Sean Ngu
//
// */
//
//
// var randomNo = function () {
//     return Math.floor(Math.random() * 60) + 30
// };
//
//
// var handleRenderChartNC2 = function () {
//     // global apexchart settings
//
//     Apex = {
//         title: {
//           style: {
//             fontSize: "12px",
//             fontWeight: "bold",
//             fontFamily: app.font.family,
//             color: app.color.white,
//           },
//         },
//         legend: {
//           fontFamily: app.font.family,
//           labels: {
//             colors: "#fff",
//             show: true,
//           },
//         },
//         tooltip: {
//           style: {
//             fontSize: "10px",
//             fontFamily: app.font.family,
//           },
//         },
//         grid: {
//           borderColor: "rgba(" + app.color.whiteRgb + ", .25)",
//         },
//         dataLabels: {
//           style: {
//             fontSize: "12px",
//             fontFamily: app.font.family,
//             fontWeight: "bold",
//             colors: undefined,
//           },
//         },
//         xaxis: {
//           axisBorder: {
//             show: false,
//             color: "rgba(" + app.color.whiteRgb + ", .25)",
//             height: 1,
//             width: "100%",
//             offsetX: 0,
//             offsetY: -1,
//           },
//           axisTicks: {
//             show: false,
//             borderType: "solid",
//             color: "rgba(" + app.color.whiteRgb + ", .25)",
//             height: 6,
//             offsetX: 0,
//             offsetY: 0,
//           },
//           labels: {
//             style: {
//               colors: "#fff",
//               fontSize: "9px",
//               fontFamily: app.font.family,
//               fontWeight: 400,
//               cssClass: "apexcharts-xaxis-label",
//             },
//           },
//         },
//         yaxis: {
//           labels: {
//             style: {
//               colors: "#fff",
//               fontSize: "9px",
//               fontFamily: app.font.family,
//               fontWeight: 400,
//               cssClass: "apexcharts-xaxis-label",
//             },
//           },
//         },
//     };
//
//     //--------------------------------------------------------------------------
//     // OM - diskChart
//     //--------------------------------------------------------------------------
//
//     for (var i = 0; i < a.ResourceDiskChartDataList.length; i++) {
//         if (a.ResourceDiskChartDataList[i]['name'] == '60Risk') {
//           disk60 = a.ResourceDiskChartDataList[i]['value']
//         } else if (a.ResourceDiskChartDataList[i]['name'] == '75Risk') {
//           disk75 = a.ResourceDiskChartDataList[i]['value']
//         } else if (a.ResourceDiskChartDataList[i]['name'] == '95Risk') {
//           disk95 = a.ResourceDiskChartDataList[i]['value']
//         } else if (a.ResourceDiskChartDataList[i]['name'] == '99Risk') {
//           disk99 = a.ResourceDiskChartDataList[i]['value']
//         }
//     };
//
//     if (a.ResourceDiskChartDataList[0]['name'] == '-') {
//         disk99 = '-'
//         disk95 = '-'
//         disk75 = ''
//         disk60 = ''
//     };
//     var om_disk_chartOptions = {
//         series: [100],
//         chart: {
//           height: 280,
//           type: 'radialBar',
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             }
//           },
//         },
//         plotOptions: {
//
//           radialBar: {
//             hollow: {
//               margin: -50,
//               size: '50%',
//               background: 'transparent',
//               image: undefined,
//               imageOffsetX: 0,
//               imageOffsetY: 0,
//               position: 'front',
//               dropShadow: {
//                 enabled: true,
//                 top: 3,
//                 left: 0,
//                 blur: 4,
//                 opacity: 0.24
//               }
//             },
//             track: {
//               background: ['rgba(' + app.color.whiteRgb + ', .30)'],
//               strokeWidth: '10%',
//               margin: 0, // margin is in pixels
//               dropShadow: {
//                 enabled: true,
//                 top: -3,
//                 left: 0,
//                 blur: 4,
//                 opacity: 0.35
//               }
//             },
//             dataLabels: {
//               show: true,
//               name: {
//                 offsetY: -10,
//                 show: true,
//                 color: '#fff',
//                 fontSize: '20px'
//               },
//               value: {
//                 formatter: function (val) {
//                   return  '95% 초과';
//                 },
//                 color: '#fff',
//                 fontSize: '14px',
//                 show: true,
//               }
//             }
//           }
//         },
//         fill: {
//           type: 'gradient',
//           colors: '#fe8c00',
//           gradient: {
//             shade: 'dark',
//             type: 'horizontal',
//             shadeIntensity: 0.5,
//             gradientToColors: ['#f83600'],
//             inverseColors: true,
//             opacityFrom: 1,
//             opacityTo: 1,
//             stops: [0, 100]
//           }
//         },
//         stroke: {
//           lineCap: 'round'
//         },
//         labels: [disk95 + ' 대'],
//     };
//     var om_disk_chart = new ApexCharts(document.querySelector('#om_disk_chart'),om_disk_chartOptions);
//     om_disk_chart.render();
//
//
//     //--------------------------------------------------------------------------
//     // OM - om_mem_chart
//     //--------------------------------------------------------------------------
//     for (var i = 0; i < a.ResourceMemoryChartDataList.length; i++) {
//         if (a.ResourceMemoryChartDataList[i]['name'] == '60Risk') {
//           memory60 = a.ResourceMemoryChartDataList[i]['value']
//         } else if (a.ResourceMemoryChartDataList[i]['name'] == '75Risk') {
//           memory75 = a.ResourceMemoryChartDataList[i]['value']
//         } else {
//           memory95 = a.ResourceMemoryChartDataList[i]['value']
//         }
//     };
//
//
//     if (a.ResourceMemoryChartDataList[0]['name'] == '-') {
//         memory95 = '-'
//         memory75 = ''
//         memory60 = ''
//     }
//     var om_mem_chartOptions = {
//         series: [100],
//         chart: {
//           height: 280,
//           type: 'radialBar',
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             }
//           },
//         },
//         plotOptions: {
//
//           radialBar: {
//             hollow: {
//               margin: -50,
//               size: '50%',
//               background: 'transparent',
//               image: undefined,
//               imageOffsetX: 0,
//               imageOffsetY: 0,
//               position: 'front',
//               dropShadow: {
//                 enabled: true,
//                 top: 3,
//                 left: 0,
//                 blur: 4,
//                 opacity: 0.24
//               }
//             },
//             track: {
//               background: ['rgba(' + app.color.whiteRgb + ', .30)'],
//               strokeWidth: '10%',
//               margin: 0, // margin is in pixels
//               dropShadow: {
//                 enabled: true,
//                 top: -3,
//                 left: 0,
//                 blur: 4,
//                 opacity: 0.35
//               }
//             },
//             dataLabels: {
//               show: true,
//               name: {
//                 offsetY: -10,
//                 show: true,
//                 color: '#fff',
//                 fontSize: '20px'
//               },
//               value: {
//                 formatter: function (val) {
//                   return  '95% 초과';
//                 },
//                 color: '#fff',
//                 fontSize: '14px',
//                 show: true,
//               }
//             }
//           }
//         },
//         fill: {
//           type: 'gradient',
//           colors: '#fe8c00',
//           gradient: {
//             shade: 'dark',
//             type: 'horizontal',
//             shadeIntensity: 0.5,
//             gradientToColors: ['#f83600'],
//             inverseColors: true,
//             opacityFrom: 1,
//             opacityTo: 1,
//             stops: [0, 100]
//           }
//         },
//         stroke: {
//           lineCap: 'round'
//         },
//         labels: [memory95+ ' 대'],
//     };
//     var om_mem_chart = new ApexCharts(document.querySelector('#om_mem_chart'),om_mem_chartOptions);
//     om_mem_chart.render();
//
//
//
//     //--------------------------------------------------------------------------
//     // OM- om_os_chart
//     //--------------------------------------------------------------------------
//     var osDonutValue = []
//     var osDonutName = []
//
//     for (var i = 0; i < a.os_pieChartData.length; i++) {
//         if (a.os_pieChartData[i]['name'] == 'Windows'){
//             osDonutValue.push(a.os_pieChartData[i]['value']);
//             osDonutName.push(a.os_pieChartData[i]['name']);
//         }else if (a.os_pieChartData[i].name == 'Linux'){
//             osDonutValue.push(a.os_pieChartData[i]['value']);
//             osDonutName.push(a.os_pieChartData[i]['name']);
//         }else if (a.os_pieChartData[i].name == 'Mac'){
//             osDonutValue.push(a.os_pieChartData[i]['value']);
//             osDonutName.push(a.os_pieChartData[i]['name']);
//         }
//     };
//
//     var om_os_chartOptions = {
//         chart: {
//           height: 220,
//           type: 'pie',
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             },
//           },
//         },
//         plotOptions: {
//           pie: {
//             dataLabels: {
//               offset: 8
//             },
//           },
//         },
//         dataLabels: {
//           enabled: true,
//           formatter(val, opts) {
//             const name = opts.w.globals.labels[opts.seriesIndex]
//             return [name+' ' + val.toFixed(1) + '%']
//           },
//           style: {
//             fontSize: '16px',
//             colors: [app.color.white],
//             fontWeight: 400
//           },
//         },
//         stroke: {
//           show: false
//         },
//         legend: {
//           show: false,
//           position: 'left',
//         },
//         colors: ["#b76306", "#db7f08", "#ff9f0c", "#ffbe48", "#ffd16d", "#ffe49d", "#fff3ce"],
//         labels: osDonutName,
//         series: osDonutValue,
//         tooltip: {
//           theme: 'dark',
//           x: {
//             show: true
//           },
//           y: {
//             title: {
//               formatter: function (val) {
//                 return '' + val + "<br>" + " Count:"
//               }
//             },
//             formatter: (value) => { return '' + value },
//           }
//         }
//     };
//     var om_os_chart = new ApexCharts(document.querySelector('#om_os_chart'),om_os_chartOptions);
//     om_os_chart.render();
//
//
//
//
//     //--------------------------------------------------------------------------
//     // OM- om_wire_chart
//     //--------------------------------------------------------------------------
//     var wireValue = []
//     var wireName = []
//
//     for (var i = 0; i < a.wire_pieChartData.length; i++) {
//         if ((a.wire_pieChartData[i]['name']) == 'Wired'){
//             wireValue.push(a.wire_pieChartData[i]['value']);
//             wireName.push(a.wire_pieChartData[i]['name']);
//         }else if ((a.wire_pieChartData[i]['name']) == 'Wireless'){
//             wireValue.push(a.wire_pieChartData[i]['value']);
//             wireName.push(a.wire_pieChartData[i]['name']);
//         }
//     };
//
//     var om_wire_chartOptions = {
//         chart: {
//           height: 220,
//           type: 'pie',
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             },
//           },
//         },
//         plotOptions: {
//           pie: {
//             dataLabels: {
//               offset: 8
//             },
//           },
//         },
//         dataLabels: {
//           enabled: true,
//           formatter(val, opts) {
//             const name = opts.w.globals.labels[opts.seriesIndex]
//             return [name+' ' + val.toFixed(1) + '%']
//           },
//           style: {
//             fontSize: '16px',
//             colors: [app.color.white],
//             fontWeight: 400
//           },
//         },
//         stroke: {
//           show: false
//         },
//         legend: {
//           show: false,
//           position: 'left',
//         },
//         colors: ["#db7f08", "#ff9f0c", "#ffbe48", "#ffd16d", "#ffe49d", "#fff3ce"],
//         labels: wireName,
//         series: wireValue,
//         tooltip: {
//           theme: 'dark',
//           x: {
//             show: true
//           },
//           y: {
//             title: {
//               formatter: function (val) {
//                 return '' + val + "<br>" + " Count:"
//               }
//             },
//             formatter: (value) => { return '' + value },
//           }
//         }
//     };
//     var om_wire_chart = new ApexCharts(document.querySelector('#om_wire_chart'),om_wire_chartOptions);
//     om_wire_chart.render();
//
//
//
//
//     //--------------------------------------------------------------------------
//     // OM- om_vp_chart
//     //--------------------------------------------------------------------------
//     var vpDonutValue = []
//
//     for (var i = 0; i < a.virtual_pieChartData.length; i++) {
//         if ((a.virtual_pieChartData[i]['name']) == 'No'){
//             vpDonutValue.push(a.virtual_pieChartData[i]['value']);
//         }else if ((a.virtual_pieChartData[i]['name']) == 'Yes'){
//             vpDonutValue.push(a.virtual_pieChartData[i]['value']);
//         }
//     };
//     console.log(vpDonutValue);
//     var om_vp_chartOptions = {
//         chart: {
//           height: 220,
//           type: 'pie',
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             },
//           },
//         },
//         plotOptions: {
//           pie: {
//             dataLabels: {
//               offset: 8
//             },
//           },
//         },
//         dataLabels: {
//           enabled: true,
//           formatter(val, opts) {
//             const name = opts.w.globals.labels[opts.seriesIndex]
//             return [name+' ' + val.toFixed(1) + '%']
//           },
//           style: {
//             fontSize: '16px',
//             colors: [app.color.white],
//             fontWeight: 400
//           },
//         },
//         stroke: {
//           show: false
//         },
//         legend: {
//           show: false,
//           position: 'left',
//         },
//         colors: ["#db7f08", "#ff9f0c", "#ffbe48", "#ffd16d", "#ffe49d", "#fff3ce"],
//         labels: ['Physical','Virtual'],
//         series: vpDonutValue,
//         tooltip: {
//           theme: 'dark',
//           x: {
//             show: true
//           },
//           y: {
//             title: {
//               formatter: function (val) {
//                 return '' + val + "<br>" + " Count:"
//               }
//             },
//             formatter: (value) => { return '' + value },
//           }
//         }
//     };
//     var om_vp_chart = new ApexCharts(document.querySelector('#om_vp_chart'),om_vp_chartOptions);
//     om_vp_chart.render();
//
//
//
//
//
//     //--------------------------------------------------------------------------
//     // OM_관리자산 om_m_chart
//     //--------------------------------------------------------------------------
//     //console.log(a.server_LChartDataList[0].data[1]);
//     //var virtual_Value2 = a.server_LChartDataList[0].data[0]
//
//     var om_m_chartOptions = {
//         chart: {
//           height: 145,
//           type: 'line',
//           toolbar: {
//             show: false
//           },
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             }
//           },
//         },
//         colors: ['rgba(' + app.color.themeRgb + ', .95)', 'rgba(' + app.color.themeRgb + ', .30)'],
//         dataLabels: {
//           enabled: false,
//         },
//         stroke: {
//           curve: 'smooth',
//           width: 3
//         },
//         grid: {
//           row: {
//             colors: ['rgba(' + app.color.whiteRgb + ', .25)', 'transparent'], // takes an array which will be repeated on columns
//             opacity: 0.5
//           }
//         },
//         markers: {
//           size: 1,
//         },
//         series: [{
//             data: [20,20,20,15,18,15,12,20,15,15]
//         }],
//         xaxis: {
//           categories: ['11','12','13','14','15','16','17','18','19','20'],
//           labels: {
//             show: true,
//           },
//           tooltip: {
//             enabled: false,
//           },
//         },
//         yaxis: {
//           labels: {
//             show: true,
//             formatter: function (val) {
//               return Math.round(val);
//             }
//           }
//         },
//         tooltip: {
//           theme: 'dark',
//           x: {
//             show: true,
//           },
//           y: {
//             title: {
//               formatter: function (val) {
//                 return '' + val
//               }
//             },
//             formatter: (value) => { return '' + value },
//           }
//         },
//         legend: {
//           show: false,
//           position: 'top',
//           offsetY: 1,
//           horizontalAlign: 'right',
//           floating: true,
//         }
//     };
//     var om_m_chart = new ApexCharts(
//     document.querySelector('#om_m_chart'),om_m_chartOptions);
//     om_m_chart.render();
//
//    //--------------------------------------------------------------------------
//     // OM_미관리자산 om_um_chart
//     //--------------------------------------------------------------------------
//     var om_um_chartOptions2 = {
//         chart: {
//           height: 145,
//           type: 'line',
//           toolbar: {
//             show: false
//           },
//           events: {
//             mounted: (chart) => {
//               chart.windowResizeHandler();
//             }
//           },
//         },
//         colors: ['rgba(' + app.color.themeRgb + ', .95)', 'rgba(' + app.color.themeRgb + ', .30)'],
//         dataLabels: {
//           enabled: false,
//         },
//         stroke: {
//           curve: 'smooth',
//           width: 3
//         },
//         grid: {
//           row: {
//             colors: ['rgba(' + app.color.whiteRgb + ', .25)', 'transparent'], // takes an array which will be repeated on columns
//             opacity: 0.5
//           }
//         },
//         markers: {
//           size: 1,
//         },
//         series: [{
//             data: [9,20,13,15,8,15,12,11,15,20]
//         }],
//         xaxis: {
//           categories: ['11','12','13','14','15','16','17','18','19','20'],
//           labels: {
//             show: true,
//           },
//           tooltip: {
//             enabled: false,
//           },
//         },
//         yaxis: {
//           labels: {
//             show: true,
//             formatter: function (val) {
//               return Math.round(val);
//             }
//           }
//         },
//         tooltip: {
//           theme: 'dark',
//           x: {
//             show: true,
//           },
//           y: {
//             title: {
//               formatter: function (val) {
//                 return '' + val
//               }
//             },
//             formatter: (value) => { return '' + value },
//           }
//         },
//         legend: {
//           show: false,
//           position: 'top',
//           offsetY: 1,
//           horizontalAlign: 'right',
//           floating: true
//         }
//     };
//     var om_um_chart = new ApexCharts(
//     document.querySelector('#om_um_chart'),om_um_chartOptions2);
//     om_um_chart.render();
//
// /* Controller
// ------------------------------------------------ */
// $(document).ready(function () {
// handleRenderChartNC2();
//
//
// });
//
//
//
//
//
