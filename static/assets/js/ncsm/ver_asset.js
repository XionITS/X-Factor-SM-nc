/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/



// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};


var all_asset_list = function () {
	var all_asset_list_Data = $('#ver_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
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

                // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
                for (var i = 0; i < rows.length; i++) {
                    var row = rows[i];
                    var data = api.row(row).data();
                    var computer_id = data.computer_id;

                    if (checkedItems[computer_id]) {
                        $(row).find('input[type="checkbox"]').prop('checked', true);
                    } else {
                        $(row).find('input[type="checkbox"]').prop('checked', false);
                    }
                }
            },
		ajax: {
			url: 'paging/',
			type: "POST",
            data: function (data) {
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                        2: 'computer_name',
                        3: 'ip_address',
                        4: 'os_total',
                        5: 'os_version',
                        6: 'os_build',
                        7: 'memo'
                        };
                data.filter = {
                    defaultColumn : defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input').val(),
                    value2 : $('#ver_asset_list_filter input[type="search"]').val(),
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

		columns: [
		    { data: '', title: '선택', searchable: false },
            { data: '', title: 'No', searchable: true },
            { data: 'computer_name', title: '컴퓨터 이름', searchable: true },
			{ data: 'ip_address', title: 'IPv4', searchable: true },
			{ data: 'os_total', title: 'OS', searchable: true },
            { data: 'os_version', title: '버전' , searchable: true},
			{ data: 'os_build', title: '빌드', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
        },
		columnDefs: [
		    {targets: 0, width: "4%", orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_id = row.computer_id;
		        return '<input type="checkbox" class="form-check-input" name="'+row.computer_name+'" id="'+computer_id+'" data-computer-id="'+ computer_id +'" data-computer-name="' + row.computer_name + '">'
		        }},
            {targets: 1, width: "4%",orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "13%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "8%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_total+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "17%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.os_version+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_build+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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

});

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

    // row 선택시 체크박스 체크 및 해제
    // checkbox_check();

    // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input').val().trim();

        if (searchValue !== '') {
            // If the search value is not empty, perform the new search
            all_asset_list_Data.columns().search('').draw();
            all_asset_list_Data.column(column).search(searchValue).draw();
        } else {

            initializeDataTable();
        }
    });


	$(document).on('click', '#nexts, #after', function() {
        var current_page = all_asset_list_Data.page();
        var total_pages = all_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    all_asset_list_Data.page(current_page + 10).draw('page');
                } else {
                    all_asset_list_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    all_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
                }
    });

};




var win_asset_list = function () {
	var win_asset_list_Data = $('#ver_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
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

                // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
                for (var i = 0; i < rows.length; i++) {
                    var row = rows[i];
                    var data = api.row(row).data();
                    var computer_id = data.computer_id;

                    if (checkedItems[computer_id]) {
                        $(row).find('input[type="checkbox"]').prop('checked', true);
                    } else {
                        $(row).find('input[type="checkbox"]').prop('checked', false);
                    }
                }
            },
		ajax: {
			url: 'paging/',
			type: "POST",
            data: function (data) {
                var defaultColumn = 'Windows'
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                        2: 'computer_name',
                        3: 'ip_address',
                        4: 'os_total',
                        5: 'os_version',
                        6: 'os_build',
                        7: 'memo'
                        };
                data.filter = {
                    defaultColumn : defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input').val(),
                    value2 : $('#ver_asset_list_filter input[type="search"]').val(),
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


		columns: [
		    { data: '', title: '선택', searchable: false },
            { data: '', title: 'No', searchable: true },
            { data: 'computer_name', title: '컴퓨터 이름', searchable: true },
			{ data: 'ip_address', title: 'IPv4', searchable: true },
			{ data: 'os_total', title: 'OS', searchable: true },
            { data: 'os_version', title: '버전' , searchable: true},
			{ data: 'os_build', title: '빌드', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
        },
		columnDefs: [
		    {targets: 0, width: "4%", orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_id = row.computer_id;
		        return '<input type="checkbox" class="form-check-input" name="'+computer_id+'" id="'+computer_id+'" data-computer-id="' + row.computer_id + '" data-computer-name="' + row.computer_name + '">'
		        }},
            {targets: 1, width: "4%",orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "13%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "8%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_total+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "17%", className: 'text-start text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.os_version+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_build+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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

});

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

    // row 선택시 체크박스 체크 및 해제
    // checkbox_check();

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input').val().trim();

        if (searchValue !== '') {
            // If the search value is not empty, perform the new search
            win_asset_list_Data.columns().search('').draw();
            win_asset_list_Data.column(column).search(searchValue).draw();
        } else {

            initializeDataTable();
        }
    });
	$(document).on('click', '#nexts, #after', function() {
        var current_page = win_asset_list_Data.page();
        var total_pages = win_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    win_asset_list_Data.page(current_page + 10).draw('page');
                } else {
                    win_asset_list_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    win_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
                }
});
};

