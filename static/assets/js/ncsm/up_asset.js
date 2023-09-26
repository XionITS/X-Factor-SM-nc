/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/



// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};

var up_asset_list = function () {
    var up_asset_list_Data = $('#up_asset_list').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
        lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
        responsive: false,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [2, "desc"]
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
            var current_page_up = up_asset_list_Data.page();
            var total_pages_up = up_asset_list_Data.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages_up > 10) { // 페이지 수가 10개 이상일때  10칸이동버튼 활성화
                $('<button type="button" class="btn" id="nexts_up">10≫</button>')
                    .insertAfter('#up_asset_list_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after_up">≪10</button>')
                    .insertBefore('#up_asset_list_paginate .paginate_button:first');
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
                    2: 'chassistype',
                    3: 'computer_name',
                    4: 'mac_address',
                    5: 'ip_address',
                    6: 'hotfix',
                    7: 'hotfix_date',
                    8: 'memo'
                };
                data.filter = {
                    defaultColumn: defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value: $('#search-input-up').val(),
                    value2: $('#up_asset_list_filter input[type="search"]').val(),
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
            {data: 'computer_name', title: '컴퓨터 이름', searchable: true},
            {data: 'mac_address', title: 'Mac주소', searchable: true},
            {data: 'ip_address', title: 'IPv4', searchable: true},
            {data: 'hotfix', title: 'hotfix', searchable: true},
            {data: 'hotfix_date', title: '업데이트 날짜', searchable: true},
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
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.chassistype + '" data-toggle="tooltip">' + data + '</span>'
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
                    return '<span title="' + row.mac_address + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 5,
                width: "10%",
                className: 'text-center new-text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    return '<span title="' + row.ip_address + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {
                targets: 6,
                width: "10%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const computer_name = row.computer_name;
                    const hotfix = row.hotfix;
                    const date = row.hotfix_date;
                    if (row.hotfix === 'unconfirmed') {
                        return "";
                    } else {
                        return '<a class="upmore swmore-font" data-hotfix="' + hotfix + '" data-date="' + date + '" data-computer_name="' + computer_name + '">' + hotfix.split('<br>')[0] + '</a>'
                    }
                }
            },
            {
                targets: 7,
                width: "10%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const computer_name = row.computer_name;
                    const hotfix = row.hotfix;
                    const date = row.hotfix_date;
                    if (row.hotfix_date === 'unconfirmed') {
                        return "";
                    } else {
                        return '<a class="upmore swmore-font" data-date="' + date + '" data-hotfix="' + hotfix + '" data-computer_name="' + computer_name + '">' + date.split('<br>')[0] + '</a>'
                    }
                }
            },
            {
                targets: 8,
                width: "10%",
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
    $('#up_asset_list').on('click', '#select-all', function () {
        var isChecked = $(this).prop('checked');

        $('#up_asset_list tbody input[type="checkbox"]').each(function () {
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
    $('#up_asset_list tbody').on('click', 'input[type="checkbox"]', function () {
        var isChecked = $(this).prop('checked');
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');

        if (isChecked) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }

        var allChecked = true;
        $('#up_asset_list tbody input[type="checkbox"]').each(function () {
            if (!$(this).prop('checked')) {
                allChecked = false;
                return false;
            }
        });
        $('#select-all').prop('checked', allChecked);
    });


    $(document).on("click", ".upmore", function (e) {
        const computer_name = $(this).data("computer_name");
        const swList = $(this).data("hotfix");
        const swVer = $(this).data("date");
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
        $("#upAssetModal .modal-title").html(computer_name + "의 Hotfix 리스트");
        $("#upAssetModal .uptbody").html(tableHTML);
        //$("#swListModal .modal-body-2").html(swVerHTML);
        $("#upAssetModal").modal("show");

    // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
        if (searchValue === "") {
            $("#upAssetModal .uptbody tr").removeClass("highlight");
            return;
        };
        $("#upAssetModal .uptbody tr").each(function () {
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

    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

    // row 선택시 체크박스 체크 및 해제
    // os_checkbox_check();

    // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-up').click(function () {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-up').val().trim();

        performSearch(column, searchValue, up_asset_list_Data);
    });

    // 검색창 enter 작동
    $('#search-input-up').on('keyup', function (event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-up').val().trim();

            performSearch(column, searchValue, up_asset_list_Data);
        }
    });

    $(document).on('click', '#nexts_up, #after_up', function () {
        var current_page_up = up_asset_list_Data.page();
        var total_pages_up = up_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_up') {
            if (current_page_up + 10 < total_pages_up) {
                up_asset_list_Data.page(current_page_up + 10).draw('page');
            } else {
                up_asset_list_Data.page(total_pages_up - 1).draw('page');
            }
        } else {
            up_asset_list_Data.page(Math.max(current_page_up - 10, 0)).draw('page');
        }
    });
    var customStyle = '<style>#nexts_up, #after_up {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};




// function os_checkbox_check(){
//     console.log("os_checkbox_check() called");
//     $('#os_asset_list tbody').off('click', 'tr');
//     $('#os_asset_list tbody').on('click', 'tr', function () {
//         var checkbox = $(this).find('input[type="checkbox"]');
//         var hidden = $(this).find('input[type="hidden"]');
//         var computer_id = checkbox.attr('id');
//         console.log(computer_id)
//         checkbox.prop('checked', !checkbox.prop('checked'));
//         if (checkbox.prop('checked')) {
//             checkedItems[computer_id] = computer_id;
//         } else {
//             delete checkedItems[computer_id];
//         }
//     });
//
//     $('#os_asset_list tbody').on('click', 'input[type="checkbox"]', function (event) {
//         event.stopPropagation(); // Prevent the row click event from firing when clicking the checkbox
//         var computer_id = $(this).data('computer-id');
//         console.log("Clicked checkbox for computer ID:", computer_id);
//         console.log(computer_id)
//
//         if ($(this).prop('checked')) {
//             checkedItems[computer_id] = computer_id;
//         } else {
//             delete checkedItems[computer_id];
//         }
//     });
// }

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
    up_asset_list();
    checkbox_check($('#up_asset_list tbody'))
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


