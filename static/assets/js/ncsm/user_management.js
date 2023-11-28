
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
        autoWidth: false,
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
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', { class: 'pagination' }).appendTo($pagination);

            // 첫 페이지 버튼
            $('<li>', {
                class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: '1', // '«' 대신 페이지 번호 사용
                    click: function () {
                        api.page('first').draw(false);
                    }
                })
            }).appendTo($ul);

            // 이전 버튼 (10칸 이동)
            $('<li>', {
                class: 'page-item' + (pageInfo.page < 10 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: '이전',
                    click: function () {
                        api.page(Math.max(pageInfo.page - 10, 0)).draw(false);
                    }
                })
            }).appendTo($ul);

            // 중앙 페이지네이션
            var startPage = Math.floor(pageInfo.page / 10) * 10;
            var endPage = Math.min(startPage + 10, pageInfo.pages);
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === i ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page(parseInt($(event.target).text()) - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 다음 버튼 (10칸 이동)
            $('<li>', {
                class: 'page-item' + (pageInfo.page >= pageInfo.pages - 10 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: '다음',
                    click: function () {
                        api.page(Math.min(pageInfo.page + 10, pageInfo.pages - 1)).draw(false);
                    }
                })
            }).appendTo($ul);

            // 마지막 페이지 버튼
            $('<li>', {
                class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: pageInfo.pages, // '»' 대신 마지막 페이지 번호 사용
                    click: function () {
                        api.page('last').draw(false);
                    }
                })
            }).appendTo($ul);
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
            {data: '', title: 'No', searchable: false},
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
                orderable: false,
                searchable: false,
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
                orderable: false,
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
		autoWidth: false,
		order: [
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
                var xuser_group = data.xuser_group;

                if (checkedItems[xuser_group]) {
                    $(row).find('input[type="checkbox"]').prop('checked', true);
                } else {
                    $(row).find('input[type="checkbox"]').prop('checked', false);
                }
            }
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', { class: 'pagination' }).appendTo($pagination);

            // 첫 페이지 버튼
            $('<li>', {
                class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: '1', // '«' 대신 페이지 번호 사용
                    click: function () {
                        api.page('first').draw(false);
                    }
                })
            }).appendTo($ul);

            // 이전 버튼 (10칸 이동)
            $('<li>', {
                class: 'page-item' + (pageInfo.page < 10 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: '이전',
                    click: function () {
                        api.page(Math.max(pageInfo.page - 10, 0)).draw(false);
                    }
                })
            }).appendTo($ul);

            // 중앙 페이지네이션
            var startPage = Math.floor(pageInfo.page / 10) * 10;
            var endPage = Math.min(startPage + 10, pageInfo.pages);
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === i ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page(parseInt($(event.target).text()) - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 다음 버튼 (10칸 이동)
            $('<li>', {
                class: 'page-item' + (pageInfo.page >= pageInfo.pages - 10 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: '다음',
                    click: function () {
                        api.page(Math.min(pageInfo.page + 10, pageInfo.pages - 1)).draw(false);
                    }
                })
            }).appendTo($ul);

            // 마지막 페이지 버튼
            $('<li>', {
                class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                html: $('<a>', {
                    class: 'page-link',
                    href: 'javascript:void(0)',
                    text: pageInfo.pages, // '»' 대신 마지막 페이지 번호 사용
                    click: function () {
                        api.page('last').draw(false);
                    }
                })
            }).appendTo($ul);
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
                            5: 'create_date',
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
            {data: '', title: 'No', searchable: false},
            {data: 'xgroup_name', title: '그룹 이름', searchable: true},
            {data: 'xgroup_note', title: '그룹 설명', searchable: true},
            {data: 'xuser_id_list', title: '그룹원', searchable: false},
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
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 2,
                width: "10%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const xgroup_name = row.xgroup_name;
                    const xgroup_note = row.xgroup_note;
                    const xuser_id_list = row.xuser_id_list;
                    const id = row.id;
                    return '<div class="um_groupalter swmore-font" data-xgroup_name="' + xgroup_name + '" data-id="'+ id +'" data-xgroup_note="'+ xgroup_note +'" data-xuser_id_list="'+ xuser_id_list +'">'+data+'</div>'
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
                orderable: false,
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    const xuser_id_list = row.xuser_id_list.replace(/'/g, '').replace(']','').replace('[','').split(', ');
                    return '<span data-toggle="tooltip">' + xuser_id_list + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden',
                render: function (data, type, row) {
                    data = data.replace("T", " ").substring(0, 16);
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 6,
                width: "10%",
                orderable: false,
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
    $('#um_creategroup').addClass('hidden');
    $('#um_delete').text("USER 삭제");
    $(btn).addClass('active');
    $('#um_insert').removeClass('hidden');
    //$('.hsbutton').not(btn).removeClass('active');
    checkedItems = {};
};

function um_groupbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>선택</th><th>No</th><th>그룹명</th><th>그룹 설명</th><th>그룹원</th><th>생성 날짜</th><th>권한 관리</th></thead><tbody></tbody>';
    $('#um_list').DataTable().destroy();
    $('#um_list').html(newTableContent);
    um_group_list();
    $('#um_delete').text("GROUP 삭제");
    $('#um_insert').addClass('hidden');
    //$('#um_creategroup').text("그룹 생성/수정");
    $(btn).addClass('active');
    $('#um_creategroup').removeClass('hidden');
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
                //console.log(checkedItems)
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
            data.auth_list.sort(function (a, b) {
                // auth_list 배열을 auth_num 기준으로 정렬합니다.
                return a.xfactor_auth.auth_num - b.xfactor_auth.auth_num;
            });
            data.auth_list.forEach(function (authItem, index) {
                modalbody += '<label class="form-check-label">';
                modalbody += '<input class="form-check-input" type="checkbox" name="' + authItem.xfactor_auth.auth_id + '" value="' + authItem.auth_use + '"';
                //modalbody += '<input class="form-check-input" type="checkbox" name="auth_id" value="' + authItem.xfactor_auth.auth_id + '"';
                if (authItem.auth_use === 'true') {
                    modalbody += ' checked';
                }
                modalbody += '> &nbsp;';
                modalbody += authItem.xfactor_auth.auth_name;
                modalbody += '</label><br>';
                if (index === 8) {
                    modalbody += '<br><div>'+x_id+' 대시보드 보기 권한</div>'; // 여기서 </div>를 추가
                }
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
function escapeHTML(html) {
    return html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
$(document).on("click", ".um_groupmore", function (e) {
    const xgroup_name = escapeHTML($(this).data("xgroup_name").toString());
    const id = $(this).data("id");
    const xuser_id_list = $(this).data("xuser_id_list");

    $.ajax({
        url: 'group_auth/',
        method:'POST',
        data:{
            id : id,
            xgroup_name: xgroup_name
        },
        success: function (res) {
            var data = res;
            //console.log(data)
            // AJAX 요청이 성공한 후에 modalbody를 설정하고 모달을 열기
            var modalbody = '<div>'+xgroup_name+' 권한</div>';
            modalbody += '<form id="authForm">';
            modalbody += '<input type="hidden" class="form-check-label" name="id" value="' + id + '">';
            modalbody += '<input type="hidden" class="form-check-label" name="xuser_id_list" value="' + xuser_id_list + '">';
            // data.auth_list 배열의 각 항목을 반복하며 체크박스 생성
            data.auth_list.sort(function (a, b) {
                // auth_list 배열을 auth_num 기준으로 정렬합니다.
                return a.xfactor_auth.auth_num - b.xfactor_auth.auth_num;
            });
            data.auth_list.forEach(function (authItem, index) {
                modalbody += '<label class="form-check-label">';
                modalbody += '<input class="form-check-input" type="checkbox" name="' + authItem.xfactor_auth.auth_id + '" value="' + authItem.auth_use + '"';

                if (authItem.auth_use === 'true') {
                    modalbody += ' checked';
                }
                modalbody += '> &nbsp;';
                modalbody += authItem.xfactor_auth.auth_name;
                modalbody += '</label><br>';
                if (index === 8) {
                    modalbody += '<br><div>'+xgroup_name+' 대시보드 보기 권한</div>'; // 여기서 </div>를 추가
                }
            });

            modalbody += '</form>';
            $("#um_auth_modal .hstbody").html(modalbody);
            $("#um_auth_modal").modal("show");


            //group페이지 권한 SAVE저장시 실행
            $(document).off("click", "#user_auth_save").on("click", "#user_auth_save", function (e) {
                e.preventDefault(); // 기본 폼 제출 동작을 막음
                var xuser_id_list_value = $('[name="xuser_id_list"]').val();
                var x_id_array = JSON.parse(xuser_id_list_value.replace(/'/g, '"'));
                var authInfo = [];
                //console.log(x_id_array)
                data.auth_list.forEach(function (authItem) {
                    const checkbox = $('[name="' + authItem.xfactor_auth.auth_id + '"]');
                    authInfo.push({
                        auth_id: authItem.xfactor_auth.auth_id,
                        auth_use: checkbox.is(":checked") ? 'true' : 'false'
                    });
                });
                //console.log(x_id_array)
                // 서버에 체크된 auth_ids와 x_id를 전달하여 DB에 저장 요청 보냄
                $.ajax({
                    url: 'save_group_auth/',
                    method: 'POST',
                    data: {
                        id : id,
                        xgroup_name : xgroup_name,
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
// function escapeHTML(html) {
//     return html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// }
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
                //console.log(x_id);
                if (!isNaN(x_id)) {
                    // If x_id is a numeric string (e.g., "1")
                    const x_group_id = x_id;
                    const xgroup_name = checkedItems[x_id];
                    modalbody += `
                        <label class="form-check-label" for="${x_group_id}">
                            <input type="hidden" class="delete_hidden" id="${x_group_id}" value="${x_group_id}">
                            <input type="hidden"  class="delete_hidden_group" value="${xgroup_name}">
                            ${escapeHTML(xgroup_name.toString())}
                        </label><br>`;
                    document.querySelector("#um_delete_modal .modal-title").innerText='그룹 삭제';

                } else {
                    // If x_id is a regular string (e.g., "Test Group")
                    document.querySelector("#um_delete_modal .modal-title").innerText='사용자 삭제';
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
    $("#um_insert_modal").modal("hide");
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
// auth 모달 닫기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#closeBtn4", function (e) {
    $("#group_alter_modal").modal("hide");
    GroupalterForm_auth.style.display = "none";
});
$(document).on("click", "#closeBtn5", function (e) {
    $("#group_insert_modal").modal("hide");
    GroupCreateForm_auth.style.display = "none";
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
//############################### User 추가하기 ###############################
$(document).on("click","#um_insert", function (e) {
    /////////////////USER 검색기능 버튼삽입
    var modalbody = `
                    <style>
                        .asset-input-group {
                            display: flex;
                            justify-content: center;
                        }
                        .asset-input-group input {
                            width: 20%; /* 검색창 너비를 조절하세요. */
                            margin-right: 10px; /* @ncsoft.com과의 간격을 조절하세요. */
                        }
                    </style>
                    <div class="asset-input-group">
                        <input type="search" class="asset-form-control" id="ncuser_search_result" placeholder="계정이나 이름을 입력하세요." style="width: 250px;">
                    </div>`;
    /////////////////사용자 목록 가져오기
    $.ajax({
        url: 'db_list/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            var nc_users = response.data;
            var userTable = "<table class='table'><thead><tr><th class='text-center'>계정</th><th class='text-center' style='width: 15%;'>이름</th><th class='text-center'>부서</th><th class='text-center' style='width: 15%;'>ADD</th></tr></thead><tbody>";
            for (var i = 0; i < nc_users.length; i++) {
                var nc_user = nc_users[i];
                var userId = nc_user.userId;
                var userName = nc_user.userName;
                var deptName = nc_user.deptName;
                var email = nc_user.email;
                userTable += `<tr>
                    <td class='text-center'>${userId}</td>
                    <td class='text-center'>${userName}</td>
                    <td class='text-center'>${deptName}</td>
                    <td class='text-center'><button id="user_add_btn" type="button" class="btn btn-outline-warning " data-userId="${userId}" data-userName="${userName}" data-deptName="${deptName}" data-email="${email}">추가</td>
                </tr>`;
            }
            userTable += "</tbody></table>";
            //////////////사용자 테이블을 modalbody에 추가
            modalbody += userTable;
            /////////////////모달바디 저장하여  html에 넣기
            $("#um_insert_modal .modal-title").html("USER 추가");
            $("#um_insert_modal .form-check").html(modalbody);
            $("#um_insert_modal").modal("show");
        }
    });
});

////////////////////////////검색한거로 USER 보이게
$(document).on("keyup", "#ncuser_search_result", function (e) {
    var searchText = $(this).val().toLowerCase(); // 입력된 검색어를 소문자로 변환
    var userRows = $("#um_insert_modal .form-check table tbody tr");

    userRows.each(function () {
        var x_id = $(this).find("td:first-child").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
        var x_name = $(this).find("td:nth-child(2)").text().toLowerCase();
        var shouldShow = searchText.length >= 3 && x_id.includes(searchText);
        var shouldShow1 = searchText.length >= 2 && x_name.includes(searchText);

        if ((searchText.length === 0 || shouldShow) || (searchText.length === 0 || shouldShow1)) {
            // 검색어가 3글자 이상이고 일치하는 경우 표시
            $(this).show();
        } else {
            // 그 외의 경우 숨김
            $(this).hide();
        }
    });
});


//###################### 유저 ADD 저장 하기 #################################
 ///////////////// 그룹 저장하기  /////////////////
$(document).on("click","#user_add_btn", function(e) {
    e.preventDefault(); // 기본 제출 동작을 막습니다.
    //console.log(this);
    const userId = $(this).data("userid");
    const userName = $(this).data("username");
    const deptName = $(this).data("deptname");
    const email = $(this).data("email");
    $.ajax({
    url: 'user_add/', // views.py 파일의 URL을 여기에 넣으세요.
    type: 'POST',
    dataType: 'json',
    data:  {
         'userId' : userId,
         'userName' : userName,
         'deptName' : deptName,
         'email' : email
    },

    success: function (response) {
    // response에 따른 처리 - 예: 경고창 띄우기
        if (response.result == "success") {
            alert("유저 추가 성공");
            $('#um_insert_modal').modal('hide');
            location.reload();

        } else {
            alert('실패 : ' + response.message);
        }
    },
    error: function(xhr, status, error) {
            alert('중복된 계정입니다');
        }
    });
});


//####################################유저 삭제하기 ##########################
$(document).on("click", "#user_delete", function (event) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.
    var x_ids = [];
    var x_groups = [];

    $(".delete_hidden").each(function () {
        var value = $(this).val(); // 각 hidden 요소의 값을 가져오기
        x_ids.push(value); // 값을 배열에 추가
    });
    var hasGroupItems = x_ids.some(function (id) {
        return !isNaN(id);
    });
    if (hasGroupItems) {
        $(".delete_hidden_group").each(function () {
            var value2 = $(this).val(); // 각 hidden 요소의 값을 가져오기
            x_groups.push(value2); // 값을 배열에 추가
        });
        console.log(x_groups)
        $.ajax({
            url: "/user_management/group_delete/", // 그룹 삭제를 처리하는 URL
            method: "POST",
            data: {
                'x_groups' : JSON.stringify(x_groups),
                'group_ids': x_ids.filter(id => !isNaN(id)).join(',')
            },
            success: function (response) {
                if (response.result === 'success') {
                    // 그룹 삭제 성공 처리
                    $("#user_delete").modal("hide");
                    alert("그룹이 삭제되었습니다.");
                    delete_modal.style.display = "none"
//                    window.location.href = "/user_management/"
                    um_groupbutton()
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
    } else {
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
    }



});
//############################################################################

function escapeSelector(s) {
    return s.replace(/([!"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~])/g, '\\$1');
}

//############################### Group 생성하기 ###############################
$(document).on("click","#um_creategroup", function (e){
    //console.log("aaa");
    $("#groupName_auth").val("");
    $("#groupDescription_auth").val("");
    const check_id = [];
    $("#group_insert_modal .form-check2").html('');
 /////////////////USER 검색기능 버튼삽입
    var modalbody =`<div class="asset-input-group justify-content-end">
                        <span class="fs-16px pb-2 pe-2">검색 : </span>
                        <input type="search" class="asset-form-control mb-2" id="user_search_result" placeholder="추가할 계정을 입력하세요">
                    </div>`;
 /////////////////사용자 목록 가져오기
    $.ajax({
        url: 'user_list/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            var users = response.data;
            var userTable = "<table class='table table-sm'><thead class='table-active'><tr><th>계정</th><th style='width: 20%;'>이름</th><th>부서</th><th style='width: 7%;'>ADD</th></tr></thead><tbody>";
            for (var i = 0; i < users.length; i++) {
                var user = users[i];
                var x_id = user.x_id;
                var x_name = user.x_name;
                var x_email = user.x_email;
                var x_auth = user.x_auth;
                userTable += `<tr>
                    <td>${x_id}</td>
                    <td>${x_name}</td>
                    <td>${x_auth}</td>
                    <td><input type="checkbox" class="user-checkbox" data-x-id="${x_id}"></td>
                </tr>`;
            }
            userTable += "</tbody></table>";
 /////////////////사용자 테이블을 modalbody에 추가
            modalbody += userTable;
            // ADD 부분의 체크박스 이벤트 처리
            var modalbody2
            $(document).off("change", ".user-checkbox");
            $(document).on("change", ".user-checkbox", function (e) {
                const x_id = $(this).data("x-id");
  /////////////// // 체크박스를 체크하면 x_id를 modalbody2에 추가
                if (this.checked) {
                        var newLine = '<div id="div_' + x_id  + '"><input class="form-check-input" type="checkbox" value="' + x_id + '" id="' + x_id  + '" checked><label class="form-check-label no-before ps-5px" for="' + x_id  + '">' + x_id  + '</label><br></div>';
                        $("#group_insert_modal .form-check2").append(newLine);
                }
 ///////////////// 체크박스를 해제하면 modalbody2에서 제거
                else if (!this.checked) {
                    $("#div_" + escapeSelector(x_id)).remove();
//                    $(`#group_insert_modal .form-check2 label[for=${x_id}]`).remove(); // 라벨도 제거
//                    $("#group_insert_modal .form-check2").find('br').last().remove();
                }
            });


            $(document).on('change', '.form-check-input', function() {
                var x_id = $(this).val();
                if (!this.checked) { // 체크박스가 해제된 경우
                    // 해당 체크박스를 #group_insert_modal .form-check2에서 제거
                    $("#div_" + escapeSelector(x_id)).remove();
                    $(".user-checkbox[data-x-id='" + escapeSelector(x_id) + "']").prop('checked', false);
                }
            });


 /////////////////검색하여 선택한  USER 추가하기

            for (const x_id in checkedItems) {
                modalbody2 += '<div id="div_'+x_id+'"><input class="form-check-input" type="checkbox" value="'+x_id+'" id="'+x_id+'" checked><label class="form-check-label" for="'+x_id+'">'+x_id+'</label><br></div>'
            }

 /////////////////모달바디 저장하여  html에 넣기
            $("#group_insert_modal .modal-title").html("그룹 생성");
            $("#group_insert_modal .form-check").html(modalbody);
            $("#group_insert_modal .form-check2").html(modalbody2);
            $("#group_insert_modal").modal("show");
        }
    });
});

////////////////////////////검색한거로 USER 보이게
$(document).on("keyup", "#user_search_result", function (e) {
    var searchText = $(this).val().toLowerCase(); // 입력된 검색어를 소문자로 변환
    var userRows = $("#group_insert_modal .form-check table tbody tr");

    userRows.each(function () {
        var x_id = $(this).find("td:first-child").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
        var x_username = $(this).find("td:nth-child(2)").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
        if (x_id.includes(searchText) || x_username.includes(searchText)) {
            // 검색어와 일치하는 경우 표시
            $(this).show();
        } else {
            // 일치하지 않는 경우 숨김
            $(this).hide();
        }
    });
});
 ///////////////// 그룹 저장하기  /////////////////
$(document).on("click","#group_insert", function(e) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.

//    const x_id = $(this).data("x_id");
//    console.log(x_id);


    var form = document.getElementById("GroupCreateForm_auth");
    //console.log(form)
    var xgroup_name = form.elements.groupName_auth.value;
    var xgroup_description = form.elements.groupDescription_auth.value;
    let xuserIds = []
    const xuserElements = $('#group_insert_modal .form-check2').find('.form-check-input');
    //console.log(xuserElements)
    xuserElements.each(function () {
        if ($(this).prop('checked')) {
            const x_id = $(this).attr("id");
            xuserIds.push(x_id);
        }
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
            $('[value="GROUP"]').click();
            $("#group_insert_modal .form-check2").empty();
            $("#group_insert_modal .form-check").empty();

        } else {
            alert('실패 : ' + response.message);
        }

    }



    });
});




//############################### Group 수정하기 ###############################
$(document).on("click",".um_groupalter", function (e){
    const id = $(this).data("id");
    const xgroup_name = $(this).data("xgroup_name");
    const xgroup_note = $(this).data("xgroup_note");
    //const id = $(this).data("id");
    const xuser_id_list = $(this).data("xuser_id_list");
    let xuser_id_array;

    if (xuser_id_list.length===0){
        xuser_id_array = [];
    }else{
        const cleanedString = xuser_id_list.replace(/[\[\]']/g, ' ');
        xuser_id_array = cleanedString.split(',').map(item => item.trim());
    };

    var modalbody = `<div class="asset-input-group justify-content-end">
                            <span class="fs-16px pb-2 pe-2">검색 : </span>
                        <input type="search" class="asset-form-control before-init mb-2" id="group_search_result" placeholder="추가할 계정을 입력하세요.">
                    </div>`;
    modalbody += '<input type="hidden" id="id" value="'+id+'">';

/////////////////////이미 체크된 유저도 리스트에 체크되어있게하기
    var selectedUsers = xuser_id_array;

//////////////////// 유저목록 가져오기
    $.ajax({
        url: 'user_list/',
        type: 'GET',
        dataType: 'json',

        success: function (response) {
            var users = response.data;
            var userTable = "<table class='table'><thead><tr><th>계정</th><th style='width: 20%;'>이름</th><th>부서</th><th style='width: 7%;'>ADD</th></tr></thead><tbody>";
            for (var i = 0; i < users.length; i++) {
                var user = users[i];
                var x_id = user.x_id;
                var x_name = user.x_name;
                var x_email = user.x_email;
                var x_auth = user.x_auth;
                var isChecked = selectedUsers.includes(x_id) ? 'checked' : '';
                userTable += `<tr>
                    <td>${x_id}</td>
                    <td>${x_name}</td>
                    <td>${x_auth}</td>
                    <td><input type="checkbox" class="user-checkbox" data-x-id="${x_id}" ${isChecked}></td>
                </tr>`;
            }
            userTable += "</tbody></table>";
 /////////////////사용자 테이블을 modalbody에 추가
            modalbody += userTable;
            var modalbody2="";
            $(document).off("change", ".user-checkbox");
            $(document).on("change", ".user-checkbox", function (e) {
            const x_id = $(this).data("x-id");
  /////////////// // 체크박스를 체크하면 x_id를 modalbody2에 추가
                if (this.checked) {
                        var newLine = '<div id="div_'+x_id+'"><input class="form-check-input" type="checkbox" value="' + x_id +  '" checked><label class="form-check-label" for="' + x_id  + '">' + x_id  + '</label><br></div>';
                        $("#group_alter_modal .form-check2").append(newLine);
                }
 ///////////////// 체크박스를 해제하면 modalbody2에서 제거
                else {
                    $("#div_" + escapeSelector(x_id)).remove();
                    $(`#group_alter_modal .form-check2 #${x_id}`).remove();
                    $(`#group_alter_modal .form-check2 label[for=${x_id}]`).remove();
                    //$(`#group_alter_modal .form-check2 label[for=${x_id}]`).remove();
//                    var nextBr = $(`#group_alter_modal .form-check2 label[for=${x_id}] + br`);
//                    if (nextBr.length > 0) {
//                        nextBr.remove();
//                    }
                }
            });

            $(document).on('change', '.form-check-input', function() {
                var x_id = $(this).val();
                if (!this.checked) { // 체크박스가 해제된 경우
                    // 해당 체크박스를 #group_insert_modal .form-check2에서 제거
                    $("#div_" + escapeSelector(x_id)).remove();
                    $(".user-checkbox[data-x-id='" + escapeSelector(x_id) + "']").prop('checked', false);
                }
            });

            for (const x_id of xuser_id_array) {
                if (x_id.trim() !== ''){
                    modalbody2 += '<div id="div_'+x_id+'"><input class="form-check-input" type="checkbox" value="'+x_id+'" id="'+x_id+'" checked><label class="form-check-label" for="'+x_id+'">'+x_id+'</label><br></div>'
                }
            }
            $("#groupNameAlter_auth").val(xgroup_name);
            $("#groupDescriptionAlter_auth").val(xgroup_note);
            $("#group_alter_modal .modal-title").html("그룹 수정 팝업창");
            $("#group_alter_modal .form-check").html(modalbody);
            $("#group_alter_modal .form-check2").html(modalbody2);
            $("#group_alter_modal").modal("show");
            }
    });
});

$(document).on("keyup", "#group_search_result", function (e) {
    var searchText = $(this).val().toLowerCase(); // 입력된 검색어를 소문자로 변환
    var userRows = $("#group_alter_modal .form-check table tbody tr");

    userRows.each(function () {
        var x_id = $(this).find("td:first-child").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
        if (x_id.includes(searchText)) {
            // 검색어와 일치하는 경우 표시
            $(this).show();
        } else {
            // 일치하지 않는 경우 숨김
            $(this).hide();
        }
    });
});
//######################### 그룹 수정 완료 ############################################
$(document).on("click","#group_alter", function(e) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.


    var form = document.getElementById("GroupalterForm_auth");
    var xgroup_name = form.elements.groupNameAlter_auth.value;
    var id = form.elements.id.value;
    //console.log(form)
    //console.log("aaa")
    var xgroup_description = form.elements.groupDescriptionAlter_auth.value;
    let xuserIds = []
    const xuserElements = $('#group_alter_modal .form-check2').find('.form-check-input');
    xuserElements.each(function () {
        if ($(this).prop('checked')) {
            const x_id = $(this).attr("value");
            xuserIds.push(x_id);
        }
    });

    $.ajax({
    url: 'groupalter_auth/', // views.py 파일의 URL을 여기에 넣으세요.
    type: 'POST',
    dataType: 'json',
    data:  {
         'id' : id,
         'xgroup_name' : xgroup_name,
         'xgroup_description' : xgroup_description,
         'xuserIds' : JSON.stringify(xuserIds),
    },

    success: function (response) {
        // if (response.None == 'None') {
        //         alert('값을 입력하세요')
        //         return
        //     }
    // response에 따른 처리 - 예: 경고창 띄우기
        if (response.success == "success") {
            alert(response.message);
            $('#group_alter_modal').modal('hide');
            $('a[value="GROUP"]').click();
            $("#group_alter_modal .form-check2").empty();
            $("#group_alter_modal .form-check").empty();
//            setTimeout(function() {
//            window.location.reload();
//            }, 1000); // 1000 밀리초 (1초) 후에 리로드
            //window.location.href = "/user_management/"; // 리다이렉트
            //um_group_list()
        } else {
            alert('실패 : ' + response.message);
        }
    }
    });
});


///////////////////////// 보너스 그룹권한 초기화할때 쓸꺼##################
$(document).on("click","#insertauth", function (e){
    $.ajax({
        url: 'insertauth/',
        type: 'get',
        dataType: 'json'
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





// /////////////////User 자동완성 기능
//            $('#user_search_result').autocomplete({
//                source: function(request, response) {
//                  $.ajax({
//                    url: 'search_box/',
//                    method: 'POST',
//                    data: {
//                      searchText: request.term
//                    },
//                    success: function(data){
//                      var autocompleteData = data.data.map(function(item) {
//                        return item.x_id;
//                      });
//                      response(autocompleteData);
//
//                    }
//                  });
//                },
//                minLength: 2  // 최소 문자 수 설정
//              });

// /////////////////검색하여 중복체크하고 없으면 오른쪽으로  USER 추가
//            $('#user_search').on('click', function(event) {
//                var searchInput = document.getElementById('user_search_result');
//                var inputValue = searchInput.value;
//                //searchPer(inputValue)
//                if (inputValue) {
//                    var isAlreadySelected = false;
//                    var xuserElements = $('#group_insert_modal .form-check2').find('.form-check-input');
//                    xuserElements.each(function () {
//                        if ($(this).val() === inputValue) { //하나씩체크해보기
//                            isAlreadySelected = true;
//                            return false;
//                        }
//                    });
//                    if (isAlreadySelected) {
//                        alert('이미 선택한 값입니다.');
//                    } else {
//  /////////////////USER 추가
//                        var newLine = '<input class="form-check-input" type="checkbox" value="' + inputValue + '" id="' + inputValue + '" checked><label class="form-check-label" for="' + inputValue + '">' + inputValue + '</label><br>';
//                        $("#group_insert_modal .form-check2").append(newLine);
//                        searchInput.value = '';
//                    }
//                }
//            });
