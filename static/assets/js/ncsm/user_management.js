
// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};


var um_user_list = function () {
    var um_user_list = $('#um_list').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: false,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [6, "desc"]
        ],
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
            var current_page_um_user = um_user_list.page();
            var total_pages_um_user = um_user_list.page.info().pages;
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
                //title: '<input type="checkbox" class="form-check-input" id="select-all" /><span>&nbsp;선택</span>',
                title: '<span>선택</span>',
                searchable: false
            },
            {data: '', title: 'No', searchable: true},
            {data: 'x_id', title: ' 아이디', searchable: true},
            {data: 'x_name', title: '사용자 이름', searchable: true},
            {data: 'x_email', title: '이메일', searchable: true},
            {data: 'x_auth', title: '부서', searchable: true},
            {data: 'create_date', title: '가입 날짜', searchable: true},
            {data: 'x_user_auth', title: '권한 관리', searchable: false},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "4%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const x_id = row.x_id;
                    return '<input type="checkbox" class="form-check-input"  id="' + x_id + '" data-x-id="' + x_id + '" >'
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
                    data = data.replace("T", " ").substring(0, 16);
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 7,
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


//    //개별선택
//    $('#um_list tbody').on('click', 'input[type="checkbox"]', function () {
//        var isChecked = $(this).prop('checked');
//        var x_id = $(this).data('x_id');
//
//
//        if (isChecked) {
//            checkedItems[x_id] = x_id;
//        } else {
//            delete checkedItems[x_id];
//        }
//
//        var allChecked = true;
//        $('#um_list tbody input[type="checkbox"]').each(function () {
//            if (!$(this).prop('checked')) {
//                allChecked = false;
//                return false;
//            }
//        });
//
//        $('#select-all').prop('checked', allChecked);
//    });

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
        var current_page_um_user = um_user_list.page();
        var total_pages_um_user = um_user_list.page.info().pages;
        if ($(this).attr('id') == 'nexts_um_user') {
            if (current_page_um_user + 10 < total_pages_um_user) {
                um_user_list.page(current_page_um_user + 10).draw('page');
            } else {
                um_user_list.page(total_pages_um_user - 1).draw('page');
            }
        } else {
            um_user_list.page(Math.max(current_page_um_user - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_um_user, #after_um_user {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var um_group_list = function () {
	var um_group_list = $('#um_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><''p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
		responsive: false,
     	searching: false,
		ordering: true,
		serverSide: true,
		displayLength: false,
		drawCallback: function (settings) {
            // 페이지 변경시 체크박스 값을 설정합니다.
            var api = this.api();
            var rows = api.rows({ page: 'current' }).nodes();

            // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                var data = api.row(row).data();
                var xuser_group = data.xuser_group;

                if (checkedItems[xuser_group]) {
                    $(row).find('input[type="checkbox"]').prop('checked', true);
                } else {
                    $(row).find('input[type="checkbox"]').prop('checked', false);
                }
            }
            var current_page_um_group = um_group_list.page();
            var total_pages_um_group = um_group_list.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages_um_group > 10){ // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
            $('<button type="button" class="btn" id="nexts_um_group">10≫</button>')
            .insertAfter('#um_list_paginate .paginate_button:last');
            $('<button type="button" class="btn" id="after_um_group">≪10</button>')
            .insertBefore('#um_list_paginate .paginate_button:first');
            }
        },

		ajax: {
			url: 'grouppaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                            2: 'xgroup_name',
                            3: 'xgroup_note',
                            4: 'xuser_id_list',
                        };
//                data.filter = {
//                    column: column,
//                    value : $('#search-input-hs').val(),
//                    value2 : $('#um_list_filter input[type="search"]').val(),
//                    regex : false // OR 조건을 사용하지 않을 경우에는 false로 설정
//                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
			dataSrc: function (res) {
				var data = res.data;
				//console.log(data);
				return data;
			}
		},

        columns: [
            {
                data: '',
                //title: '<input type="checkbox" class="form-check-input" id="select-all" /><span>&nbsp;선택</span>',
                title: '<span>선택</span>',
                searchable: false
            },
            {data: '', title: 'No', searchable: true},
            {data: 'xgroup_name', title: '그룹 이름', searchable: true},
            {data: 'xgroup_note', title: '그룹 설명', searchable: true},
            {data: 'xuser_id_list', title: '그룹원', searchable: true},
            {data: 'create_date', title: '생성 날짜', searchable: true},
            {data: 'id', title: '권한 관리', searchable: false},

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
                    const xgroup_name = row.xgroup_name;
                    const id = row.id;
                    return '<input type="checkbox" class="form-check-input"  id="' + id + '" data-xgroup_name="' + xgroup_name + '"  data-x_group_id="' + id + '">'
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
                    const xgroup_name = row.xgroup_name;
                    const xgroup_note = row.xgroup_note;
                    const xuser_id_list = row.xuser_id_list;
                    const id = row.id;
                    return '<div class="um_groupalter swmore-font" data-xgroup_name="' + xgroup_name + '" data-id="'+ id +'" data-xuser_id_list="'+ xuser_id_list +'">'+data+'</div>'
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
                    const xuser_id_list = row.xuser_id_list.replace(/'/g, '').replace(']','').replace('[','').split(', ');
                    return '<span data-toggle="tooltip">' + xuser_id_list + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center text-truncate flex-cloumn column_hidden',
                render: function (data, type, row) {
                    data = data.replace("T", " ").substring(0, 16);
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 6,
                width: "10%",
                className: 'text-center text-truncate flex-cloumn column_hidden',
                render: function (data, type, row) {
                    const xgroup_name = row.xgroup_name;
                    const id = row.id;
                    const xuser_id_list = row.xuser_id_list;
                    return '<div class="um_groupmore swmore-font" data-xgroup_name="' + xgroup_name + '" data-id="'+ id +'" data-xuser_id_list="'+ xuser_id_list +'">권한 관리 설정</div>'
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

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    //dropdown_text();


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

	$(document).on('click', '#nexts_um_group, #after_um_group', function() {
        var current_page_um_group = um_group_list.page();
        var total_pages_um_group = um_group_list.page.info().pages;
        if ($(this).attr('id') == 'nexts_um_group') {
                if (current_page_um_group + 10 < total_pages_um_group) {
                    um_group_list.page(current_page_um_group + 10).draw('page');
                } else {
                    um_group_list.page(total_pages_um_group - 1).draw('page');
                }
                } else {
                    um_group_list.page(Math.max(current_page_um_group- 10, 0)).draw('page');
                }
});
    var customStyle = '<style>#nexts_um_group, #after_um_group {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};

function um_userbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>선택</th><th>No</th><th>아이디</th><th>사용자 이름</th><th>이메일</th><th>부서</th><th>가입 날짜</th><th>권한 관리</th></tr></thead><tbody></tbody>';
    $('#um_list').DataTable().destroy();
    $('#um_list').html(newTableContent);
    um_user_list();
    $('#um_creategroup').text("그룹 생성");
    $(btn).addClass('active');
    $('#um_creategroup').removeClass('hidden');
    //$('.hsbutton').not(btn).removeClass('active');
    checkedItems = {};
};

function um_groupbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>선택</th><th>No</th><th>그룹명</th><th>그룹 설명</th><th>그룹원</th><th>생성 날짜</th><th>권한 관리</th></thead><tbody></tbody>';
    $('#um_list').DataTable().destroy();
    $('#um_list').html(newTableContent);
    um_group_list();
    //$('#um_creategroup').text("그룹 생성/수정");
    $(btn).addClass('active');
    $('#um_creategroup').addClass('hidden');
    //$('.hsbutton').not(btn).removeClass('active');
    checkedItems = {};
};


//################# 컴퓨터 체크하기 ##########################################
function um_checkbox_check($tbody) {
    $tbody.on('click', 'input[type="checkbox"]', function (event) {
        event.stopPropagation(); // Prevent the row click event from firing when clicking the checkbox
        var x_id = $(this).data('x-id');
        var x_group_id = $(this).data('x_group_id');
        var xgroup_name = $(this).data('xgroup_name');

        if (x_id) {
            //console.log(x_id);
            if ($(this).prop('checked')) {
                checkedItems[x_id] = x_id;
            } else {
                delete checkedItems[x_id];
            }
        } else if (x_group_id) {
            //console.log(x_group_id);
            if ($(this).prop('checked')) {
                // Add the group value to checkedItems
                checkedItems[x_group_id] = xgroup_name;
                console.log(checkedItems)
                //checkedItems['xgroup_name'] = xgroup_name;
            } else {
                // Remove the group value from checkedItems
                delete checkedItems[x_group_id];
                //delete checkedItems['xgroup_name'];
            }
        }
    });
}


$(document).ready(function () {
    user_list_popup();
    um_user_list();

});



//################ USER 권한관리 설정 JS ######################################
$(document).on("click", ".ummore", function (e) {
    const x_id = $(this).data("x_id");
    $.ajax({
        url: 'user_auth/',
        method:'POST',
        data:{
            x_id: x_id
        },
        success: function (res) {
            var data = res;
            // AJAX 요청이 성공한 후에 modalbody를 설정하고 모달을 열기
            var modalbody = '<div>'+x_id+' 권한</div>';
            modalbody += '<form id="authForm">';
            modalbody += '<input type="hidden" class="form-check-label" name="x_id" value="' + x_id + '">';
            // data.auth_list 배열의 각 항목을 반복하며 체크박스 생성
            data.auth_list.forEach(function (authItem) {
                modalbody += '<label class="form-check-label">';
                modalbody += '<input class="form-check-input" type="checkbox" name="' + authItem.xfactor_auth.auth_id + '" value="' + authItem.auth_use + '"';
                //modalbody += '<input class="form-check-input" type="checkbox" name="auth_id" value="' + authItem.xfactor_auth.auth_id + '"';
                if (authItem.auth_use === 'true') {
                    modalbody += ' checked';
                }
                modalbody += '>';
                modalbody += authItem.xfactor_auth.auth_name;
                modalbody += '</label><br>';
            });

            modalbody += '</form>';

            $("#um_auth_modal .hstbody").html(modalbody);
            $("#um_auth_modal").modal("show");


            //User페이지 권한 SAVE저장시 실행
            $(document).off("click", "#user_auth_save").on("click", "#user_auth_save", function (e) {
                e.preventDefault(); // 기본 폼 제출 동작을 막음
                var authInfo = []; // 각 체크박스 정보를 저장할 배열
                data.auth_list.forEach(function (authItem) {
                    const checkbox = $('[name="' + authItem.xfactor_auth.auth_id + '"]');
                    authInfo.push({
                        auth_id: authItem.xfactor_auth.auth_id,
                        auth_use: checkbox.is(":checked") ? 'true' : 'false'
                    });
                });
                //console.log(authInfo)
                // 서버에 체크된 auth_ids와 x_id를 전달하여 DB에 저장 요청 보냄
                $.ajax({
                    url: 'save_user_auth/',
                    method: 'POST',
                    data: {
                        x_id: x_id,
                        auth_info: JSON.stringify(authInfo) // authInfo 배열을 JSON 문자열로 변환하여 전송
                    },
                    success: function (res) {
                        // 저장 완료 후 어떤 작업을 수행할 수 있음
                        console.log("권한이 저장되었습니다.");
                        alert("권한이 저장되었습니다.")
                        $("#um_auth_modal").modal("hide");
                    },
                    error: function (err) {
                        // 저장 중 에러 발생 시 처리
                        console.error("권한 저장 중 에러가 발생했습니다.", err);
                        alert("권한 저장 중 에러가 발생했습니다.")
                    },
                });
            });
        },
    })
});
//###############################################################################

//################ Group 권한관리 설정 JS ######################################
$(document).on("click", ".um_groupmore", function (e) {
    const xgroup_name = $(this).data("xgroup_name");
    const id = $(this).data("id");
    const xuser_id_list = $(this).data("xuser_id_list");

    //console.log(xuser_id_list)
    $.ajax({
        url: 'group_auth/',
        method:'POST',
        data:{
            xgroup_name: xgroup_name
        },
        success: function (res) {
            var data = res;
           // console.log(data)
            // AJAX 요청이 성공한 후에 modalbody를 설정하고 모달을 열기
            var modalbody = '<div>'+xgroup_name+' 권한</div>';
            modalbody += '<form id="authForm">';
            modalbody += '<input type="hidden" class="form-check-label" name="x_id" value="' + id + '">';
            modalbody += '<input type="hidden" class="form-check-label" name="xuser_id_list" value="' + xuser_id_list + '">';
            // data.auth_list 배열의 각 항목을 반복하며 체크박스 생성
            data.auth_list.forEach(function (authItem) {
                modalbody += '<label class="form-check-label">';
                modalbody += '<input class="form-check-input" type="checkbox" name="' + authItem.auth_id + '" value=""';
                //modalbody += '<input class="form-check-input" type="checkbox" name="auth_id" value="' + authItem.xfactor_auth.auth_id + '"';
//                if (authItem.auth_use === 'true') {
//                    modalbody += ' checked';
//                }
                modalbody += '>';
                modalbody += authItem.auth_name;
                modalbody += '</label><br>';
            });

            modalbody += '</form>';

            $("#um_auth_modal .hstbody").html(modalbody);
            $("#um_auth_modal").modal("show");


            //User페이지 권한 SAVE저장시 실행
            $(document).off("click", "#user_auth_save").on("click", "#user_auth_save", function (e) {
                e.preventDefault(); // 기본 폼 제출 동작을 막음
                var xuser_id_list_value = $('[name="xuser_id_list"]').val();
                var x_id_array = JSON.parse(xuser_id_list_value.replace(/'/g, '"'));
                var authInfo = [];
                //console.log(x_id_array)
                data.auth_list.forEach(function (authItem) {
                    const checkbox = $('[name="' + authItem.auth_id + '"]');
                    authInfo.push({
                        auth_id: authItem.auth_id,
                        auth_use: checkbox.is(":checked") ? 'true' : 'false'
                    });
                });
                console.log(x_id_array)
                // 서버에 체크된 auth_ids와 x_id를 전달하여 DB에 저장 요청 보냄
                $.ajax({
                    url: 'save_group_auth/',
                    method: 'POST',
                    data: {
                        x_id_array: JSON.stringify(x_id_array),
                        auth_info: JSON.stringify(authInfo) // authInfo 배열을 JSON 문자열로 변환하여 전송
                    },
                    success: function (res) {
                        // 저장 완료 후 어떤 작업을 수행할 수 있음
                        console.log("권한이 저장되었습니다.");
                        alert("권한이 저장되었습니다.")
                        $("#um_auth_modal").modal("hide");
                    },
                    error: function (err) {
                        // 저장 중 에러 발생 시 처리
                        console.error("권한 저장 중 에러가 발생했습니다.", err);
                        alert("권한 저장 중 에러가 발생했습니다.")
                    },
                });
            });
        },
    })
});



//######################################### 모달창 열고닫기 JS ##############################
var insert_modal = document.getElementById("um_insert_modal");
var delete_modal = document.getElementById("um_delete_modal");
var auth_modal = document.getElementById("um_auth_modal");

// insert 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#um_insert", function (e) {
    insert_modal.style.display = "block";
});

// delete 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#um_delete", function (e) {
    var modalbody = "";
    const checkedIds = Object.keys(checkedItems); // Assuming checkedItems is an object with IDs as keys

    if (checkedIds.length === 0) {
        // 체크된 체크박스가 없는 경우 알람 창을 띄우고 삭제 동작을 수행하지 않습니다.
        alert("적어도 하나의 항목을 선택하세요.");
    } else {
        delete_modal.style.display = "block";

        checkedIds.forEach(function (x_id) {
            // Check if x_id is a string
            if (typeof x_id === "string") {
                console.log(x_id);
                if (!isNaN(x_id)) {
                    // If x_id is a numeric string (e.g., "1")
                    const x_group_id = x_id;
                    const xgroup_name = checkedItems[x_id];
                    modalbody += `
                        <label class="form-check-label" for="${x_group_id}">
                            <input type="hidden" class="delete_hidden" id="${x_group_id}" value="${x_group_id}">
                            ${xgroup_name}
                        </label><br>`;
                } else {
                    // If x_id is a regular string (e.g., "Test Group")
                    const x_name = x_id;
                    modalbody += '<label class="form-check-label" for="x_id"><input type="hidden" class="delete_hidden" id="' + x_id + '" value="' + x_id + '">' + x_name + '</label><br>';
                }
            }
        });

        $("#um_delete_form .form-check").html(modalbody);
        // $("#um_delete_form").modal("show"); // Uncomment this line if needed
    }
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
//##########################################################################################


//####################################유저 삭제하기 ##########################
$(document).on("click", "#user_delete", function (event) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.
    var x_ids = [];

    $(".delete_hidden").each(function () {
        var value = $(this).val(); // 각 hidden 요소의 값을 가져오기
        x_ids.push(value); // 값을 배열에 추가
    });
    var hasGroupItems = x_ids.some(function (id) {
        return !isNaN(id);
    });
    if (hasGroupItems) {
        // 그룹 처리를 위한 AJAX
        $.ajax({
            url: "/user_management/group_delete/", // 그룹 삭제를 처리하는 URL
            method: "POST",
            data: {
                'group_ids': x_ids.filter(id => !isNaN(id)).join(',')
            },
            success: function (response) {
                if (response.result === 'success') {
                    // 그룹 삭제 성공 처리
                    alert("그룹이 삭제되었습니다.");
                } else {
                    console.error("Group delete failure");
                    // 그룹 삭제 실패 처리
                }
            },
            error: function (xhr, status, error) {
                console.error("Group delete error:", error);
                // 그룹 삭제 오류 처리
            }
        });
    }


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
//############################################################################


//############################### Group 생성하기 ###############################
$(document).on("click","#um_creategroup", function (e){
    //console.log("aaa");
    $("#groupName_auth").val("");
    $("#groupDescription_auth").val("");
    const check_id = [];

    var modalbody = "";
    console.log(checkedItems)

    for (const x_id in checkedItems) {
        modalbody += '<input class="form-check-input" type="checkbox" value="'+x_id+'" id="'+x_id+'" checked><label class="form-check-label" for="'+x_id+'">'+x_id+'</label><br>'
    }
    $("#group_insert_modal .modal-title").html("그룹 생성 팝업창");
    $("#group_insert_modal .form-check").html(modalbody);
    $("#group_insert_modal").modal("show");
});

$(document).on("click","#group_insert", function(e) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.
//    const x_id = $(this).data("x_id");
//    console.log(x_id);

    var form = document.getElementById("GroupCreateForm_auth");
    //console.log(form)
    var xgroup_name = form.elements.groupName_auth.value;
    var xgroup_description = form.elements.groupDescription_auth.value;
    let xuserIds = []
    const xuserElements = $('#group_insert_modal .form-check').find('.form-check-input');
    //console.log(xuserElements)
    xuserElements.each(function () {
        const x_id = $(this).attr("id");
        xuserIds.push(x_id);
    });

    $.ajax({
    url: 'groupcreate_auth/', // views.py 파일의 URL을 여기에 넣으세요.
    type: 'POST',
    dataType: 'json',
    data:  {
         'xgroup_name' : xgroup_name,
         'xgroup_description' : xgroup_description,
         'xuserIds' : JSON.stringify(xuserIds),
    },

    success: function (response) {
    // response에 따른 처리 - 예: 경고창 띄우기
        if (response.success == "success") {
            alert(response.message);
            $('#group_insert_modal').modal('hide');
            //Group으로 페이지이동
            //um_group_list()
        } else {
            alert('실패 : ' + response.message);
        }
    }
    });
});


//############################### Group 수정하기 ###############################
$(document).on("click",".um_groupalter", function (e){
    console.log("aaa");
//    $("#groupNameAlter_auth").val("");
//    $("#groupDescriptionAlter_auth").val("");

    const xgroup_name = $(this).data("xgroup_name");
    const id = $(this).data("id");
    const xuser_id_list = $(this).data("xuser_id_list");
//    const check_id = [];

    var modalbody = "";
//    console.log(checkedItems)

    for (const x_id in checkedItems) {
        modalbody += '<input class="form-check-input" type="checkbox" value="'+x_id+'" id="'+x_id+'" checked><label class="form-check-label" for="'+x_id+'">'+x_id+'</label><br>'
    }
    $("#group_alter_modal .modal-title").html("그룹 수정 팝업창");
    $("#group_alter_modal .form-check").html(modalbody);
    $("#group_alter_modal").modal("show");
});

$(document).on("click","#group_alter", function(e) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.
//    const x_id = $(this).data("x_id");
//    console.log(x_id);

    var form = document.getElementById("GroupalterForm_auth");
    //console.log(form)
    var xgroup_name = form.elements.groupName_auth.value;
    var xgroup_description = form.elements.groupDescription_auth.value;
    let xuserIds = []
    const xuserElements = $('#group_insert_modal .form-check').find('.form-check-input');
    //console.log(xuserElements)
    xuserElements.each(function () {
        const x_id = $(this).attr("id");
        xuserIds.push(x_id);
    });

    $.ajax({
    url: 'groupcreate_auth/', // views.py 파일의 URL을 여기에 넣으세요.
    type: 'POST',
    dataType: 'json',
    data:  {
         'xgroup_name' : xgroup_name,
         'xgroup_description' : xgroup_description,
         'xuserIds' : JSON.stringify(xuserIds),
    },

    success: function (response) {
    // response에 따른 처리 - 예: 경고창 띄우기
        if (response.success == "success") {
            alert(response.message);
            $('#group_insert_modal').modal('hide');
            //Group으로 페이지이동
            //um_group_list()
        } else {
            alert('실패 : ' + response.message);
        }
    }
    });
});








//추가하기 회원가입 체크
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
