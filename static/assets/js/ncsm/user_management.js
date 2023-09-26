/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/
// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};


var um_user_list = function () {
    var um_user_list_Data = $('#um_list').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        //searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,

        drawCallback: function (settings) {
            // 페이지 변경시 체크박스 값을 설정합니다.
            var api = this.api();
            var rows = api.rows({page: 'current'}).nodes();
            var allCheckedOnCurrentPage = rows.length > 0;


            // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                var data = api.row(row).data();
                var x_id = data.x_id;

                if (checkedItems[x_id]) {
                    $(row).find('input[type="checkbox"]').prop('checked', true);
                } else {
                    $(row).find('input[type="checkbox"]').prop('checked', false);
                    allCheckedOnCurrentPage = false; // 하나라도 체크되지 않은 체크박스가 있으면 전체선택 체크박스를 비활성화

                }
            }
            $('#select-all').prop('checked', allCheckedOnCurrentPage);
            var current_page_um_user = um_user_list_Data.page();
            var total_pages_um_user = um_user_list_Data.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages_um_user > 10) { // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
                $('<button type="button" class="btn" id="nexts_um_user">10≫</button>')
                    .insertAfter('#um_list_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after_um_user">≪10</button>')
                    .insertBefore('#um_list_paginate .paginate_button:first');
            }
        },
        ajax: {
            url: 'userpaging/',
            type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                    2: 'x_id',
                    3: 'x_name',
                    4: 'x_email',
                    5: 'x_auth',
                };