var mac_asset_list = function () {
	var mac_asset_list_Data = $('#ver_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
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

                // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
                for (var i = 0; i < rows.length; i++) {
                    var row = rows[i];
                    var data = api.row(row).data();
                    var computer_id = data.computer_id;

                    if (checkedItems[computer_id]) {
                        $(row).find('input[type="checkbox"]').prop('checked', true);
                    } else {
                        $(row).find('input[type="checkbox"]').prop('checked', false);
                    }
                }
            },
		ajax: {
			url: 'paging/',
			type: "POST",
            data: function (data) {
                var defaultColumn = 'Mac'
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                        2: 'computer_name',
                        3: 'ip_address',
                        4: 'os_total',
                        5: 'os_version',
                        6: 'os_build',
                        7: 'memo'
                        };
                data.filter = {
                    defaultColumn : defaultColumn,
                    column: column,
                    value : $('#search-input').val(),
                    value2 : $('#ver_asset_list_filter input[type="search"]').val(),
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

		columns: [
		    { data: '', title: '선택', searchable: false },
            { data: '', title: 'No', searchable: true },
            { data: 'computer_name', title: '컴퓨터 이름', searchable: true },
			{ data: 'ip_address', title: 'IPv4', searchable: true },
			{ data: 'os_total', title: 'OS', searchable: true },
            { data: 'os_version', title: '버전' , searchable: true},
			{ data: 'os_build', title: '빌드', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
        },
		columnDefs: [
		    {targets: 0, width: "4%", orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_id = row.computer_id;
		        return '<input type="checkbox" class="form-check-input" name="'+computer_id+'" id="'+computer_id+'" data-computer-id="' + row.computer_id + '" data-computer-name="' + row.computer_name + '">'
		        }},
            {targets: 1, width: "4%",orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "13%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "8%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_total+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "17%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.os_version+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_build+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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

});

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

    // row 선택시 체크박스 체크 및 해제
    // checkbox_check();

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input').val().trim();

        if (searchValue !== '') {
            // If the search value is not empty, perform the new search
            mac_asset_list_Data.columns().search('').draw();
            mac_asset_list_Data.column(column).search(searchValue).draw();
        } else {

            initializeDataTable();
        }
    });
	$(document).on('click', '#nexts, #after', function() {
        var current_page = mac_asset_list_Data.page();
        var total_pages = mac_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    mac_asset_list_Data.page(current_page + 10).draw('page');
                } else {
                    mac_asset_list_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    mac_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
                }
});
};

