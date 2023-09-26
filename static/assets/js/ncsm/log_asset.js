/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/



// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};

var log_popupTable_list = function () {
    var log_popupTable_data = $('#log_popupTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
		lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
		pageLength: 10,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,
		order : [
		    [2, "desc"]
		],
		drawCallback: function (settings) {
                // 페이지 변경시 체크박스 값을 설정합니다.
            var api = this.api();
            var rows = api.rows({ page: 'current' }).nodes();

            var current_page_sec = log_popupTable_data.page();
            var total_pages_sec = log_popupTable_data.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages_sec > 10){ // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
            $('<button type="button" class="btn" id="nexts_sec">10≫</button>')
            .insertAfter('#sec_asset_list_paginate .paginate_button:last');
            $('<button type="button" class="btn" id="after_sec">≪10</button>')
            .insertBefore('#sec_asset_list_paginate .paginate_button:first');
            }
        },
		ajax: {
			url: 'paging/',
			type: "POST",
            data: function (data) {
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                        0: 'id',
                        1: 'log_func',
                        2: 'log_item',
                        3: 'log_result',
                        4: 'log_user',
                        5: 'log_date'
                        };
                // console.log(columnMap)
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
		},

		columns: [
            { data: '', title: 'No', searchable: true },
			{ data: 'log_func', title: '기능 이름', searchable: true },
            { data: 'log_item', title: '항목 이름', searchable: true },
			{ data: 'log_result', title: '결과', searchable: true },
			{ data: 'log_user', title: '유저', searchable: true },
			{ data: 'log_date', title: '시간', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
		columnDefs: [
            {targets: 0, width: "3%",orderable: false, searchable:false, className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 1, width: "5%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.log_func+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "20%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.log_item+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "5%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.log_result+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.log_user+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.log_date+'" data-toggle="tooltip">'+data+'</span>'}},
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
});


	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = log_popupTable_data.page();
        var total_pages_sec = log_popupTable_data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
                if (current_page_sec + 10 < total_pages_sec) {
                    log_popupTable_data.page(current_page_sec + 10).draw('page');
                } else {
                    log_popupTable_data.page(total_pages_sec - 1).draw('page');
                }
                } else {
                    log_popupTable_data.page(Math.max(current_page_sec - 10, 0)).draw('page');
                }
});
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};

$(document).ready(function () {
    user_list_popup();
    log_popupTable_list();
    // checkbox_check($('#sec_asset_list tbody'))
    //initializeDataTable();
});


