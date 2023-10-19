///*
//Template Name: HUD - Responsive Bootstrap 5 Admin Template
//Version: 1.8.0
//Author: Sean Ngu
//
//*/
//
//var handleRenderReportTableData = function () {
//	var reportTable = $('#reportDailyTable, #reportWeeklyTable, #reportMonthlyTable').DataTable({
//		destroy: true,
//		dom: "<'row mb-3'<'col-md-4 mb-3 mb-md-0'l><'col-md-8 text-right'<'d-flex justify-content-end'fB>>>t<'row align-items-center'<'mr-auto col-md-6 mb-3 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [10, 20, 30, 40, 50],
//		responsive: true,
//		searching: true,
//		language: {
//			"decimal": "",
//			"info": "현재 _START_ - _END_건 / 전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//	});
//};
//
//var handleRenderWeakTableData = function () {
//	var weakTable = $('#weakTable-windows, #weakTable-unix').DataTable({
//		dom: "<'row mb-3'<'col-md-4 mb-3 mb-md-0'l><'col-md-8 text-right'<'d-flex justify-content-end'fB>>>t<'row align-items-center'<'mr-auto col-md-6 mb-3 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [10, 20, 30, 40, 50],
//		responsive: true,
//		destroy : true,
//		searching: true,
//		autoWidth: false,
//		ordering: false,
//		columnDefs: [
//            { width: "2%", target: [0] },
//            { width: "4%", target: [1] },
//            { width: "20%", target: [2] },
//            { width: "66%", target: [3] },
//            { width: "3%", target: [4] },
//            { width: "4%", target: [5] }
//		],
//		language: {
//			"decimal": "",
//			"info": "현재 _START_ - _END_건 / 전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//	});
//};
//
//var handleRenderWeakDetailTableData = function () {
//
//	var url = (window.location.search).split('&');
//    var swv = url[0].substr(url[0].indexOf("=") + 1);
//    var count = url[1].substr(url[1].indexOf("=") + 1);
//	var weakDetailtable = $('#weakTableDetail').DataTable({
//		dom: "<'row mb-3'<'col-md-4 mb-3 mb-md-0'l><'col-md-8 text-right'<'d-flex justify-content-end'fB>>>t<'row align-items-center'<'mr-auto col-md-6 mb-3 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [10, 20, 30, 40, 50],
//		responsive: true,
//		searching: true,
//		autoWidth: false,
//		ordering: false,
//		serverSide: true,
//		processing: true,
//		ajax: {
//			url: './paging?swv=' + swv + '&count=' + count,
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				console.log(data);
//                return data;
//			},
//			// dataFilter: function (data) {
//			// 	var json = jQuery.parseJSON(data);
//			// 	console.log(json);
//			// 	console.log(data);
//			// 	json.recordsTotal = 10;
//			// 	json.recordsFiltered = 42;
//			// 	json.data = json.list;
//
//			// 	return JSON.stringify(json);
//			// }
//		},
//		columns: [
//			{data : 'index'},
//			{data : 'cid'},
//			{data : 'cpnm'},
//			{data : 'os'},
//			{data : 'ip'},
//			{data : 'type'},
//			{data : 'last_login'},
//			{data : 'index'},
//		],
//		columnDefs: [
//			{ width: "5%", target: [0] },
//			{ width: "15%", target: [1] },
//			{ width: "16%", target: [2] },
//			{ width: "20%", target: [3] },
//			{ width: "14%", target: [4] },
//			{ width: "10%", target: [5] },
//			{ width: "15%", target: [6] },
//			{
//				width: "5%", target: [7],
//				render: function (data, type, full, meta) {
//					return '<i class="caret" onclick="caret_event();"></i>';
//				}
//			}
//		],
//		language: {
//			"decimal": "",
//			"info": "현재 _START_ - _END_건 / 전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//	});
//};
//
//var handleRenderWeakDetailModalTableData = function () {
//	var weakDetailModaltable = $('#weakTableDetail_modal').DataTable({
//		dom: "<'row mb-3'<'col-md-4 mb-3 mb-md-0'l><'col-md-8 text-right'<'d-flex justify-content-end'fB>>>t<'row align-items-center'<'mr-auto col-md-6 mb-3 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [10, 20, 30, 40, 50],
//		responsive: true,
//		searching: true,
//		autoWidth: false,
//		ordering: false,
//		columnDefs: [
//			{ width: "5%", target: [0] },
//			{ width: "85%", target: [1] },
//			{ width: "5%", target: [2] },
//			{ width: "5%", target: [3] },
//		],
//		language: {
//			"info": "현재 _START_ - _END_건 / 전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//	});
//
//	$("#weakTableDetail_modal_filter.dataTables_filter").append($("#weak-box"));
//
//	var categoryIndex = 0;
//	$("#weakTableDetail_modal th").each(function (i) {
//		if ($($(this)).html() == "상태") {
//			categoryIndex = i; return false;
//		}
//	});
//	$.fn.dataTable.ext.search.push(
//		function (settings, data, dataIndex) {
//			var selectedItem = $('#weak-box').val()
//			var category = data[categoryIndex];
//			if (selectedItem === "" || category.includes(selectedItem)) {
//				return true;
//			}
//			return false;
//		}
//	);
//
//	$("#weak-box").change(function (e) {
//		weakDetailModaltable.draw();
//	});
//	weakDetailModaltable.draw();
//};
//
//var OshandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#OsDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'name'},
//			{data: 'count'},
//
//		],
//		columnDefs : [
//		    {targets: 0, width: "10%", className: 'text-center'},
//		    {targets: 1, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "20%", className: 'text-center'}
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//		drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#OsDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#OsDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//	});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//    });
//
//    $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var serverhandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#serverBandBydashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'name'},
//			{data: 'count'},
//		],
//		columnDefs: [
//		    {targets: 0, width: "10%", className: 'text-center'},
//		    {targets: 1, width: "70%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "20%", className: 'text-center'}
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#serverBandBydashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#serverBandBydashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//	});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//    });
//
//    $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var runningServicehandleRenderDashboardPopupTableData = function (url) {
//    var pagingValue = url;
//	var dashboardpopupTable = $('#runningServiceDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		autoWidth: true,
//		ajax: {
//			url: pagingValue ,
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'name'},
//			{data: 'count'},
//		],
//		columnDefs: [
//		    {targets: 0, width: "10%", className: 'text-center'},
//		    {targets: 1, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "20%", className: 'text-center'}
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//        pagingType: 'numbers',//이전 다음 버튼 히든처리
//
//        //페이징 10칸식 이동 로직
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){ // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#runningServiceDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#runningServiceDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var physicalServerhandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#physicalServerDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'name'},
//			{data: 'count'},
//		],
//		columnDefs: [
//		    {targets: 0, width: "10%", className: 'text-center'},
//		    {targets: 1, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "20%", className: 'text-center'}
//
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//
//	drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#physicalServerDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#physicalServerDashboard-popupTable_paginate .paginate_button:first');
//             }
//        }
//
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//
//
//
//var idleAssetHandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#idleDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'computer_name'},
//			{data: 'chassis_type'},
//			{data: 'ipv_address'},
//			{data: 'disk_total_used_space'},
//			{data: 'last_logged_in_date'},
//
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "20%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "20%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.chassis_type+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "20%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ipv_address+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 4, width: "15%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.disk_total_used_space+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 5, width: "15%", className: 'text-center'},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//        pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#idleDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#idleDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//};
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//var gpuServerhandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#gpuServerDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'ip'},
//			{data: 'name'},
//			{data: 'model'},
//			{data: 'count'},
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "20%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "30%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "28%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.model+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 4, width: "12%", className: 'text-center'},
//
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//        pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#gpuServerDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#gpuServerDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var handleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#MemoryDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data : 'index'},
//			{data : 'ip'},
//			{data : 'name'},
//			{data : 'use'},
//			{data : 'total'},
//			{data : 'usage'},
//			{data : 'index'}
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "15%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "35%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "12%", className: 'text-center'},
//            {targets: 4, width: "12%", className: 'text-center'},
//            {targets: 5, width: "12%", className: 'text-center'},
//            {targets: 6, width: "14%", render: function(data, type, row) {return '<select class="btn btn-outline-primary" onchange="confirm(this.options[this.selectedIndex].value)"><option value="" selected disabled>Action</option><option value="메일을 보내시겠습니까?">Mail</option><option value="알람을 보내시겠습니까?">Alarm</option><option value="정말로 리부팅을 실행시키겠습니까?">Reboot</option></select>'}},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//	    pagingType: 'numbers',
//
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#MemoryDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#MemoryDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var CpuhandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#CpuDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'ip'},
//			{data: 'name'},
//			{data: 'use'},
//			{data: 'usage'},
//			{data: 'index'},
//
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "20%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "34%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "13%", className: 'text-center'},
//            {targets: 4, width: "9%", className: 'text-center'},
//            {targets: 5, width: "14%", render: function(data, type, row) {return '<select class="btn btn-outline-primary" onchange="confirm(this.options[this.selectedIndex].value)"><option value="" selected disabled>Action</option><option value="메일을 보내시겠습니까?">Mail</option><option value="알람을 보내시겠습니까?">Alarm</option><option value="정말로 리부팅을 실행시키겠습니까?">Reboot</option></select>'}},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//        pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#CpuDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#CpuDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var DiskhandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#DiskDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data : 'index'},
//			{data : 'ip'},
//			{data : 'name'},
//			{data : 'use'},
//			{data : 'total'},
//			{data : 'usage'},
//			{data : 'index'},
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "15%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "35%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "12%", className: 'text-center'},
//            {targets: 4, width: "12%", className: 'text-center'},
//            {targets: 5, width: "12%", className: 'text-center'},
//            {targets: 6, width: "14%", render: function(data, type, row) {return '<select class="btn btn-outline-primary" onchange="confirm(this.options[this.selectedIndex].value)"><option value="" selected disabled>Action</option><option value="메일을 보내시겠습니까?">Mail</option><option value="알람을 보내시겠습니까?">Alarm</option><option value="정말로 리부팅을 실행시키겠습니까?">Reboot</option></select>'}},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//		pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#DiskDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#DiskDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var alarmCasehandleRenderDashboardPopupTableData = function () {
//	var dashboardpopupTable = $('#alarmCaseDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//
//		columns: [
//			{data: 'index'},
//			{data: 'ip'},
//			{data: 'name'},
//			{data: 'ramusage'},
//			{data: 'cpuusage'},
//			{data: 'driveusage'},
//			{data: 'date'},
//			{data: 'index',
//            className: 'select-checkbox',
//            orderable: false}
//		],
//		columnDefs: [
//            {targets: 0, width: "4%", className: 'text-center'},
//            {targets: 1, width: "13%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "20%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "12%", className: 'text-center'},
//            {targets: 4, width: "11%", className: 'text-center'},
//            {targets: 5, width: "12%", className: 'text-center'},
//            {targets: 6, width: "11%", className: 'text-center'},
//            {targets: 7, width: "11%", render: function(data, type, row) {
//            return `<select class="btn btn-outline-primary" onchange="sendAction(this,\'`+row.ip+`\',\'`+row.name+`\',\'`+row.ramusage+`\',\'`+row.cpuusage+`\',\'`+row.driveusage+`\',\'`+row.date+`\')">
//                    <option value="">Action</option>
//                    <option value="mail">Mail</option>
//                    <option value="">Alarm</option>
//                    <option value="">Off Process</option>
//                    <option value="">Service Restart</option>
//                    <option value="">Isolation</option>
//                    <option value="reboot">Reboot</option>
//
//                    </select>`}},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//		pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#alarmCaseDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#alarmCaseDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
////-------------------connectDestinationIp_--- 종윤---------------------------
//
//var connectDestinationIphandleRenderDashboardPopupTableData = function () {
//
//	var dashboardpopupTable = $('#connectDestinationIpDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//
//		ajax: {
//
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//
//
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'ip'},
//			{data: 'name'},
//			{data: 'port'},
//			{data: 'count'},
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "30%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "30%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "20%", className: 'text-center', render: function(data, type, row) {return '<span title="'+row.port+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 4, width: "10%", className: 'text-center'},
//
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//
//	});
//};
//var connectSourceIphandleRenderDashboardPopupTableData = function () {
//
//	var dashboardpopupTable = $('#connectSourceIpDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//
//		ajax: {
//
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//
//                print(res)
//			}
//		},
//		columns: [
//			{data: 'index'},
//			{data: 'ip'},
//			{data: 'name'},
//			{data: 'count'},
//		],
//		columnDefs: [
//            {targets: 0, width: "10%", className: 'text-center'},
//            {targets: 1, width: "35%", className: 'text-center text-truncate', render: function(data, type, row) {return '<span title="'+row.ip+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 2, width: "35%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.name+'" data-toggle="tooltip">'+data+'</span>'}},
//            {targets: 3, width: "10%", className: 'text-center'},
//
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//		},
//        		pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#connectSourceIpDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#connectSourceIpDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//var certHandleRenderDashboardPopupTableData = function () {
//
//	var dashboardpopupTable = $('#certDashboard-popupTable').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//
//		responsive: true,
//		searching: true,
//		ordering: false,
//		serverSide: true,
//		displayLength: false,
//
//		ajax: {
//			url: 'paging/',
//			type: "POST",
//			dataSrc: function (res) {
//				var data = res.data.item;
//				return data;
//			}
//		},
//		columns: [
//			{data: 'crt_name'},
//			{data: 'crt_expire_date'},
//		],
//		columnDefs: [
//		    {targets: 0, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.crt_name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 1, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.crt_expire_date+'" data-toggle="tooltip">'+data+'</span>'}},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//			"paginate": {
//				"first": "처음",
//				"last": "끝",
//				"next": "다음",
//				"previous": "이전"
//			},
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//},
//        		pagingType: 'numbers',
//
//        drawCallback: function() {
//            var current_page = dashboardpopupTable.page();
//            var total_pages = dashboardpopupTable.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages > 10){
//            $('<button type="button" class="btn" id="nexts">10≫</button>')
//            .insertAfter('#certDashboard-popupTable_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after">≪10</button>')
//            .insertBefore('#certDashboard-popupTable_paginate .paginate_button:first');
//            }
//        }
//});
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = dashboardpopupTable.page();
//        var total_pages = dashboardpopupTable.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    dashboardpopupTable.page(current_page + 10).draw('page');
//                } else {
//                    dashboardpopupTable.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});
//        $(document).ready(function() {
//        var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//        $('head').append(customStyle);
//});
//};
//
//
//
///* Controller weakBoxs
//------------------------------------------------ */
//$(document).ready(function () {
//
//    if ($("#reportDailyTable, #reportWeeklyTable, #reportMonthlyTable").length > 0) {
//
//        handleRenderReportTableData();
//
//    }else if ($("#weakTable-windows, #weakTable-unix").length > 0) {
//
//        handleRenderWeakTableData();
//
//    }else if ($("#weakTableDetail").length > 0) {
//
//        handleRenderWeakDetailTableData();
//
//    }else if ($("#weakTableDetail_modal").length > 0) {
//
//        handleRenderWeakDetailModalTableData();
//
//    }else if($("#OsDashboard-popupTable").length > 0){
//
//		OshandleRenderDashboardPopupTableData();
//	}else if($("#serverBandBydashboard-popupTable").length > 0){
//
//		serverhandleRenderDashboardPopupTableData();
//	}else if($("#runningServiceDashboard-popupTable").length > 0){
//	    runningServicehandleRenderDashboardPopupTableData("paging/");
//	    var checkbox = document.getElementById("check_btn");
//            checkbox.addEventListener("change", function() {
//              if (checkbox.checked) {
//                $('#runningServiceDashboard-popupTable').DataTable().destroy();
//                runningServicehandleRenderDashboardPopupTableData("paging/");
//              } else {
//                $('#runningServiceDashboard-popupTable').DataTable().destroy();
//                runningServicehandleRenderDashboardPopupTableData("paging2/");
//              }
//            });
//
//	}else if($("#physicalServerDashboard-popupTable").length > 0){
//
//		physicalServerhandleRenderDashboardPopupTableData();
//	}else if($("#gpuServerDashboard-popupTable").length > 0){
//
//		gpuServerhandleRenderDashboardPopupTableData();
//	}else if($("#alarmCaseDashboard-popupTable").length > 0){
//
//		alarmCasehandleRenderDashboardPopupTableData();
//	}else if ($("#MemoryDashboard-popupTable").length > 0) {
//
//        handleRenderDashboardPopupTableData();
//	}else if ($("#CpuDashboard-popupTable").length > 0) {
//
//		CpuhandleRenderDashboardPopupTableData();
//    }else if($("#DiskDashboard-popupTable").length > 0){
//
//		DiskhandleRenderDashboardPopupTableData();
////----------------------------ip 더보기 종윤--------------------------
//	}else if($("#connectDestinationIpDashboard-popupTable").length > 0){
//    	connectDestinationIphandleRenderDashboardPopupTableData();
//	}else if($("#connectSourceIpDashboard-popupTable").length > 0){
//    	connectSourceIphandleRenderDashboardPopupTableData();
////----------------------------대시보드 하단 인증서 더보기 ---------------
//    }else if($("#certDashboard-popupTable").length > 0){
//        certHandleRenderDashboardPopupTableData();
//    }else if ($("#idleDashboard-popupTable").length > 0) {
//        idleAssetHandleRenderDashboardPopupTableData();
//        };
//});