var other_asset_list = function () {
	var other_asset_list_Data = $('#ver_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
		lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
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

                // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
                for (var i = 0; i < rows.length; i++) {
                    var row = rows[i];
                    var data = api.row(row).data();
                    var computer_id = data.computer_id;

                    if (checkedItems[computer_id]) {
                        $(row).find('input[type="checkbox"]').prop('checked', true);
                    } else {
                        $(row).find('input[type="checkbox"]').prop('checked', false);
                    }
                }
            },
		ajax: {
			url: 'paging/',
			type: "POST",
            data: function (data) {
                var defaultColumn = 'Linux'
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                        2: 'computer_name',
                        3: 'ip_address',
                        4: 'os_total',
                        5: 'os_version',
                        6: 'os_build',
                        7: 'memo'
                        };
                data.filter = {
                    defaultColumn : defaultColumn,
                    column: column,
                    value : $('#search-input').val(),
                    value2 : $('#ver_asset_list_filter input[type="search"]').val(),
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

		columns: [
		    { data: '', title: '선택', searchable: false },
            { data: '', title: 'No', searchable: true },
            { data: 'computer_name', title: '컴퓨터 이름', searchable: true },
			{ data: 'ip_address', title: 'IPv4', searchable: true },
			{ data: 'os_total', title: 'OS', searchable: true },
            { data: 'os_version', title: '버전' , searchable: true},
			{ data: 'os_build', title: '빌드', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
        },
		columnDefs: [
		    {targets: 0, width: "4%", orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_id = row.computer_id;
		        return '<input type="checkbox" class="form-check-input" name="'+computer_id+'" id="'+computer_id+'" data-computer-id="' + row.computer_id + '" data-computer-name="' + row.computer_name + '">'
		        }},
            {targets: 1, width: "4%",orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "13%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "8%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_total+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "17%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.os_version+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "22%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_build+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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

});

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

    // row 선택시 체크박스 체크 및 해제
    // checkbox_check();

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input').val().trim();

        if (searchValue !== '') {
            // If the search value is not empty, perform the new search
            other_asset_list_Data.columns().search('').draw();
            other_asset_list_Data.column(column).search(searchValue).draw();
        } else {

            initializeDataTable();
        }
    });
	$(document).on('click', '#nexts, #after', function() {
        var current_page = other_asset_list_Data.page();
        var total_pages = other_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    other_asset_list_Data.page(current_page + 10).draw('page');
                } else {
                    other_asset_list_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    other_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
                }
});
};


function allbutton(btn) {
    $('#ver_asset_list').DataTable().destroy();
    all_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
    checkedItems= {};
    checkedNames= {};
}

function winbutton(btn) {
    $('#ver_asset_list').DataTable().destroy();
    win_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
    checkedItems= {};
    checkedNames= {};
}

function macbutton(btn) {
    $('#ver_asset_list').DataTable().destroy();
    mac_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
    checkedItems= {};
    checkedNames= {};
}

function otherbutton(btn) {
    $('#ver_asset_list').DataTable().destroy();
    other_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
    checkedItems= {};
    checkedNames= {};
}

// function checkbox_check(){
//     $('#ver_asset_list tbody').off('click', 'tr');
//     $('#ver_asset_list tbody').on('click', 'tr', function () {
//         var checkbox = $(this).find('input[type="checkbox"]');
//         var hidden = $(this).find('input[type="hidden"]');
//         var computer_id = checkbox.attr('id');
//         console.log(computer_id)
//         var computer_name = hidden.attr("id");
//         checkbox.prop('checked', !checkbox.prop('checked'));
//         if (checkbox.prop('checked')) {
//             checkedItems[computer_id] = computer_name;
//         } else {
//             delete checkedItems[computer_id];
//         }
//     });
// }

// 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
function dropdown_text(){
    $('.dropdown-menu a').click(function() {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
    });
}

$(document).ready(function () {
    user_list_popup();
    all_asset_list();
    //sidebar();
    //initEvent();
    checkbox_check($('#ver_asset_list tbody'))

    //initializeDataTable();
});

