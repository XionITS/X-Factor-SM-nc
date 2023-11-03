/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/


// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};

var all_asset_detail_list1 = function (categoryName, seriesName, selectedDate) {
    var all_asset_detail1_Data = $('#all_asset_detail1').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        // 기존 설정에 추가
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },

        ajax: {
            url: 'all_asset_paging1/',
            type: "POST",
            data: function (data) {
                data.seriesName = seriesName[0];
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'logged_name_id__deptName',
                    2: 'computer_name',
                    3: 'logged_name_id__userId',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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


};


// 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
function dropdown_text() {
    $('.dropdown-menu a').click(function () {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
    });
}

$(document).ready(function () {
    user_list_popup();
    // all_asset_detail_list1();
    // checkbox_check($('#sec_asset_list tbody'))
    //initializeDataTable();
});

var asset_os_detail_list1 = function (categoryName, seriesName, selectedDate) {
    var asset_os_detail_list1_Data = $('#asset_os_detail1').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'asset_os_paging1/',
            type: "POST",
            data: function (data) {
                data.seriesName = seriesName;
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = all_asset_detail1_Data.page();
        var total_pages_sec = all_asset_detail1_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var asset_os_detail_list2 = function (categoryName, seriesName, selectedDate) {
    var asset_os_detail_list2_Data = $('#asset_os_detail2').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'asset_os_paging2/',
            type: "POST",
            data: function (data) {
                data.seriesName = seriesName;
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = all_asset_detail1_Data.page();
        var total_pages_sec = all_asset_detail1_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var oslistPieChart_list = function (categoryName, seriesName, selectedDate) {
    var oslistPieChart_list_Data = $('#oslistPieChart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'oslistPieChart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = all_asset_detail1_Data.page();
        var total_pages_sec = all_asset_detail1_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};



var osVerPieChart_list = function (categoryName, seriesName, selectedDate) {
    var osVerPieChart_list_Data = $('#osVerPieChart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'osVerPieChart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = all_asset_detail1_Data.page();
        var total_pages_sec = all_asset_detail1_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};



var office_chart_list = function (categoryName, seriesName, selectedDate) {
    var office_chart_list_Data = $('#office_chart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'office_chart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();
    checkbox_check($('#sec_asset_list tbody'))
    // row 선택시 체크박스 체크 및 해제
    // os_checkbox_check();

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = office_chart_list_Data.page();
        var total_pages_sec = office_chart_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                office_chart_list_Data.page(current_page_sec + 10).draw('page');
            } else {
                office_chart_list_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};



var subnet_chart_list = function (categoryName, seriesName, selectedDate) {
    var subnet_chart_list_Data = $('#subnet_chart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'subnet_chart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();
    checkbox_check($('#sec_asset_list tbody'))
    // row 선택시 체크박스 체크 및 해제
    // os_checkbox_check();

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = subnet_chart_list_Data.page();
        var total_pages_sec = subnet_chart_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                subnet_chart_list_Data.page(current_page_sec + 10).draw('page');
            } else {
                subnet_chart_list_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            subet_chart_list_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var hotfix_chart_list = function (categoryName, seriesName, selectedDate) {
    var hotfix_chart_list_Data = $('#hotfix_chart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'hotfixChart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = all_asset_detail1_Data.page();
        var total_pages_sec = all_asset_detail1_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var tcpuChart_list = function (categoryName, seriesName, selectedDate) {
    var tcpuChart_list_Data = $('#tcpuChart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'tcpuChart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                     var title = row.ncdb_data && row.ncdb_data.deptName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    var title = row.ncdb_data && row.ncdb_data.userName || '';
                    return '<span title="' + title + '" data-toggle="tooltip">' + title + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + data + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = tcpuChart_list_Data.page();
        var total_pages_sec = tcpuChart_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var discoverChart_list = function (categoryName, seriesName, selectedDate) {
    var discoverChart_list_Data = $('#discoverChart').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [3, "asc"]
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination small-pagination'}).appendTo($pagination);

            // 첫 페이지 번호 버튼 생성
            if (pageInfo.page > 5) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === 0 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '1',
                        click: function () {
                            api.page(0).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // << 10 버튼 생성
            if (pageInfo.page > 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '<< 10',
                        click: function () {
                            api.page(pageInfo.page - 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 중앙 페이지네이션 생성
            var startPage = Math.max(0, pageInfo.page - 5);
            var endPage = Math.min(pageInfo.pages, pageInfo.page + 5);

            if (startPage > 0) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }
            for (var i = startPage; i < endPage; i++) {
                $('<li>', {
                    class: 'page-item' + (i === pageInfo.page ? ' active' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: i + 1,
                        click: function (event) {
                            api.page($(event.target).text() - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
            if (endPage < pageInfo.pages) {
                $('<li>', {class: 'page-item'}).append($('<span>', {class: 'page-link'}).text('...')).appendTo($ul);
            }

            // 10 >> 버튼 생성
            if (pageInfo.page < pageInfo.pages - 10) {
                $('<li>', {
                    class: 'page-item',
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: '10 >>',
                        click: function () {
                            api.page(pageInfo.page + 10).draw(false);
                        }
                    })
                }).appendTo($ul);
            }

            // 마지막 페이지 번호 버튼 생성
            if (pageInfo.page < pageInfo.pages - 6) {
                $('<li>', {
                    class: 'page-item' + (pageInfo.page === pageInfo.pages - 1 ? ' disabled' : ''),
                    html: $('<a>', {
                        class: 'page-link',
                        href: 'javascript:void(0)',
                        text: pageInfo.pages,
                        click: function () {
                            api.page(pageInfo.pages - 1).draw(false);
                        }
                    })
                }).appendTo($ul);
            }
        },
        ajax: {
            url: 'discoverChart/',
            type: "POST",
            data: function (data) {
                data.categoryName = categoryName;
                data.selectedDate = selectedDate;
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'deptName',
                    2: 'computer_name',
                    3: 'logged_name',
                    4: 'ip_address.',
                    5: 'mac_address',
                };
                //console.log(columnMap)
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec').val(),
                    value2: $('#sec_asset_list_filter input[type="search"]').val(),
                    regex: false // OR 조건을 사용하지 않을 경우에는 false로 설정
                };
                data.page = (data.start / data.length) + 1;
                data.page_length = data.length;
            },
        },

        columns: [
            {data: '', title: 'No', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true},
            {data: 'computer_name', title: '컴퓨터이름', searchable: true},
            {data: 'ncdb_data.userId', title: '사용자', searchable: true},
            {data: 'ip_address', title: 'IP', searchable: true},
            {data: 'mac_address', title: 'MAC', searchable: true},
            // {data: '', title: 'Email', searchable: true},
        ],
        rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
        columnDefs: [
            {
                targets: 0,
                width: "5%",
                orderable: false,
                searchable: false,
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 1,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.os_simple + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 2,
                width: "15%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.os_simple + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 4,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.security1 + '" data-toggle="tooltip">' + data + '</span>'
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

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = tcpuChart_list_Data.page();
        var total_pages_sec = tcpuChart_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                all_asset_detail1_Data.page(current_page_sec + 10).draw('page');
            } else {
                all_asset_detail1_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            all_asset_detail1_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};