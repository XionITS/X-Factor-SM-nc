/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/


// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};

var sec_asset_list2 = function () {
    var sec_asset_list2_Data = $('#sec_asset_list2').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
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
            $('#select-all').prop('checked', allCheckedOnCurrentPage);
            var current_page_sec2 = sec_asset_list2_Data.page();
            var total_pages_sec2 = sec_asset_list2_Data.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages_sec2 >= 1) { // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
                $('<button type="button" class="btn" id="nexts_sec2">10≫</button>')
                    .insertAfter('#sec_asset_list2_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after_sec2">≪10</button>')
                    .insertBefore('#sec_asset_list2_paginate .paginate_button:first');
            }

            var startPage = Math.floor(current_page_sec2 / 10) * 10;
            var endPage = startPage + 9;
            if (endPage > total_pages_sec2 - 1) {
                endPage = total_pages_sec2 - 1;
            }

            $('#sec_asset_list2_paginate .paginate_button').not('.first, .last').remove();

            var maxButtons = 10;
            var halfWay = Math.floor(maxButtons / 2);

            if (current_page_sec2 < halfWay) {
                var startPage = 0;
                var endPage = Math.min(maxButtons - 1, total_pages_sec2 - 1);
            } else if ((current_page_sec2 + halfWay) > total_pages_sec2) {
                var startPage = total_pages_sec2 - maxButtons;
                var endPage = total_pages_sec2 - 1;
            } else {
                var startPage = current_page_sec2 - halfWay;
                var endPage = current_page_sec2 + halfWay;
            }

            var oneButton = $('<button type="button" class="paginate_button btn">1</button>')
                .on('click', function() {
                    sec_asset_list2_Data.page(0).draw(false);
                })
                .insertAfter('#after_sec2')
                .css(current_page_sec2 == 0 ? {
                    'font-weight': 'bold',
                    'color': '#f39c12'
                } : {});

            if (startPage > 1) {
                $('<button type="button" class="paginate_button btn">...</button>')
                    .insertAfter(oneButton);
            }

            for (var i = startPage; i <= endPage; i++) {
                if (i == 0 || i == total_pages_sec2 - 1) continue;
                var btn = $('<button type="button" class="paginate_button btn"></button>').text(i + 1);
                if (i == current_page_sec2) {
                    btn.addClass('current');
                    btn.css({
                        'font-weight': 'bold',
                        'color': '#f39c12'
                    });
                }
                btn.on('click', function() {
                    sec_asset_list2_Data.page(parseInt($(this).text()) - 1).draw(false);
                });
                btn.insertBefore('#nexts_sec2');
            }

            if (endPage < total_pages_sec2 - 2) {
                $('<button type="button" class="paginate_button btn">...</button>')
                    .insertBefore('#nexts_sec2');
            }

            $('<button type="button" class="paginate_button btn">' + total_pages_sec2 + '</button>')
                .on('click', function() {
                    sec_asset_list2_Data.page(total_pages_sec2 - 1).draw(false);
                })
                .insertBefore('#nexts_sec2')
                .css(current_page_sec2 == (total_pages_sec2 - 1) ? {
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
                var orderDir = data.order[0].dir;
                var columnMap = {
                    2: 'chassistype',
                    3: 'os_simple',
                    4: 'logged_name_id__deptName',
                    5: 'logged_name_id__userName',
                    6: 'logged_name_id__userId',
                    7: 'computer_name',
                    8: 'ip_address',
                    9: 'mac_address',
                    10: 'ext_chr',
                    11: 'sw_list',
                    12: 'hotfix',
                    13: 'cache_date',
                    14: 'memo',
                };
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-sec_list').val(),
                    value2: $('#sec_asset_list2_filter input[type="search"]').val(),
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
            {data: 'os_simple', title: 'OS', searchable: true},
            {data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{data: 'ncdb_data.userName', title: '이름', searchable: true },
	        {data: 'ncdb_data.userId', title: '계정', searchable: true },
            {data: 'computer_name', title: '컴퓨터 이름', searchable: true},
            {data: 'ip_address', title: 'IPv4', searchable: true},
            {data: 'mac_address', title: 'MAC주소', searchable: true},
            {data: 'ext_chr', title: '확장프로그램', searchable: true},
            {data: 'sw_list', title: '소프트웨어', searchable: true},
            {data: 'hotfix', title: 'Hotfix', searchable: true},
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
        columnDefs: [
            {
                targets: 0,
                width: "4%",
                orderable: false,
                searchable: false,
                className: 'text-center text-truncate flex-cloumn align-middle',
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
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.index + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 2,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.chassistype + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 3,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.os_simple + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 4, width: "7%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.deptName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 5, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.userName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 6, width: "5%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {var title = row.ncdb_data && row.ncdb_data.userId || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 7, width: "7%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 8, width: "7%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 9, width: "7%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.mac_address+'" data-toggle="tooltip">'+data+'</span>'}},
            {
                targets: 10,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    if (row.ext_chr === 'unconfirmed' && row.ext_edg === 'unconfirmed' && row.ext_fir === 'unconfirmed') {
                        return '';
                    } else {
                        return '<a class="extmore swmore-font" data-ext_chr="' + row.ext_chr + '" ' +
                            'data-ext_chr_ver="' + row.ext_chr_ver + '" data-ext_edg="' + row.ext_edg + '" data-ext_edg_ver="' + row.ext_edg_ver + '" ' +
                            'data-ext_fir="' + row.ext_fir + '" data-ext_fir_ver="' + row.ext_fir_ver + '" data-computer_name="' + row.computer_name + '" >더보기</a>'
                    }
                }
            },
            {
                targets: 11,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<a class="swListmore swmore-font" ' +
                        'data-computer_name="' + row.computer_name + '" data-sw_list="' + row.sw_list + '" data-sw_ver_list="' + row.sw_ver_list + '" ' +
                        'data-sw_install="' + row.sw_install + '">더보기</a>'
                }
            },
            {
                targets: 12,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    if (row.hotfix === 'not apply') {
                        return "";
                    } else {
                        return '<a class="hotmore swmore-font" ' +
                            'data-computer_name="' + row.computer_name + '" data-hotfix="' + row.hotfix + '" data-hotfix_date="' + row.hotfix_date + '">더보기</a>'
                    }
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
    $('#sec_asset_list2').on('click', '#select-all', function () {
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
    $('#sec_asset_list2 tbody').on('click', 'input[type="checkbox"]', function () {
        var isChecked = $(this).prop('checked');
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');

        if (isChecked) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }

        var allChecked = true;
        $('#sec_asset_list2 tbody input[type="checkbox"]').each(function () {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false;
            }
        });

        $('#select-all').prop('checked', allChecked);
    });


//-----------------------------------브라우저 확장 프로그램------------------------------------------------
    $(document).on("click", ".extmore", function (e) {

        const computer_name = $(this).data("computer_name");
        const extList1 = $(this).data("ext_chr").split('<br>');
        const extVer1 = $(this).data("ext_chr_ver").split('<br>');
        const extList2 = $(this).data("ext_edg").split('<br>');
        const extVer2 = $(this).data("ext_edg_ver").split('<br>');
        const extList3 = $(this).data("ext_fir").split('<br>');
        const extVer3 = $(this).data("ext_fir_ver").split('<br>');

        let maxLength = Math.max(extList1.length, extList2.length, extList3.length);

        let tableHTML = '';
        for (let i = 0; i < maxLength; i++) {
            const rowHTML =
                `<tr>
                    <td scope="row" style="text-align: center">${extList1[i] || ''}</td>
                    <td style="text-align: center">${extVer1[i] || ''}</td>
                    <td scope="row" style="text-align: center">${extList2[i] || ''}</td>
                    <td style="text-align: center">${extVer2[i] || ''}</td>
                    <td scope="row" style="text-align: center">${extList3[i] || ''}</td>
                    <td style="text-align: center">${extVer3[i] || ''}</td>
                </tr>`;
            tableHTML += rowHTML;
        }



        //console.log(swVer[1]);
        // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
        $("#ext_Modal .modal-title").html(computer_name + "의 브라우저 확장프로그램 및 버전");
        $("#ext_Modal .exttbody").html(tableHTML);
        //$("#swListModal .modal-body-2").html(swVerHTML);
        $("#ext_Modal").modal("show");

        // Input 상자 값에 따라 해당 값을 노란색으로 처리
        $("#searchInput_ext").on("input", function () {
            const searchValue = $(this).val().trim().toLowerCase();
            // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
            if (searchValue === "") {
                $("#ext_Modal .exttbody tr").removeClass("highlight");
                return;
            };
            $("#ext_Modal .exttbody tr").each(function () {
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
    //-----------------------------------------------------------------------------------


//--------------------------핫픽스 목록-------------------------------
    $(document).on("click", ".hotmore", function (e) {
        const computer_name = $(this).data("computer_name");
        const swList = $(this).data("hotfix");
        const swVer = $(this).data("hotfix_date");
        swList2 = swList.split('<br>')
        swVer2 = swVer.split('<br>')
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
        const combinedData = swList2.map((item, index) => [item, swVer2[index]]);

        // Generate the table HTML
        const tableHTML = combinedData.map(([item, version]) => `
        <tr>
            <td scope="row" style="text-align: center">${item}</td>
            <td style="text-align: center">${version}</td>
        </tr>
    `).join('');


        //console.log(swVer[1]);
        // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
        $("#hotModal .modal-title").html(computer_name + "의 Hotfix 리스트");
        $("#hotModal .hottbody").html(tableHTML);
        //$("#swListModal .modal-body-2").html(swVerHTML);
        $("#hotModal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput_hot").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
        if (searchValue === "") {
            $("#hotModal .hottbody tr").removeClass("highlight");
            return;
        };
        $("#hotModal .hottbody tr").each(function () {
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
    //-----------------------------------------------------------------------------------


    //-----------------------------------sw 설치된 프로그램------------------------------------------------
    $(document).on("click", ".swListmore", function (e) {

        const computer_name = $(this).data("computer_name");
        const swList = $(this).data("sw_list");
        const swVer = $(this).data("sw_ver_list");
        let swInstall = $(this).data("sw_install");
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
            <td scope="row" style="text-align: center">${item}</td>
            <td style="text-align: center">${version}</td>
            <td style="text-align: center">${install}</td>
        </tr>
    `).join('');


        //console.log(swVer[1]);
        // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
        $("#swList_Modal .modal-title").html(computer_name + "의 소프트웨어 및 버전");
        $("#swList_Modal .swListtbody").html(tableHTML);
        //$("#swListModal .modal-body-2").html(swVerHTML);
        $("#swList_Modal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput_swList").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
        if (searchValue === "") {
            $("#swList_Modal .swListtbody tr").removeClass("highlight");
            return;
        };
        $("#swList_Modal .swListtbody tr").each(function () {

            const rowData = $(this).text().toLowerCase();
            if (rowData.includes(searchValue)) {
                $(this).addClass("highlight");
            } else {
                $(this).removeClass("highlight");
            }
        });
    });
});
    //-----------------------------------------------------------------------------------

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();
    checkbox_check($('#sec_asset_list2 tbody'))
    // row 선택시 체크박스 체크 및 해제
    // os_checkbox_check();

    // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-sec_list').click(function () {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-sec_list').val().trim();

        performSearch(column, searchValue, sec_asset_list2_Data);
    });

    // 검색창 enter 작동
    $('#search-input-sec_list').on('keyup', function (event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-sec_list').val().trim();

            performSearch(column, searchValue, sec_asset_list2_Data);
        }
    });

    $(document).on('click', '#nexts_sec2, #after_sec2', function () {
        var current_page_sec2 = sec_asset_list2_Data.page();
        var total_pages_sec2 = sec_asset_list2_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sec2') {
            if (current_page_sec2 + 10 < total_pages_sec2) {
                sec_asset_list2_Data.page(current_page_sec2 + 10).draw('page');
            } else {
                sec_asset_list2_Data.page(total_pages_sec2 - 1).draw('page');
            }
        } else {
            sec_asset_list2_Data.page(Math.max(current_page_sec2 - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_sec2, #after_sec2 {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
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
    sec_asset_list2();
    // checkbox_check($('#sec_asset_list tbody'))
    //initializeDataTable();
});