//                data.filter = {
//                    column: column,
//                    columnmap: columnMap[orderColumn],
//                    direction: orderDir,
//                    value : $('#search-input-hs').val(),
//                    value2 : $('#um_listt_filter input[type="search"]').val(),
//                    regex : false // OR 조건을 사용하지 않을 경우에는 false로 설정
//                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
            dataSrc: function (res) {
                var data = res.data;
                return data;
            }
        },

        columns: [
            {
                data: '',
                title: '<input type="checkbox" class="form-check-input" id="select-all" /><span>&nbsp;선택</span>',
                searchable: false
            },
            {data: '', title: 'No', searchable: true},
            {data: 'x_id', title: ' 아이디', searchable: true},
            {data: 'x_name', title: '사용자 이름', searchable: true},
            {data: 'x_email', title: '이메일', searchable: true},
            {data: 'x_auth', title: '권한', searchable: true},
            {data: 'x_user_auth', title: '권한 관리', searchable: false},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
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
            {
                targets: 0,
                width: "4%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const x_id = row.x_id;
                    return '<input type="checkbox" class="form-check-input" name="' + row.x_name + '" id="' + row.x_id + '" data-x-id="' + x_id + '" data-x-name="' + row.x_name + '">'
                }
            },
            {
                targets: 1,
                width: "3%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 2,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 4,
                width: "20%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 6,
                width: "10%",
                className: 'text-center text-truncate flex-cloumn column_hidden',
                render: function (data, type, row) {
                    const x_id = row.x_id;
                    return '<div class="ummore swmore-font" data-x_id="' + x_id + '" >권한 관리 설정</div>'
                }
            },
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
    //체크박스 저장하기
    um_checkbox_check($('#um_list tbody'))

    //전체선택
    $('#um_list').on('click', '#select-all', function () {
        var isChecked = $(this).prop('checked');

        $('#sec_asset_list2 tbody input[type="checkbox"]').each(function () {
            $(this).prop('checked', isChecked);
            var computer_id = $(this).data('computer-id');
            var computer_name = $(this).data('computer-name'); // 컴퓨터 이름도 가져옵니다.

            if (isChecked) {
                checkedItems[computer_id] = computer_name;
            } else {
                delete checkedItems[computer_id];
            }
        });
    });
    //개별선택
    $('#um_list tbody').on('click', 'input[type="checkbox"]', function () {
        var isChecked = $(this).prop('checked');
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');

        if (isChecked) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }

        var allChecked = true;
        $('#um_list tbody input[type="checkbox"]').each(function () {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false;
            }
        });

        $('#select-all').prop('checked', allChecked);
    });

    /*      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
        dropdown_text();

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
        $('#search-button-hs').click(function() {
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-hs').val().trim();

            performSearch(column, searchValue, um_user_list_Data)
        });

    $('#search-input-hs').on('keyup', function(event) {
            if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
                var column = $('#column-dropdown').data('column');
                var searchValue = $('#search-input-hs').val().trim();

                performSearch(column, searchValue, um_user_list_Data);
            }
        });*/

    $(document).on('click', '#nexts_um_user, #after_um_user', function () {
        var current_page_um_user = um_user_list_Data.page();
        var total_pages_um_user = um_user_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_um_user') {
            if (current_page_um_user + 10 < total_pages_um_user) {
                um_user_list_Data.page(current_page_um_user + 10).draw('page');
            } else {
                um_user_list_Data.page(total_pages_um_user - 1).draw('page');
            }
        } else {
            um_user_list_Data.page(Math.max(current_page_um_user - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_um_user, #after_um_user {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};

//
//var um_group_list = function () {
//	var um_group_list = $('#um_list').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><''p>>",
//		lengthMenu: [[5, 10, 25, 50], [5, 10, 25, 50]],
//        pageLength: 5,
//		responsive: false,
////		searching: true,
//		ordering: true,
//		serverSide: true,
//		displayLength: false,
//
//		drawCallback: function (settings) {
//            // 페이지 변경시 체크박스 값을 설정합니다.
//            var api = this.api();
//            var rows = api.rows({ page: 'current' }).nodes();
//
//            // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
//            for (var i = 0; i < rows.length; i++) {
//                var row = rows[i];
//                var data = api.row(row).data();
//                var computer_id = data.computer.computer_id;
//
//                if (checkedItems[computer_id]) {
//                    $(row).find('input[type="checkbox"]').prop('checked', true);
//                } else {
//                    $(row).find('input[type="checkbox"]').prop('checked', false);
//                }
//            }
//            var current_page_um_groupr = um_group_list.page();
//            var total_pages_um_groupr = um_group_list.page.info().pages;
//            $('#nexts').remove();
//            $('#after').remove();
//
//            if (total_pages_um_group > 10){ // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
//            $('<button type="button" class="btn" id="nexts_um_group">10≫</button>')
//            .insertAfter('#um_list_paginate .paginate_button:last');
//            $('<button type="button" class="btn" id="after_um_group">≪10</button>')
//            .insertBefore('#um_list_paginate .paginate_button:first');
//            }
//        },
//
//		ajax: {
//			url: 'grouppaging/',
//			type: "POST",
//            data: function (data) {
//                var column = $('#column-dropdown').data('column');
//                var orderColumn = data.order[0].column;
//                var orderDir = data.order[0].dir;
//                var columnMap = {
//                            2: 'chassistype',
//                            3: 'computer_name',
//                            4: 'ip_address',
//                            5: 'sw_list',
//                            6: 'sw_ver_list',
//                            7: 'sw_install',
//                            8: 'more',
//                            9: 'memo',
//
//                        };
//                data.filter = {
//                    column: column,
//                    value : $('#search-input-hs').val(),
//                    value2 : $('#um_list_filter input[type="search"]').val(),
//                    regex : false // OR 조건을 사용하지 않을 경우에는 false로 설정
//                };
//                data.page = (data.start / data.length) + 1;
//                data.page_length = data.length;
//            },
//			dataSrc: function (res) {
//				var data = res.data;
//				return data;
//			}
//		},
//
//		columns: [
//            { data: '', title: '선택', searchable: false },
//		    { data: '', title: 'No', searchable: true },
//			{ data: 'computer.chassistype', title: '구분', searchable: true },
//			{ data: 'computer.computer_name', title: '컴퓨터 이름', searchable: true },
//            { data: 'computer.ip_address', title: 'IPv4' , searchable: true},
//			{ data: 'computer.sw_list', title: '소프트웨어 목록', searchable: true },
//			{ data: 'computer.sw_ver_list', title: '소프트웨어 버전', searchable: true },
//			{ data: 'computer.sw_install', title: '설치 일자', searchable: true },
//			{ data: '', title: '더보기', searchable: false },
//			{ data: 'computer.memo', title: '메모', searchable: true },
//
//		],
//		rowCallback: function (row, data, index) {
//            var api = this.api();
//            var page = api.page.info().page;
//            var pageLength = api.page.info().length;
//            var index = (page * pageLength) + (index + 1);
//            $('td:eq(1)', row).html(index);
//        },
////        columnDefs: [
////		    {targets: 0, width: "10%", className: 'text-start text-truncate'},
////		    {targets: 1, width: "20%", className: 'text-start text-truncate'},
////		    {targets: 2, width: "10%", className: 'text-start text-truncate'},
////            {targets: 3, width: "10%", className: 'text-start text-truncate'},
////		    {targets: 4, width: "40%", className: 'text-start text-truncate'},
////		    {targets: 5, width: "10%", className: 'text-start text-truncate'},
////		],
//		columnDefs: [
//            {targets: 0, width: "2%", orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
//		        const computer_id = row.computer.computer_id;
//		        return '<input type="checkbox" class="form-check-input" name="'+row.computer.computer_name+'" id="'+row.computer.computer_id+'" data-computer-id="' + computer_id + '" data-computer-name="' + row.computer.computer_name + '">'
//            }},
//            {targets: 1, width: "3%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "3%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 3, width: "10%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 4, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 5, width: "15%", className: 'text-start text-truncate flex-cloumn column_hidden',
//		    render: function(data, type, row) {
//		        const swList = row.computer.sw_list;
//                const swListArray = swList ? swList.split('<br>') : [];
//		        return '<span data-toggle="tooltip">' + (swListArray[0] || '') + '<br>' + (swListArray[1] || '') + '<br>' + (swListArray[2] || '') + '<br>' + (swListArray[3] || '')}},
//
//		    {targets: 6, width: "10%", className: 'text-start text-truncate flex-cloumn column_hidden',
//		    render: function(data, type, row) {
//                const swVer = row.computer.sw_ver_list;
//                const swVerArray = swVer ? swVer.split('<br>') : [];
//		        return '<span data-toggle="tooltip">' + (swVerArray[0] || '') + '<br>' + (swVerArray[1] || '') + '<br>' + (swVerArray[2] || '') + '<br>' + (swVerArray[3] || '')}},
//
//		    {targets: 7, width: "10%", className: 'text-start text-truncate flex-cloumn column_hidden',
//		    render: function(data, type, row) {
//		        const swInstall= row.computer.sw_install;
//		        const swInstallArray = swInstall ? swInstall.split('<br>') : [];
//		        return '<span data-toggle="tooltip">' + (swInstallArray[0] || '') + '<br>' + (swInstallArray[1] || '') + '<br>' + (swInstallArray[2] || '') + '<br>' + (swInstallArray[3] || '')}},
//
//		    {targets: 8, width: "5%", className: 'text-start text-truncate flex-cloumn column_hidden',
//		    render: function(data, type, row) {
//		        const computer_name = row.computer.computer_name;
//		        const swList = row.computer.sw_list;
//		        const swVer = row.computer.sw_ver_list;
//		        const swInstall= row.computer.sw_install;
//		        return '</span><br><div class="pur_swmore swmore-font" data-swlist="' + swList + '" data-swver="' + swVer + '" data-swinstall="' + swInstall + '" data-computer_name="' + computer_name +'">더보기...</div>'}},
//
//		    {targets: 9, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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
//            },
//            pagingType: 'numbers',//이전 다음 버튼 히든처리
//});
//    //체크박스 저장하기
//um_checkbox_check($('#um_list tbody'))
//
//    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
//    dropdown_text();
//
//
//      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
//    $('#search-button-up').click(function() {
//        var column = $('#column-dropdown').data('column');
//        var searchValue = $('#search-input').val().trim();
//
//        performSearch(column, searchValue, um_group_list_Data);
//    });
//
//    // 검색창 enter 작동
//    $('#search-input').on('keyup', function(event) {
//        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
//            var column = $('#column-dropdown').data('column');
//            var searchValue = $('#search-input').val().trim();
//
//            performSearch(column, searchValue, um_group_list_Data);
//        }
//    });
//
//	$(document).on('click', '#nexts_um_group, #after_um_group', function() {
//        var current_page_um_group = um_group_list.page();
//        var total_pages_um_group = um_group_list.page.info().pages;
//        if ($(this).attr('id') == 'nexts_um_group') {
//                if (current_page_um_group + 10 < total_pages_um_group) {
//                    um_group_list.page(current_page_um_group + 10).draw('page');
//                } else {
//                    um_group_list.page(total_pages_um_group - 1).draw('page');
//                }
//                } else {
//                    um_group_list.page(Math.max(current_page_um_group- 10, 0)).draw('page');
//                }
//});
//    var customStyle = '<style>#nexts_um_group, #after_um_group {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//    $('head').append(customStyle);
//};

function um_userbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>선택</th><th>No</th><th>아이디</th><th>사용자 이름</th><th>이메일</th><th>권한</th></tr></thead><tbody></tbody>';
    $('#um_list').DataTable().destroy();
    $('#um_list').html(newTableContent);
    um_user_list();
    $(btn).addClass('active');
    //$('.hsbutton').not(btn).removeClass('active');
    checkedItems = {};
};
//
//function pur_swbutton(btn) {
//    let newTableContent = '';
//    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>선택</th><th>No</th><th>구분</th><th>컴퓨터 이름</th><th>IPv4</th><th>소프트웨어 목록</th><th>소프트웨어 버전</th><th>설치 일자</th><th>더보기</th><th>메모</th></tr></thead><tbody></tbody>';
//    $('#um_list').DataTable().destroy();
//    $('#um_list').html(newTableContent);
//    um_group_list();
//    $(btn).addClass('active');
//    $('.hsbutton').not(btn).removeClass('active');
//    checkedItems = {};
//};

//// 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
//function dropdown_text(){
//    $('.dropdown-menu a').click(function() {
//        var column = $(this).data('column');
//        $('#column-dropdown').text($(this).text());
//        $('#column-dropdown').data('column', column);
//    });
//};

$(document).ready(function () {
    user_list_popup();
    um_user_list();
    //sidebar();
    //initEvent();
    //initializeDataTable();

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
$(document).on("click", ".ummore", function (e) {
    const x_id = $(this).data("x_id");
    var modalbody = "";
    modalbody += '권한' + x_id;
    $("#um_auth_modal .hstbody").html(modalbody);
//    $("#swListModal .modal-title").htlbody);
    $("#um_auth_modal").modal("show");
//    $("#swListModal .hstbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
});

var insert_modal = document.getElementById("um_insert_modal");
var delete_modal = document.getElementById("um_delete_modal");
var auth_modal = document.getElementById("um_auth_modal");

// insert 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#um_insert", function (e) {
    insert_modal.style.display = "block";
});

// delete 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#um_delete", function (e) {
    delete_modal.style.display = "block";
    const x_id = [];
    const x_name = [];
    var modalbody = "";
    for (const x_id in checkedItems) {
        const x_name = checkedItems[x_id];
        //modalbody += '<div><input type="hidden" name="'+computer_id+'" id="'+computer_id+'" value="'+computer_id+'">'+computer_name+'</div>'
        //modalbody += '<input type="hidden" name="'+computer_name+'" id="'+computer_name+'" value="'+computer_name+'">'
        //modalbody += '컴퓨터아이디'+computer_id + '<br/>';

        modalbody += '<input type="hidden" class="delete_hidden" id="' + x_id + '" value="' + x_id + '"><label class="form-check-label" for="x_id">' + x_id + '</label><br>'
    }
    $("#um_delete_form .form-check").html(modalbody);
    //$("#um_delete_form").modal("show");
});

// insert 모달 닫기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#closeBtn", function (e) {
    insert_modal.style.display = "none";
});
// delete 모달 닫기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#closeBtn2", function (e) {
    delete_modal.style.display = "none";
});
// auth 모달 닫기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#closeBtn3", function (e) {
    $("#um_auth_modal").modal("hide");
    auth_modal.style.display = "none";
});
// 모달 외부 클릭 시 닫기 이벤트 핸들러
window.onclick = function (event) {
    if (event.target == insert_modal) {
        insert_modal.style.display = "none";
    } else if (event.target == delete_modal) {
        delete_modal.style.display = "none";
    } else if (event.target == auth_modal) {
        auth_modal.style.display = "none";
    }
};