var hw_asset_list = function () {
	var hs_asset_list_Data = $('#hs_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
		lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
		pageLength: 10,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,

		ajax: {
			url: 'hwpaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                            1: 'chassistype',
                            2: 'dep',
                            3: 'name',
                            4: 'logged_name',
                            5: 'computer_name',
                            6: 'ip_address',
                            7: 'mac_address',
                            8: 'memo'

                        };
                data.filter = {
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input-hs').val(),
                    value2 : $('#hs_asset_list_filter input[type="search"]').val(),
                    regex : false, // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
			dataSrc: function (res) {
				var data = res.data;
				console.log(data)

				return data;
			}
		},

		columns: [
            { data: '', title: 'No', searchable: true },
//			{ data: 'chassistype', title: '구분', searchable: true },
			{ data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{ data: 'ncdb_data.userName', title: '이름', searchable: true },
			{ data: 'ncdb_data.userId', title: '계정', searchable: true },
			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
            { data: 'ip_address', title: 'IPv4' , searchable: true},
            { data: 'mac_address', title: 'MAC' , searchable: true},
			{ data: 'hw', title: '하드웨어 목록', searchable: true },
//			{ data: 'hw_mb', title: 'Mainboard', searchable: true },
//			{ data: 'hw_ram', title: 'RAM', searchable: true },
//			{ data: 'hw_disk', title: 'DISK', searchable: true },
//			{ data: 'hw_gpu', title: 'VGA', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
//        columnDefs: [
//		    {targets: 0, width: "10%", className: 'text-start text-truncate'},
//		    {targets: 1, width: "20%", className: 'text-start text-truncate'},
//		    {targets: 2, width: "10%", className: 'text-start text-truncate'},
//            {targets: 3, width: "10%", className: 'text-start text-truncate'},
//		    {targets: 4, width: "40%", className: 'text-start text-truncate'},
//		    {targets: 5, width: "10%", className: 'text-start text-truncate'},
//		],
//		columnDefs: [
//            {targets: 0, width: "3%", orderable: false, searchable: false, className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 1, width: "3%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.chassistype+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 3, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.logged_name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 4, width: "5%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 5, width: "10%", className: 'text-center new-text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_cpu+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 6, width: "5%", className: 'text-center new-text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_mb+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 7, width: "3%", className: 'text-center new-text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_ram+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 8, width: "10%", className: 'text-center new-text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_disk+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 9, width: "10%", className: 'text-center new-text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_gpu+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 10, width: "5%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
//                if (data === null || data === undefined || data.trim() === '') { return '';
//                } else {return '<span title="' + row.memo + '" data-toggle="tooltip">' + data + '</span>';}}},
//		],
		columnDefs: [
            {targets: 0, width: "5%", orderable: false, searchable: false, className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 1, width: "15%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ncdb_data.deptName+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ncdb_data.userName+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ncdb_data.userId+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.mac_address+'" data-toggle="tooltip">'+data+'</span>'}},
            {targets: 7, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_name = row.computer_name;
		        const hw_cpu = row.hw_cpu;
                const hw_mb = row.hw_mb;
                const hw_ram = row.hw_ram;
                const hw_disk = row.hw_disk;
                const hw_gpu = row.hw_gpu;
		        return '<span data-toggle="tooltip"></span><div class="hwmore swmore-font text-center new-text-truncate flex-cloumn align-middle " data-hw_cpu="' + hw_cpu + '" data-hw_mb="' + hw_mb + '"  data-hw_ram="' + hw_ram + '"  data-hw_disk="' + hw_disk + '"  data-hw_gpu="' + hw_gpu + '"data-computer_name="' + computer_name +'">더보기...</div>'}},
		    {targets: 8, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
                if (data === null || data === undefined || data.trim() === '') { return '';
                } else {return '<span title="' + row.memo + '" data-toggle="tooltip">' + data + '</span>';}}},
		],
		language: {
			"decimal": "",
			"info": "전체 _TOTAL_건",
			"infoEmpty": "데이터가 없습니다.",
			"emptyTable": "데이터가 없습니다.",
			"thousands": ",",
			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
			"loadingRecords": "로딩 중입니다.",
			"processing": "",
			"zeroRecords": "검색 결과 없음",
			"paginate": {
				"first": "처음",
				"last": "끝",
				"next": "다음",
				"previous": "이전"
			},
			"search": "검색:",
			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
			"infoPostFix": "",
            },
            pagingType: 'numbers',//이전 다음 버튼 히든처리

            //페이징 10칸식 이동 로직
            drawCallback: function() {
                var current_page_hw = hs_asset_list_Data.page();
                var total_pages_hw = hs_asset_list_Data.page.info().pages;
                $('#nexts').remove();
                $('#after').remove();

                if (total_pages_hw > 10){ // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
                $('<button type="button" class="btn" id="nexts_hw">10≫</button>')
                .insertAfter('#hs_asset_list_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after_hw">≪10</button>')
                .insertBefore('#hs_asset_list_paginate .paginate_button:first');
                }
            }
});
      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
      $('.dropdown-menu a').click(function() {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
      });

  // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
$('#search-button-hs').click(function() {
    var column = $('#column-dropdown').data('column');
    var searchValue = $('#search-input-hs').val().trim();

    performSearch(column, searchValue, hs_asset_list_Data)
});

$('#search-input-hs').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-hs').val().trim();

            performSearch(column, searchValue, hs_asset_list_Data);
        }
    });

	$(document).on('click', '#nexts_hw, #after_hw', function() {
        var current_page_hw = hs_asset_list_Data.page();
        var total_pages_hw = hs_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_hw') {
                if (current_page_hw + 10 < total_pages_hw) {
                    hs_asset_list_Data.page(current_page_hw + 10).draw('page');
                } else {
                    hs_asset_list_Data.page(total_pages_hw - 1).draw('page');
                }
                } else {
                    hs_asset_list_Data.page(Math.max(current_page_hw - 10, 0)).draw('page');
                }
});
    var customStyle = '<style>#nexts_hw, #after_hw {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var sw_asset_list = function () {
	var sw_asset_list_Data = $('#hs_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><''p>>",
		lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,


		ajax: {
			url: 'swpaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                            1: 'chassistype',
                            2: 'dep',
                            3: 'name',
                            4: 'logged_name',
                            5: 'computer_name',
                            6: 'ip_address',
                            7: 'mac_address',
                            8: 'memo'

                        };
                data.filter = {
                    column: column,
                    value : $('#search-input-hs').val(),
                    value2 : $('#hs_asset_list_filter input[type="search"]').val(),
                    regex : false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
			dataSrc: function (res) {
				var data = res.data;
				return data;
			}
		},

//		columns: [
//		    { data: '', title: 'No', searchable: true },
//			{ data: 'chassistype', title: '구분', searchable: true },
//			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
//			{ data: 'logged_name', title: '사용자', searchable: true },
//            { data: 'ip_address', title: 'IPv4' , searchable: true},
//			{ data: 'sw_list', title: '소프트웨어 목록', searchable: true },
//			{ data: 'memo', title: '메모', searchable: true },
//
//		],
        columns: [
            { data: '', title: 'No', searchable: true },
//			{ data: 'chassistype', title: '구분', searchable: true },
			{ data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{ data: 'ncdb_data.userName', title: '이름', searchable: true },
			{ data: 'ncdb_data.userId', title: '계정', searchable: true },
			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
            { data: 'ip_address', title: 'IPv4' , searchable: true},
            { data: 'mac_address', title: 'MAC' , searchable: true},
            { data: 'sw', title: '소프트웨어 목록', searchable: true },
    //			{ data: 'hw_mb', title: 'Mainboard', searchable: true },
    //			{ data: 'hw_ram', title: 'RAM', searchable: true },
    //			{ data: 'hw_disk', title: 'DISK', searchable: true },
    //			{ data: 'hw_gpu', title: 'VGA', searchable: true },
            { data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
//        columnDefs: [
//		    {targets: 0, width: "10%", className: 'text-start text-truncate'},
//		    {targets: 1, width: "20%", className: 'text-start text-truncate'},
//		    {targets: 2, width: "10%", className: 'text-start text-truncate'},
//            {targets: 3, width: "10%", className: 'text-start text-truncate'},
//		    {targets: 4, width: "40%", className: 'text-start text-truncate'},
//		    {targets: 5, width: "10%", className: 'text-start text-truncate'},
//		],
		columnDefs: [
            {targets: 0, width: "5%", orderable: false, searchable: false, className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 1, width: "15%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ncdb_data.deptName+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ncdb_data.userName+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ncdb_data.userId+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.mac_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_name = row.computer_name;
		        const swList = row.sw_list;
                const swVer = row.sw_ver_list;
		        return '<span data-toggle="tooltip"></span><div class="swmore swmore-font align-middle text-center " data-swlist="' + swList + '" data-swver="' + swVer + '" data-computer_name="' + computer_name +'">더보기...</div>'}},
		    {targets: 8, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
                if (data === null || data === undefined || data.trim() === '') { return '';
                } else {return '<span title="' + row.memo + '" data-toggle="tooltip">' + data + '</span>';}}},
		],
		language: {
			"decimal": "",
			"info": "전체 _TOTAL_건",
			"infoEmpty": "데이터가 없습니다.",
			"emptyTable": "데이터가 없습니다.",
			"thousands": ",",
			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
			"loadingRecords": "로딩 중입니다.",
			"processing": "",
			"zeroRecords": "검색 결과 없음",
			"paginate": {
				"first": "처음",
				"last": "끝",
				"next": "다음",
				"previous": "이전"
			},
			"search": "검색:",
			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
			"infoPostFix": "",
            },
            pagingType: 'numbers',//이전 다음 버튼 히든처리

            //페이징 10칸식 이동 로직
            drawCallback: function() {
                var current_page_sw = sw_asset_list_Data.page();
                var total_pages_sw = sw_asset_list_Data.page.info().pages;
                $('#nexts').remove();
                $('#after').remove();

                if (total_pages_sw > 10){ // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
                $('<button type="button" class="btn" id="nexts_sw">10≫</button>')
                .insertAfter('#hs_asset_list_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after_sw">≪10</button>')
                .insertBefore('#hs_asset_list_paginate .paginate_button:first');
                }
            }
});

      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
      $('.dropdown-menu a').click(function() {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
      });

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-hs').click(function() {
    var column = $('#column-dropdown').data('column');
    var searchValue = $('#search-input-hs').val().trim();

    performSearch(column, searchValue, sw_asset_list_Data)
});

    $('#search-input-hs').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-hs').val().trim();

            performSearch(column, searchValue, sw_asset_list_Data);
        }
    });

	$(document).on('click', '#nexts_sw, #after_sw', function() {
        var current_page_sw = sw_asset_list_Data.page();
        var total_pages_sw = sw_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sw') {
                if (current_page_sw + 10 < total_pages_sw) {
                    sw_asset_list_Data.page(current_page_sw + 10).draw('page');
                } else {
                    sw_asset_list_Data.page(total_pages_sw - 1).draw('page');
                }
                } else {
                    sw_asset_list_Data.page(Math.max(current_page_sw - 10, 0)).draw('page');
                }
});
    var customStyle = '<style>#nexts_sw, #after_sw {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};



function hwbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>No</th><th>부서</th><th>이름</th><th>계정</th><th>컴퓨터 이름</th><th>IPv4</th><th>MAC</th><th>하드웨어 목록</th><th>memo</th></tr></thead><tbody></tbody>';
    $('#hs_asset_list').DataTable().destroy();
    $('#hs_asset_list').html(newTableContent);
    hw_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');

}

function swbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>No</th><th>부서</th><th>이름</th><th>계정</th><th>컴퓨터 이름</th><th>IPv4</th><th>MAC</th><th>소프트웨어 목록</th><th>memo</th></tr></thead><tbody></tbody>';
    $('#hs_asset_list').DataTable().destroy();
    $('#hs_asset_list').html(newTableContent);
    sw_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');

}

$(document).ready(function () {
    user_list_popup();
    hw_asset_list();
    //sidebar();
    //initEvent();

});






//$('html').click(function(e){
//const appElement = document.getElementById('app');
//        var sidebar = $('#sidebar');
//        var app = $('#app');
//    	if(!$(e.target).hasClass('app-sidebar-content') && !$(e.target).hasClass('menu-toggler') && !$(e.target).hasClass('app-sidebar')){
//            sidebar.css({'display':'none'});
//            app.removeClass("app-sidebar-toggled");
//            app.addClass("app-sidebar-collapsed");
//        }
//        else{
//            sidebar.css({'display':'block'});
//        }
//    });

