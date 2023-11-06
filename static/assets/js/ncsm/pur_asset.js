/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/
// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};


var hw_pur_asset_list = function () {
    var hw_pur_asset_list_Data = $('#hs_pur_asset_list').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 5,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        autoWidth: false,
        order: [
            [3, "asc"]
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
                var computer_id = data.computer_id;

                if (checkedItems[computer_id]) {
                    $(row).find('input[type="checkbox"]').prop('checked', true);
                } else {
                    $(row).find('input[type="checkbox"]').prop('checked', false);
                    allCheckedOnCurrentPage = false; // 하나라도 체크되지 않은 체크박스가 있으면 전체선택 체크박스를 비활성화
                }
            }
            // 현재 페이지의 모든 체크박스가 선택된 경우에만
            // 전체 선택 체크박스를 활성화합니다.
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
            url: 'pur_hwpaging/',
            type: "POST",
            data: function (data) {
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                    2: 'chassistype',
                    3: 'logged_name_id__deptName',
                    4: 'logged_name_id__userName',
                    5: 'logged_name_id__userId',
                    6: 'computer_name',
                    7: 'ip_address',
                    8: 'first_network',
                    9: 'mem_use',
                    10: 'disk_use',
                    12: 'cache_date',
                    13: 'memo',

                };
                data.filter = {
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-pur').val(),
                    value2: $('#hs_pur_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
            dataSrc: function (res) {
                var data = res.data;
                console.log(data);
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
            {data: 'chassistype', title: '구분', searchable: true},
            { data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{ data: 'ncdb_data.userName', title: '이름', searchable: true },
			{ data: 'ncdb_data.userId', title: '계정', searchable: true },
            {data: 'computer_name', title: '컴퓨터 이름', searchable: true},
            {data: 'ip_address', title: 'IPv4', searchable: true},
            {data: 'first_network', title: '최초 네트워크 접속일', searchable: true},
            {data: 'mem_use', title: '메모리 사용률', searchable: true},
            {data: 'disk_use', title: '디스크 사용률', searchable: true},
            {
                data: 'hw', title: '부품 목록',
                render: function (data, type, row) {
                    return "CPU : " + row.hw_cpu + "<br>메인보드 : " + row.hw_mb + "<br>RAM : " + row.hw_ram + "<br>디스크 : " + row.hw_disk + "<br>VGA : " + row.hw_gpu;
                }, searchable: true
            },
            { data: 'cache_date', title: '온/오프라인', searchable: true },
            {data: 'memo', title: '메모', searchable: true},
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
                    const computer_id = row.computer_id;
                    return '<input type="checkbox" class="form-check-input" name="' + row.computer_name + '" id="' + row.computer_id + '" data-computer-id="' + row.computer_id + '" data-computer-name="' + row.computer_name + '">'
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
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 3, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.deptName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 4, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.userName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 5, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {var title = row.ncdb_data && row.ncdb_data.userId || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 6, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "7%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
            {
                targets: 8,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 9,
                width: "7%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 10,
                width: "7%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 11,
                width: "15%",
                className: 'text-start new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 12, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.cache_date+'" data-toggle="tooltip">'+data+'</span>'}},
            {
                targets: 13,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    if (data === null || data === undefined || data.trim() === '') {
                        return '';
                    } else {
                        return '<span title="' + row.memo + '" data-toggle="tooltip">' + data + '</span>';
                    }
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
    checkbox_check($('#hs_pur_asset_list tbody'))

    //전체선택
    $('#hs_pur_asset_list').on('click', '#select-all', function () {
        var isChecked = $(this).prop('checked');

        $('#hs_pur_asset_list tbody input[type="checkbox"]').each(function () {
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
    $('#hs_pur_asset_list tbody').on('click', 'input[type="checkbox"]', function () {
        var isChecked = $(this).prop('checked');
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');

        if (isChecked) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }

        var allChecked = true;
        $('#hs_pur_asset_list tbody input[type="checkbox"]').each(function () {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false;
            }
        });

        $('#select-all').prop('checked', allChecked);
    });

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

    // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-pur').click(function () {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-pur').val().trim();

        performSearch(column, searchValue, hw_pur_asset_list_Data);
    });

    // 검색창 enter 작동
    $('#search-input-pur').on('keyup', function (event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-pur').val().trim();
            performSearch(column, searchValue, hw_pur_asset_list_Data);
        }
    });


    $(document).on('click', '#nexts_hw_pur, #after_hw_pur', function () {
        var current_page_hw_pur = hw_pur_asset_list_Data.page();
        var total_pages_hw_pur = hw_pur_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_hw_pur') {
            if (current_page_hw_pur + 10 < total_pages_hw_pur) {
                hw_pur_asset_list_Data.page(current_page_hw_pur + 10).draw('page');
            } else {
                hw_pur_asset_list_Data.page(total_pages_hw_pur - 1).draw('page');
            }
        } else {
            hw_pur_asset_list_Data.page(Math.max(current_page_hw_pur - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_hw_pur, #after_hw_pur {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};

// ############### SW #############
var sw_pur_asset_list = function () {
    var sw_pur_asset_list = $('#hs_pur_asset_list').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><''p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 5,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        autoWidth: false,
        drawCallback: function (settings) {
            // 페이지 변경시 체크박스 값을 설정합니다.
            var api = this.api();
            var rows = api.rows({page: 'current'}).nodes();
            var allCheckedOnCurrentPage = rows.length > 0;


            // 현재 페이지의 체크박스 값을 확인하여 체크박스를 설정합니다.
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                var data = api.row(row).data();
                var computer_id = data.computer_id;


                if (checkedItems[computer_id]) {
                    $(row).find('input[type="checkbox"]').prop('checked', true);
                } else {
                    $(row).find('input[type="checkbox"]').prop('checked', false);
                    allCheckedOnCurrentPage = false; // 하나라도 체크되지 않은 체크박스가 있으면 전체선택 체크박스를 비활성화

                }
            }
            // 현재 페이지의 모든 체크박스가 선택된 경우에만
            // 전체 선택 체크박스를 활성화합니다.
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
            url: 'pur_swpaging/',
            type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                    2: 'chassistype',
                    3: 'logged_name_id__deptName',
                    4: 'logged_name_id__userName',
                    5: 'logged_name_id__userId',
                    6: 'computer_name',
                    7: 'ip_address',
                    12: 'cache_date',
                    13: 'memo',

                };
                data.filter = {
                    column: column,
                    value: $('#search-input-pur').val(),
                    value2: $('#hs_pur_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
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
            {
                data: '',
                title: '<input type="checkbox" class="form-check-input" id="select-all" /><span>&nbsp;선택</span>',
                searchable: false
            },
            {data: '', title: 'No', searchable: true},
            {data: 'chassistype', title: '구분', searchable: true},
            { data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{ data: 'ncdb_data.userName', title: '이름', searchable: true },
			{ data: 'ncdb_data.userId', title: '계정', searchable: true },
            {data: 'computer_name', title: '컴퓨터 이름', searchable: true},
            {data: 'ip_address', title: 'IPv4', searchable: true},
            {data: 'sw_list', title: '소프트웨어 목록', searchable: true},
            {data: 'sw_ver_list', title: '소프트웨어 버전', searchable: true},
            {data: 'sw_install', title: '설치 일자', searchable: true},
            {data: '', title: '더보기', searchable: false},
            { data: 'cache_date', title: '온/오프라인', searchable: true },
            {data: 'memo', title: '메모', searchable: true},

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
                    const computer_id = row.computer_id;
                    return '<input type="checkbox" class="form-check-input" name="' + row.computer_name + '" id="' + row.computer_id + '" data-computer-id="' + computer_id + '" data-computer-name="' + row.computer_name + '">'
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
                width: "3%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 3, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.deptName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 4, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.userName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 5, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {var title = row.ncdb_data && row.ncdb_data.userId || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 6, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "7%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},

            {
                targets: 8, width: "10%", className: 'text-start new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const swList = row.sw_list;
                    const swListArray = swList ? swList.split('<br>') : [];
                    return '<span data-toggle="tooltip">' + (swListArray[0] || '') + '<br>' + (swListArray[1] || '') + '<br>' + (swListArray[2] || '') + '<br>' + (swListArray[3] || '')
                }
            },

            {
                targets: 9, width: "10%", className: 'text-start new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    const swVer = row.sw_ver_list;
                    const swVerArray = swVer ? swVer.split('<br>') : [];
                    return '<span data-toggle="tooltip">' + (swVerArray[0] || '') + '<br>' + (swVerArray[1] || '') + '<br>' + (swVerArray[2] || '') + '<br>' + (swVerArray[3] || '')
                }
            },

            {
                targets: 10, width: "10%", className: 'text-start new-text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    const swInstall = row.sw_install;
                    const swInstallArray = swInstall ? swInstall.split('<br>') : [];
                    return '<span data-toggle="tooltip">' + (swInstallArray[0] || '') + '<br>' + (swInstallArray[1] || '') + '<br>' + (swInstallArray[2] || '') + '<br>' + (swInstallArray[3] || '')
                }
            },

            {
                targets: 11, width: "5%", className: 'text-start text-truncate flex-cloumn column_hidden align-middle',
                render: function (data, type, row) {
                    const computer_name = row.computer_name;
                    const swList = row.sw_list;
                    const swVer = row.sw_ver_list;
                    const swInstall = row.sw_install;
                    return '</span><br><div class="pur_swmore swmore-font" data-swlist="' + swList + '" data-swver="' + swVer + '" data-swinstall="' + swInstall + '" data-computer_name="' + computer_name + '">더보기...</div>'
                }
            },
            {targets: 12, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.cache_date+'" data-toggle="tooltip">'+data+'</span>'}},
            {
                targets: 13,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    if (data === null || data === undefined || data.trim() === '') {
                        return '';
                    } else {
                        return '<span title="' + row.memo + '" data-toggle="tooltip">' + data + '</span>';
                    }
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

    //전체선택
    $('#hs_pur_asset_list').on('click', '#select-all', function () {
        var isChecked = $(this).prop('checked');

        $('#hs_pur_asset_list tbody input[type="checkbox"]').each(function () {
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
    $('#hs_pur_asset_list tbody').on('click', 'input[type="checkbox"]', function () {
        var isChecked = $(this).prop('checked');
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');

        if (isChecked) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }

        var allChecked = true;
        $('#hs_pur_asset_list tbody input[type="checkbox"]').each(function () {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false;
            }
        });

        $('#select-all').prop('checked', allChecked);
    });
    //체크박스 저장하기
    checkbox_check($('#hs_pur_asset_list tbody'))

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();



    // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-pur').click(function () {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-pur').val().trim();

        performSearch(column, searchValue, sw_pur_asset_list);
    });

    // 검색창 enter 작동
    $('#search-input-ver').on('keyup', function (event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-pur').val().trim();

            performSearch(column, searchValue, sw_pur_asset_list);
        }
    });


    $(document).on('click', '#nexts_sw_pur, #after_sw_pur', function () {
        var current_page_sw_pur = sw_pur_asset_list.page();
        var total_pages_sw_pur = sw_pur_asset_list.page.info().pages;
        if ($(this).attr('id') == 'nexts_sw_pur') {
            if (current_page_sw_pur + 10 < total_pages_sw_pur) {
                sw_pur_asset_list.page(current_page_sw_pur + 10).draw('page');
            } else {
                sw_pur_asset_list.page(total_pages_sw_pur - 1).draw('page');
            }
        } else {
            sw_pur_asset_list.page(Math.max(current_page_sw_pur - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sw_pur, #after_sw_pur {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};

function pur_hwbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75 text-center"><th>선택</th><th>No</th><th>구분</th><th>부서</th><th>이름</th><th>계정</th><th>컴퓨터 이름</th><th>IPv4</th><th>최초 네트워크 접속일</th><th>메모리 사용률</th><th>디스크 사용률</th><th>부품목록</th><th>온/오프라인</th><th>메모</th></tr></thead><tbody></tbody>';
    $('#hs_pur_asset_list').DataTable().destroy();
    $('#hs_pur_asset_list').html(newTableContent);
    hw_pur_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
    checkedItems = {};
};

function pur_swbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75 text-center"><th>선택</th><th>No</th><th>구분</th><th>부서</th><th>이름</th><th>계정</th><th>컴퓨터 이름</th><th>IPv4</th><th>소프트웨어 목록</th><th>소프트웨어 버전</th><th>설치 일자</th><th>더보기</th><th>온/오프라인</th><th>메모</th></tr></thead><tbody></tbody>';
    $('#hs_pur_asset_list').DataTable().destroy();
    $('#hs_pur_asset_list').html(newTableContent);
    sw_pur_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
    checkedItems = {};
};

// 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
function dropdown_text() {
    $('.dropdown-menu a').click(function () {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
    });
};

$(document).ready(function () {
    user_list_popup();
    hw_pur_asset_list();
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

$(document).on("click", ".pur_swmore", function (e) {

    const computer_name = $(this).data("computer_name");
    const swList = $(this).data("swlist");
    const swVer = $(this).data("swver");
    let swInstall = $(this).data("swinstall");
    if (!swInstall || typeof swInstall !== "string") {
        swInstall = "";
    }

    pur_swList2 = swList.split('<br>');
    pur_swVer2 = swVer.split('<br>');
    let pur_swInstall2;
    if (typeof swInstall === "string") {
        pur_swInstall2 = swInstall.split('<br>').map(value => value.trim());
    } else {
        pur_swInstall2 = [];
    }
    //pur_swInstall2 = swInstall.split('<br>');
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
    //const combinedData = pur_swList2.map((item, index) => [item, pur_swVer2[index], pur_swInstall2[index]]);
    const combinedData = pur_swList2.map((item, index) => [item, pur_swVer2[index], pur_swInstall2[index] || ""]);

    // Generate the table HTML
    const tableHTML = combinedData.map(([item, version, install]) => `
        <tr>
            <td scope="row">${item}</td>
            <td>${version}</td>
            <td>${install}</td>
        </tr>
    `).join('');


    //console.log(swVer[1]);
    // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
    $("#pur_swListModal .modal-title").html(computer_name + "의 소프트웨어 및 버전");
    $("#pur_swListModal .hstbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#pur_swListModal").modal("show");

    // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
        if (searchValue === "") {
            $("#pur_swListModal .hstbody tr").removeClass("highlight");
            return;
        };
        $("#pur_swListModal .hstbody tr").each(function () {
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