function um_checkbox_check($tbody) {
    $tbody.on('click', 'input[type="checkbox"]', function (event) {
        event.stopPropagation(); // Prevent the row click event from firing when clicking the checkbox
        var x_id = $(this).data('x-id');
        var x_name = $(this).data('x-name');
        console.log("Clicked checkbox for computer ID:", x_id);
        if ($(this).prop('checked')) {
            checkedItems[x_id] = x_id;
        } else {
            delete checkedItems[x_id];
        }
    });
}

//삭제하기 체크
$(document).on("click", "#user_delete", function (event) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.
    var x_ids = [];

    $(".delete_hidden").each(function () {
        var value = $(this).val(); // 각 hidden 요소의 값을 가져오기
        x_ids.push(value); // 값을 배열에 추가
    });

    $.ajax({
        url: "/user_management/um_delete/", // 서버의 URL을 여기에 입력
        method: "POST", // 또는 "GET" 등 HTTP 요청 메서드 선택
        data: {
            'x_id': x_ids.join(',')

        }, // x_id 값을 서버로 전송
        success: function (response) {
            if (response.result === 'success') {
                $("#delete_modal").modal("hide"); // 모달 창 닫기
                alert("유저가 삭제되었습니다.")
                window.location.href = "/user_management/"; // 리다이렉트
            } else {
                console.error("Delete failure");
                // 실패한 경우 처리
            }
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            // 오류 처리
        }
    });
});

