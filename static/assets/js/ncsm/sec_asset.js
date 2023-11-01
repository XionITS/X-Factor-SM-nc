/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/


// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};

var sec_asset_list = function () {
    var sec_asset_list_Data = $('#sec_asset_list').DataTable({
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
            $('#select-all').prop('checked', allCheckedOnCurrentPage);
            var current_page_sec = sec_asset_list_Data.page();
            var total_pages_sec = sec_asset_list_Data.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages_sec >= 1) { // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
                $('<button type="button" class="btn" id="nexts_sec">10≫</button>')
                    .insertAfter('#sec_asset_list_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after_sec">≪10</button>')
                    .insertBefore('#sec_asset_list_paginate .paginate_button:first');
            }

            var startPage = Math.floor(current_page_sec / 10) * 10;
            var endPage = startPage + 9;
            if (endPage > total_pages_sec - 1) {
                endPage = total_pages_sec - 1;
            }

            $('#sec_asset_list_paginate .paginate_button').not('.first, .last').remove();

            var maxButtons = 10;
            var halfWay = Math.floor(maxButtons / 2);

            if (current_page_sec < halfWay) {
                var startPage = 0;
                var endPage = Math.min(maxButtons - 1, total_pages_sec - 1);
            } else if ((current_page_sec + halfWay) > total_pages_sec) {
                var startPage = total_pages_sec - maxButtons;
                var endPage = total_pages_sec - 1;
            } else {
                var startPage = current_page_sec - halfWay;
                var endPage = current_page_sec + halfWay;
            }

            var oneButton = $('<button type="button" class="paginate_button btn">1</button>')
                .on('click', function() {
                    sec_asset_list_Data.page(0).draw(false);
                })
                .insertAfter('#after_sec')
                .css(current_page_sec == 0 ? {
                    'font-weight': 'bold',
                    'color': '#f39c12'
                } : {});

            if (startPage > 1) {
                $('<button type="button" class="paginate_button btn">...</button>')
                    .insertAfter(oneButton);
            }

            for (var i = startPage; i <= endPage; i++) {
                if (i == 0 || i == total_pages_sec - 1) continue;
                var btn = $('<button type="button" class="paginate_button btn"></button>').text(i + 1);
                if (i == current_page_sec) {
                    btn.addClass('current');
                    btn.css({
                        'font-weight': 'bold',
                        'color': '#f39c12'
                    });
                }
                btn.on('click', function() {
                    sec_asset_list_Data.page(parseInt($(this).text()) - 1).draw(false);
                });
                btn.insertBefore('#nexts_sec');
            }

            if (endPage < total_pages_sec - 2) {
                $('<button type="button" class="paginate_button btn">...</button>')
                    .insertBefore('#nexts_sec');
            }

            $('<button type="button" class="paginate_button btn">' + total_pages_sec + '</button>')
                .on('click', function() {
                    sec_asset_list_Data.page(total_pages_sec - 1).draw(false);
                })
                .insertBefore('#nexts_sec')
                .css(current_page_sec == (total_pages_sec - 1) ? {
                    'font-weight': 'bold',
                    'color': '#f39c12'
                } : {});

        },
        ajax: {
            url: 'paging/',
            type: "POST",
            data: function (data) {
                var defaultColumn = ''
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                //console.log(orderColumn)
                var orderDir = data.order[0].dir;
                var columnMap = {
                    1: 'chassistype',
                    2: 'os_simple',
                    3: 'logged_name_id__deptName',
                    4: 'logged_name_id__userName',
                    5: 'logged_name_id__userId',
                    6: 'computer_name',
                    7: 'security1',
                    8: 'security2',
                    9: 'security3',
                    10: 'security4',
                    11: 'security5',
                    13: 'cache_date',
                    14: 'memo'
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
            dataSrc: function (res) {
                $("#sec_total_list tbody").empty();
                var data = res.data;
                var countList = res.count_list;
                var tbody = $("#sec_total_list tbody");
                var row = '<tr>';
                for (var j = 0; j < countList.length; j++) {
                    var count = countList[j];
                    row += '<td>' + count + ' 개</td>';
                }
                tbody.append(row);
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
            {data: 'os_simple', title: 'OS', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{data: 'ncdb_data.userName', title: '이름', searchable: true },
	        {data: 'ncdb_data.userId', title: '계정', searchable: true },
            {data: 'computer_name', title: '컴퓨터 이름', searchable: true},
            {data: 'security1', title: 'Cososys', searchable: true},
            {data: 'security2', title: 'Symantec', searchable: true},
            {data: 'security3', title: 'CarbonBlack CBR', searchable: true},
            {data: 'security4', title: 'CarbonBlack CBC', searchable: true},
            {data: 'security5', title: 'McAfee VSE', searchable: true},
            {data: '', title: '더보기', searchable: true},
            {data: 'cache_date', title: '온/오프라인', searchable: true },
            {data: 'memo', title: '메모', searchable: true},
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
                    const computer_id = row.computer_id;
                    return '<input type="checkbox" class="form-check-input" name="' + row.computer_name + '" id="' + row.computer_id + '" data-computer-id="' + computer_id + '" data-computer-name="' + row.computer_name + '">'
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
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.os_simple + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 3, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.deptName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 4, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.userName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 5, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {var title = row.ncdb_data && row.ncdb_data.userId || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 6, width: "7%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
            {
                targets: 7,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.security1 + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 8,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.security2 + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 9,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.security3 + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 10,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.security4 + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 11,
                width: "5%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.security5 + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 12,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<a class="secmore swmore-font" data-cbr="' + row.security3 + '" ' +
                        'data-computer_name="' + row.computer_name + '" data-cososys="' + row.security1 + '" data-cososys_ver="' + row.security1_ver + '" ' +
                        'data-symantec="' + row.security2 + '" data-symantec_ver="' + row.security2_ver + '" data-cbr_ver="' + row.security3_ver + '" data-cbc="' + row.security4 + '" ' +
                        'data-cbc_ver="' + row.security4_ver + '" data-mcafee="' + row.security5 + '" data-mcafee_ver="' + row.security5_ver + '" data-ip_address="' + row.ip_address + '" data-mac_address="' + row.mac_address + '" data-os_total="' + row.os_total + '"> 더보기 </a>'
                }
            },
            {targets: 13, width: "5%", className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function(data, type, row) {
                    return '<span title="'+row.cache_date+'" data-toggle="tooltip">'+data+'</span>'}},
            {
                targets: 14,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
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
    $('#sec_asset_list').on('click', '#select-all', function () {
        var isChecked = $(this).prop('checked');

        $('#sec_asset_list tbody input[type="checkbox"]').each(function () {
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
     $('#sec_asset_list tbody').on('click', 'input[type="checkbox"]', function () {
        var isChecked = $(this).prop('checked');
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');

        if (isChecked) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }

        var allChecked = true;
        $('#sec_asset_list tbody input[type="checkbox"]').each(function () {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false;
            }
        });

        $('#select-all').prop('checked', allChecked);
    });

    $(document).on("click", ".secmore", function (e) {
        let swList = []
        let swVer = []
        if ($(this).data("cososys").trim() === "True") {
            swList.push('Cososys')
            swVer.push($(this).data("cososys_ver"))
        }
        if ($(this).data("symantec").trim() === 'True') {
            swList.push('symantec')
            swVer.push($(this).data("symantec_ver"))
        }
        if ($(this).data("cbr").trim() === 'True') {
            swList.push('CarbonBlack CBR')
            swVer.push($(this).data("cbr_ver"))
        }
        if ($(this).data("cbc").trim() === 'True') {
            swList.push('CarbonBlack CBC');
            swVer.push($(this).data("cbc_ver"))
        }
        if ($(this).data("mcafee").trim() === 'True') {
            swList.push('McAfee VSE')
            swVer.push($(this).data("mcafee_ver"))
        }

//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
        let tableHTML = "";
        $(this).data("computer_name").trim()
        //console.log(swList)
        // Generate the table HTML
        for (let i = 0; i < swList.length; i++) {
            const item = swList[i];
            const version = swVer[i];

            tableHTML += `
            <tr>
                <td scope="row" style="text-align: center">${item}</td>
                <td style="text-align: center">${version}</td>
            </tr>
        `;
        }
        $('.sectableCom .sectheadCom tr:nth-child(1) th:nth-child(2)').text($(this).data("computer_name").trim());
        $('.sectableCom .sectheadCom tr:nth-child(2) th:nth-child(2)').text($(this).data("ip_address").trim());
        $('.sectableCom .sectheadCom tr:nth-child(3) th:nth-child(2)').text($(this).data("mac_address").trim());
        $('.sectableCom .sectheadCom tr:nth-child(4) th:nth-child(2)').text($(this).data("os_total").trim());
        // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
        $("#secAssetModal .modal-title").html('보안솔루션 팝업창');
        $("#secAssetModal .sectbody").html(tableHTML);
        //$("#swListModal .modal-body-2").html(swVerHTML);
        $("#secAssetModal").modal("show");

        // Input 상자 값에 따라 해당 값을 노란색으로 처리
        // $("#searchInput-sec").on("input", function () {
        //     const searchValue = $(this).val().trim().toLowerCase();
        //     $("#secAssetModal .sectbody tr").each(function () {
        //         const rowData = $(this).text().toLowerCase();
        //         if (rowData.includes(searchValue)) {
        //             $(this).addClass("highlight");
        //         } else if(!rowData.includes(searchValue)) {
        //             $(this).removeClass("highlight");
        //         } else {
        //             $("#secAssetModal .sectbody").removeClass("highlight");
        //         }
        //     });
        // });
    });

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();
    checkbox_check($('#sec_asset_list tbody'))
    // row 선택시 체크박스 체크 및 해제
    // os_checkbox_check();

    // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-sec').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-sec').val().trim();

        performSearch(column, searchValue, sec_asset_list_Data);
    });

    // 검색창 enter 작동
    $('#search-input-sec').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-sec').val().trim();

            performSearch(column, searchValue, sec_asset_list_Data);
        }
    });

	$(document).on('click', '#nexts_sec, #after_sec', function() {
        var current_page_sec = sec_asset_list_Data.page();
        var total_pages_sec = sec_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec') {
            if (current_page_sec + 10 < total_pages_sec) {
                sec_asset_list_Data.page(current_page_sec + 10).draw('page');
            } else {
                sec_asset_list_Data.page(total_pages_sec - 1).draw('page');
            }
        } else {
            sec_asset_list_Data.page(Math.max(current_page_sec - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec, #after_sec {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
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
    sec_asset_list();
    // checkbox_check($('#sec_asset_list tbody'))
    //initializeDataTable();
});


