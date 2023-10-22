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
        categories: ['']
    },
    dataLabels: {
        enabled: true, // 데이터 라벨 활성화
        style: {
            colors: ['#000000'] // 검정색으로 설정
        }
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
        categories: ['']
    },
    dataLabels: {
        enabled: true, // 데이터 라벨 활성화
        style: {
            colors: ['#000000'] // 검정색으로 설정
        }
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
        categories: ['']
    },
    dataLabels: {
        enabled: true, // 데이터 라벨 활성화
        style: {
            colors: ['#000000'] // 검정색으로 설정
        }
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
        height: 200,
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
    },
    dataLabels: {
        enabled: true, // 데이터 라벨 활성화
        style: {
            colors: ['#000000'] // 검정색으로 설정
        }
    }
}

var chart_chassis = new ApexCharts(document.querySelector("#chart_chassis"), options_chassis);
chart_chassis.render();

// Window 버전별 데이터를 테이블로 삽입
var winVerData = dataList['win_ver'];
var tableBody = document.getElementById('winVerTableBody');
console.log(winVerData)
for (var i = 0; i < winVerData.length; i++) { // 배열을 순회하기 위해 인덱스 기반의 for 문을 사용합니다.
    var row = tableBody.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.textContent = winVerData[i].item; // 'item' 속성의 값
    cell2.textContent = winVerData[i].current_value + '대'; // 'current_value' 속성의 값 또는 원하는 다른 속성
    cell3.textContent = winVerData[i].increase_amount  + '대';
    cell4.textContent = winVerData[i].increase_rate + '%';
}

};


var currentDate = new Date();
var formattedDate = currentDate.getFullYear() + '년 ' + (currentDate.getMonth() + 1).toString().padStart(2, '0') + '월 ' + currentDate.getDate().toString().padStart(2, '0') + '일 ' + currentDate.getHours().toString().padStart(2, '0') + '시';
document.querySelector(".daily-report-content-left ul li:nth-child(1) p:nth-child(2)").textContent = formattedDate;
var urlParams = new URLSearchParams(window.location.search);
var datetimeValue = urlParams.get('datetime');
if (datetimeValue) {
    var parts = datetimeValue.split('-');
    var selected_date = parts[0] + '년 ' + parts[1] + '월 ' + parts[2] + '일 ' + parts[3] + '시';
    document.querySelector(".daily-report-content-left ul li:nth-child(2) p:nth-child(2)").textContent = selected_date;
} else {
    document.querySelector(".daily-report-content-left ul li:nth-child(2) p:nth-child(2)").textContent = "datetime 값이 없습니다.";
}



/* Controller
------------------------------------------------ */
$(document).ready(function () {
	handleRenderdailyApexChart();

	$(document).on('theme-reload', function () {
		$('#dailyChart_deviceAsset, #dailyChart_deviceAsset1, #dailyChart_actionAsset, #dailyChart_completedAsset, #weeklyChart_usedCPU, #weeklyChart_usedMemory, #weeklyChart_usedDisk, #weeklyChart_usedSystem, #weeklyChart_usedSw1, #weeklyChart_usedSw2').empty();

		handleRenderWeeklyApexChart();
	});
});