//추가하기 체크
function um_check() {
    var uid = document.getElementById("x_id");
    var pwd = document.getElementById("x_pw");
    var repwd = document.getElementById("re_x_pw");
    var uname = document.getElementById("x_name");
    var email_id = document.getElementById("x_email");
    var x_auth = document.getElementById("x_auth");
    var agree = document.getElementById("customCheck1");
    var page = document.getElementById("page");

    var uidCheck = /^[a-zA-z0-9]{4,12}$/;
    if (!uidCheck.test(uid.value)) {
        alert("아이디는 영문 대소문자와 숫자 4~12자리로 입력해야합니다.");
        uid.focus(); //focus(): 커서가 깜빡이는 현상, blur(): 커서가 사라지는 현상
        return false;
    }
    ;

    if (pwd.value == "") {
        alert("비밀번호를 입력하세요.");
        pwd.focus();
        return false;
    }
    ;

    //비밀번호 영문자+숫자+특수조합(8~25자리 입력) 정규식
    var pwdCheck = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,25}$/;

    if (!pwdCheck.test(pwd.value)) {
        alert("비밀번호는 영문자+숫자+특수문자 조합으로 8~25자리 사용해야 합니다.");
        pwd.focus();
        return false;
    }
    ;

    if (repwd.value !== pwd.value) {
        alert("비밀번호가 일치하지 않습니다..");
        repwd.focus();
        return false;
    }
    ;


    if (uname.value == "") {
        alert("이름을 입력해 주세요");
        uname.focus();
        return false;
    }
    ;


    var email_idCheck = /^[A-Za-z0-9_]+[A-Za-z0-9]*[@]{1}[A-Za-z0-9]+[A-Za-z0-9]*[.]{1}[A-Za-z]{1,3}$/;

    if (!email_idCheck.test(email_id.value)) {
        alert("이메일 형식이 올바르지 않습니다.");
        email_id.focus();
        return false;
    }

    //입력 값 전송
    document.um_signup_form.submit(); //유효성 검사의 포인트
}
