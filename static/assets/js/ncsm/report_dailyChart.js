/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu
Website: http://www.seantheme.com/hud/
*/

//세자리 숫자마다 ,붙여주는 함수
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

//null 값을 0으로 변환하는 함수
function parseValue(value) {
    return value === "null" ? 0 : value;
}

var handleRenderdailyApexChart = function () {
	Apex = {
		title: {
			style: {
				fontSize: '14px',
				fontWeight: 'bold',
				fontFamily: app.font.family,
				color: app.color.white
			},
		},
		legend: {
			fontFamily: app.font.family,
			labels: {
				colors: app.color.black
			}
		},
		tooltip: {
			style: {
				fontSize: '10px',
				fontFamily: app.font.family
			}
		},
		grid: {
			borderColor: 'rgba(' + app.color.darkRgb + ', .25)',
		},
		dataLabels: {
			style: {
				fontSize: '10px',
				fontFamily: app.font.family,
				fontWeight: 'bold',
				colors: undefined
			}
		},
		xaxis: {
			axisBorder: {
				show: true,
				color: 'rgba(' + app.color.whiteRgb + ', .25)',
				height: 1,
				width: '100%',
				offsetX: 0,
				offsetY: -1
			},
			axisTicks: {
				show: true,
				borderType: 'solid',
				color: 'rgba(' + app.color.whiteRgb + ', .25)',
				height: 1,
				offsetX: 0,
				offsetY: 0
			},
			labels: {
				style: {
					colors: app.color.gray300,
					fontSize: '10px',
					fontFamily: app.font.family,
					fontWeight: app.font.weight,
					cssClass: 'apexcharts-xaxis-label',
				}
			}
		},
		yaxis: {
			labels: {
				style: {
					colors: app.color.gray300,
					fontSize: '10px',
					fontFamily: app.font.family,
					fontWeight: app.font.weight,
					cssClass: 'apexcharts-xaxis-label',
				}
			}
		}
	};

// 장기 미접속 자산 증가율
var dataFor150days = dataList['150days'];
var currentDataValue = parseValue(dataFor150days['current_value']);
var lastMonthDataValue = parseValue(dataFor150days['last_value_in_prev_month']);
var options150days = {
    chart: {
        type: 'bar',
        height: 200
    },
    series: [{
        name: '전월 자산 수',
        data: [lastMonthDataValue]
    }, {
        name: '현재 자산 수',
        data: [currentDataValue]
    }],
    xaxis: {
        categories: ['150days']
    }
}
var chart150days = new ApexCharts(document.querySelector("#chart-150days"), options150days);
chart150days.render();

// 업데이트 대상 수 변화량
var dataFor_osVersionUp = dataList['os_version_up'];
var currentDataValue = parseValue(dataFor_osVersionUp['current_value']);
var lastMonthDataValue = parseValue(dataFor_osVersionUp['last_value_in_prev_month']);
var options_osVersionUp = {
    chart: {
        type: 'bar',
        height: 200
    },
    series: [{
        name: '전월 자산 수',
        data: [lastMonthDataValue]
    }, {
        name: '현재 자산 수',
        data: [currentDataValue]
    }],
    xaxis: {
        categories: ['os_version_up']
    }
}
var chart_os_version_up = new ApexCharts(document.querySelector("#chart_os_version_up"), options_osVersionUp);
chart_os_version_up.render();

// 보안 패치 대상 수 변화량
var dataFor_hotfix = dataList['hotfix'];
var currentDataValue_hotfix = parseValue(dataFor_hotfix['current_value']);
var lastMonthDataValue_hotfix = parseValue(dataFor_hotfix['last_value_in_prev_month']);
var options_hotfix = {
    chart: {
        type: 'bar',
        height: 200
    },
    series: [{
        name: '전월 자산 수',
        data: [lastMonthDataValue_hotfix]
    }, {
        name: '현재 자산 수',
        data: [currentDataValue_hotfix]
    }],
    xaxis: {
        categories: ['hotfix']
    }
}
var chart_hotfix = new ApexCharts(document.querySelector("#chart_hotfix"), options_hotfix);
chart_hotfix.render();

// 월간 자산 수 비교
var dataFor_Notebook = dataList['Notebook_chassis_total'];
var currentDataValue_Notebook = parseValue(dataFor_Notebook['current_value']);
var lastMonthDataValue_Notebook = parseValue(dataFor_Notebook['last_value_in_prev_month']);
var dataFor_Desktop = dataList['Desktop_chassis_total'];
var currentDataValue_Desktop = parseValue(dataFor_Desktop['current_value']);
var lastMonthDataValue_Desktop = parseValue(dataFor_Desktop['last_value_in_prev_month']);

var options_chassis = {
    chart: {
        type: 'bar',
        height: 250,
        stacked: false
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '50%',
            dataLabels: {
                position: 'top', // top, center, bottom
            },
        },
    },
    series: [{
        name: '전월 자산 수',
        data: [lastMonthDataValue_Notebook, lastMonthDataValue_Desktop]
    }, {
        name: '현재 자산 수',
        data: [currentDataValue_Notebook, currentDataValue_Desktop]
    }],
    xaxis: {
        categories: ['노트북', '데스크탑']
    }
}

var chart_chassis = new ApexCharts(document.querySelector("#chart_chassis"), options_chassis);
chart_chassis.render();

// Window 버전별 데이터를 테이블로 삽입
var winVerData = dataList['win_ver'];
var tableBody = document.getElementById('winVerTableBody');

for (var version in winVerData) {
    var row = tableBody.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.textContent = version;
    cell2.textContent = winVerData[version];
}v






};


/* Controller
------------------------------------------------ */
$(document).ready(function () {
	handleRenderdailyApexChart();

	$(document).on('theme-reload', function () {
		$('#dailyChart_deviceAsset, #dailyChart_deviceAsset1, #dailyChart_actionAsset, #dailyChart_completedAsset, #weeklyChart_usedCPU, #weeklyChart_usedMemory, #weeklyChart_usedDisk, #weeklyChart_usedSystem, #weeklyChart_usedSw1, #weeklyChart_usedSw2').empty();

		handleRenderWeeklyApexChart();
	});
});