//
//$(document).on("click","#creategroup", function (e){
//    $("#groupName").val("");
//    $("#groupDescription").val("");
//    const check_id = [];
//    const check_name = [];
//    var modalbody = "";
//    for (const computer_id in checkedItems) {
//        const computer_name = checkedItems[computer_id];
//        //modalbody += '<div><input type="hidden" name="'+computer_id+'" id="'+computer_id+'" value="'+computer_id+'">'+computer_name+'</div>'
//        //modalbody += '<input type="hidden" name="'+computer_name+'" id="'+computer_name+'" value="'+computer_name+'">'
//        //modalbody += '컴퓨터아이디'+computer_id + '<br/>';
//        //modalbody += '컴퓨터이름'+computer_name + '<br/>';
//        modalbody += '<input class="form-check-input" type="checkbox" value="'+computer_id+'" id="'+computer_id+'" computer-name="' + computer_name +'" checked><label class="form-check-label" for="'+computer_id+'">'+computer_name+'</label><br>'
//    }
//    $("#groupModal .modal-title").html("그룹 생성 팝업창");
//    $("#groupModal .form-check").html(modalbody);
//    $("#groupModal").modal("show");
//});
//
//
//$(document).on("click","#groupCreate", function(event) {
//    event.preventDefault(); // 기본 제출 동작을 막습니다.
//    // 폼 데이터를 가져옵니다.
//    var form = document.getElementById("GroupCreateForm");
//    var group_name = form.elements.groupName.value;
//    var group_description = form.elements.groupDescription.value;
//    let computerIds = []
//    let computerNames = []
//    const computerElements = $('#groupModal .form-check').find('.form-check-input');
//
//    computerElements.each(function () {
//        const computer_id = $(this).attr("id");
//        const computer_name = $(this).attr('computer-name');
//        computerIds.push(computer_id);
//        computerNames.push(computer_name);
//    });
//
//    $.ajax({
//    url: 'create/', // views.py 파일의 URL을 여기에 넣으세요.
//    type: 'POST',
//    dataType: 'json',
//    data:  {
//         'group_name' : group_name,
//         'group_description' : group_description,
//         'computerIds' : JSON.stringify(computerIds),
//         'computerNames' : JSON.stringify(computerNames),
//    },
//    data:  {
//         'group_name' : group_name,
//         'group_description' : group_description,
//         'computerIds' : JSON.stringify(computerIds),
//         'computerNames' : JSON.stringify(computerNames),
//    },
//    success: function (response) {
//    // response에 따른 처리 - 예: 경고창 띄우기
//        if (response.success == "success") {
//            alert(response.message);
//            $('#groupModal').modal('hide');
//        } else {
//            alert('실패 : ' + response.message);
//        }
//    }
//    });
//});

//document.getElementById("groupCreate").addEventListener("submit", function(event) {
//    console.log("11");
//    event.preventDefault(); // 폼의 실제 제출을 막습니다.
//
//    var form = event.target; // 이벤트가 발생한 폼 엘리먼트를 가져옵니다.
//    var group_name = form.elements.groupName.value;
//    var groupDescription = form.elements.groupDescription.value;
//
//    console.log(form);
//    console.log("Group Description:", groupDescription);
//});
    //var groupid
//    const computer_name = $(this).data("computer_name");
//    const swList = $(this).data("swlist");
//    const swVer = $(this).data("swver");
//    swList2 = swList.split('<br>')
//    swVer2 = swVer.split('<br>')
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const combinedData = swList2.map((item, index) => [item, swVer2[index]]);
//
//    // Generate the table HTML
//    const tableHTML = combinedData.map(([item, version]) => `
//        <tr>
//            <td scope="row">${item}</td>
//            <td>${version}</td>
//        </tr>
//    `).join('');
//
//
//
//    console.log(swList2);
//    console.log(swVer2);
//    //console.log(swVer[1]);
//    // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
//    $("#swListModal .modal-title").html(computer_name+"의 소프트웨어 및 버전");
//    $("#swListModal .hstbody").html(tableHTML);
//    //$("#swListModal .modal-body-2").html(swVerHTML);
//    $("#swListModal").modal("show");
//
//     // Input 상자 값에 따라 해당 값을 노란색으로 처리
//    $("#searchInput").on("input", function () {
//        const searchValue = $(this).val().trim().toLowerCase();
//        $("#swListModal .hstbody tr").each(function () {
//            const rowData = $(this).text().toLowerCase();
//            if (rowData.includes(searchValue)) {
//                $(this).addClass("highlight");
//            } else {
//                $(this).removeClass("highlight");
//            }
//        });
//    });