$(document).on("click",".swmore", function (e){
    const computer_name = $(this).data("computer_name");
    const swList = $(this).data("swlist");
    const swVer = $(this).data("swver");
    swList2 = swList.split('<br>')
    swVer2 = swVer.split('<br>')
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
    const combinedData = swList2.map((item, index) => [item, swVer2[index]]);

    // Generate the table HTML
    const tableHTML = combinedData.map(([item, version]) => `
        <tr>
            <td scope="row">${item}</td>
            <td>${version}</td>
        </tr>
    `).join('');



    //console.log(swVer[1]);
    // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
    $("#swListModal .modal-title").html(computer_name+"의 소프트웨어 및 버전");
    $("#swListModal .hstbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#swListModal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
        if (searchValue === "") {
            $("#swListModal .hstbody tr").removeClass("highlight");
            return;
        };
        $("#swListModal .hstbody tr").each(function () {
            const rowData = $(this).text().toLowerCase();
            // 검색어가 rowData에 포함되면 highlight 클래스 추가
            if (rowData.includes(searchValue)) {
                $(this).addClass("highlight");
            }
            // 포함되지 않으면 highlight 클래스 제거
            else {
                $(this).removeClass("highlight");
            }
        });
    });
});


$(document).on("click",".hwmore", function (e){
    const computer_name = $(this).data("computer_name");
    const hw_cpu = $(this).data("hw_cpu");
    const hw_mb = $(this).data("hw_mb");
    const hw_ram = $(this).data("hw_ram");
    const hw_disk = $(this).data("hw_disk");
    const hw_gpu = $(this).data("hw_gpu");
//    swList2 = swList.split('<br>')
//    swVer2 = swVer.split('<br>')
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
    //const combinedData = hw_cpu.map((item, index) => [item, hw_cpu[index]]);

    // Generate the table HTML
    const tableHTML = `
        <tr>
            <td class=text-center>CPU</td>
            <td class=text-center>${hw_cpu}</td>
        </tr>
        <tr>
            <td class=text-center>메인보드</td>
            <td class=text-center>${hw_mb}</td>
        </tr>
        <tr>
            <td class=text-center>RAM</td>
            <td class=text-center>${hw_ram}</td>
        </tr>
        <tr>
            <td class=text-center>디스크</td>
            <td class=text-center>${hw_disk}</td>
        </tr>
        <tr>
            <td class=text-center>그래픽카드</td>
            <td class=text-center>${hw_gpu}</td>
        </tr>

    `;



    //console.log(swVer[1]);
    // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
    $("#hwListModal .modal-title").html(computer_name+"의 하드웨어");
    $("#hwListModal .hstbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#hwListModal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
//    $("#searchInput2").on("input", function () {
//        const searchValue = $(this).val().trim().toLowerCase();
//        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
//        if (searchValue === "") {
//            $("#hwListModal .hstbody tr").removeClass("highlight");
//            return;
//        };
//        $("#hwListModal .hstbody tr").each(function () {
//            const rowData = $(this).text().toLowerCase();
//            // 검색어가 rowData에 포함되면 highlight 클래스 추가
//            if (rowData.includes(searchValue)) {
//                $(this).addClass("highlight");
//            }
//            // 포함되지 않으면 highlight 클래스 제거
//            else {
//                $(this).removeClass("highlight");
//            }
//        });
//    });
});