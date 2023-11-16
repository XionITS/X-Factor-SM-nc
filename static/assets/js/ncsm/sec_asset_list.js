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
                        const ext_chr = row.ext_chr.replace(/\"/g, "");
                        const ext_chr_ver = row.ext_chr_ver.replace(/\"/g, "");
                        const ext_edg = row.ext_edg.replace(/\"/g, "");
                        const ext_edg_ver = row.ext_edg_ver.replace(/\"/g, "");
                        const ext_fir = row.ext_fir.replace(/\"/g, "");
                        const ext_fir_ver = row.ext_fir_ver.replace(/\"/g, "");
                        return '<a class="extmore swmore-font" data-ext_chr="' + ext_chr + '"data-ext_chr_ver="' + ext_chr_ver + '" data-ext_edg="' + ext_edg + '" data-ext_edg_ver="' + ext_edg_ver + '"data-ext_fir="' + ext_fir + '" data-ext_fir_ver="' + ext_fir_ver + '" data-computer_name="' + row.computer_name + '" >더보기</a>'
                    }
                }
            },
            {
                targets: 11,
                width: "5%",
                className: 'text-center text-truncate flex-cloumn align-middle',
                render: function (data, type, row) {
                    const sw_list = row.sw_list.replace(/\"/g, "");
                    const sw_ver_list = row.sw_ver_list.replace(/\"/g, "");
                    const sw_install = row.sw_install.replace(/\"/g, "");
                    return '<a class="swListmore swmore-font" data-computer_name="' + row.computer_name + '" data-sw_list="' + sw_list + '" data-sw_ver_list="' + sw_ver_list + '"data-sw_install="' + sw_install + '">더보기</a>'
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
                var color = row.cache_date === "Online" ? "lime" : "red";
                return '<span title="'+row.cache_date+'" data-toggle="tooltip" style="color: ' + color + '; font-weight: bold;">'+data+'</span>';
              }},
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
        $('#searchInput_ext').val("");
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



        $(document).off("click", ".sortable").on("click", ".sortable", function (e) {
            const $table = $("#ext_Modal .exttbody");
            const $rows = $table.find("tr").toArray();
            const $th = $(this);
            const index = $th.index();
            const sortDirection = $th.data("sort") || 1;

            // 행 정렬
            $rows.sort(function (a, b) {
                const aText = $(a).find("td").eq(index).text();
                const bText = $(b).find("td").eq(index).text();
                if (index === 0 || index === 2 || index === 4) {
                    return aText.localeCompare(bText) * sortDirection;
                } else {
                    const aVersion = parseFloat(aText);
                    const bVersion = parseFloat(bText);
                    return (aVersion - bVersion) * sortDirection;
                }
            });

            // 정렬 순서 업데이트
            $table.empty().append($rows);
            $th.data("sort", sortDirection === 1 ? -1 : 1);
        });


    ////////////////////////////검색한거로 SW 보이게
    $(document).on("keyup", "#searchInput_ext", function (e) {
        var searchText = $(this).val().toLowerCase(); // 입력된 검색어를 소문자로 변환
        var userRows = $("#ext_Modal .exttable .exttbody tr");
        userRows.each(function () {
            var ext_chr = $(this).find("td:first-child").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var ext_edg = $(this).find("td:first-child").next().next().text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var ext_fir = $(this).find("td:first-child").next().next().next().next().text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var shouldShow_chr = searchText.length >= 2 && ext_chr.includes(searchText);
            var shouldShow_edg = searchText.length >= 2 && ext_edg.includes(searchText);
            var shouldShow_fir = searchText.length >= 2 && ext_fir.includes(searchText);

            if (searchText.length === 0 || shouldShow_chr ||shouldShow_edg || shouldShow_fir ) {
                // 검색어가 3글자 이상이고 일치하는 경우 표시
                $(this).show();
            } else {
                // 그 외의 경우 숨김
                $(this).hide();
            }
        });
    });
//        // Input 상자 값에 따라 해당 값을 노란색으로 처리
//        $("#searchInput_ext").on("input", function () {
//            const searchValue = $(this).val().trim().toLowerCase();
//            // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
//            if (searchValue === "") {
//                $("#ext_Modal .exttbody tr").removeClass("highlight");
//                return;
//            };
//            $("#ext_Modal .exttbody tr").each(function () {
//                const rowData = $(this).text().toLowerCase();
//                // 검색어가 rowData에 포함되면 highlight 클래스 추가
//                if (rowData.includes(searchValue)) {
//                    $(this).addClass("highlight");
//                }
//                // 포함되지 않으면 highlight 클래스 제거
//                else {
//                    $(this).removeClass("highlight");
//                }
//            });
//        });
    });
    //-----------------------------------------------------------------------------------


//--------------------------핫픽스 목록-------------------------------
    $(document).on("click", ".hotmore", function (e) {
        $('#searchInput_hot').val("");
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

        $(document).off("click", ".sortable").on("click", ".sortable", function (e) {
            const $table = $("#hotModal .hottbody");
            const $rows = $table.find("tr").toArray();
            const $th = $(this);
            const index = $th.index();
            const sortDirection = $th.data("sort") || 1;

            // 행 정렬
            $rows.sort(function (a, b) {
                const aText = $(a).find("td").eq(index).text();
                const bText = $(b).find("td").eq(index).text();
                if (index === 0) {
                    const aVersion = parseFloat(aText.replace(/KB/g, ''));
                    const bVersion = parseFloat(bText.replace(/KB/g, ''));
                    return (aVersion - bVersion) * sortDirection;
                } else if (index === 1) {
                    const aDate = new Date(aText);
                    const bDate = new Date(bText);
                    return (aDate - bDate) * sortDirection;
                }
            });

            // 정렬 순서 업데이트
            $table.empty().append($rows);
            $th.data("sort", sortDirection === 1 ? -1 : 1);
        });


    ////////////////////////////검색한거로 SW 보이게
    $(document).on("keyup", "#searchInput_hot", function (e) {
        var searchText = $(this).val().toLowerCase(); // 입력된 검색어를 소문자로 변환
        var userRows = $("#hotModal .hottable .hottbody tr");
        userRows.each(function () {
            var hotfix = $(this).find("td:first-child").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var hotfix_Date = $(this).find("td:first-child").next().text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var shouldShow = searchText.length >= 3 && hotfix.includes(searchText);
            var shouldShow_Date = searchText.length >= 3 && hotfix_Date.includes(searchText);

            if (searchText.length === 0 || shouldShow ||shouldShow_Date) {
                // 검색어가 3글자 이상이고 일치하는 경우 표시
                $(this).show();
            } else {
                // 그 외의 경우 숨김
                $(this).hide();
            }
        });
    });
//
//     // Input 상자 값에 따라 해당 값을 노란색으로 처리
//    $("#searchInput_hot").on("input", function () {
//        const searchValue = $(this).val().trim().toLowerCase();
//        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
//        if (searchValue === "") {
//            $("#hotModal .hottbody tr").removeClass("highlight");
//            return;
//        };
//        $("#hotModal .hottbody tr").each(function () {
//            const rowData = $(this).text().toLowerCase();
//            // 검색어가 rowData에 포함되면 highlight 클래스 추가
//            if (rowData.includes(searchValue)) {
//                $(this).addClass("highlight");
//            }
//            // 포함되지 않으면 highlight 클래스 제거
//            else {
//                $(this).removeClass("highlight");
//            }
//        });
//    });
});
    //-----------------------------------------------------------------------------------


    //-----------------------------------sw 설치된 프로그램------------------------------------------------
    $(document).on("click", ".swListmore", function (e) {
        $('#searchInput_swList').val("");
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

        $(document).off("click", ".sortable").on("click", ".sortable", function (e) {
            const $table = $("#swList_Modal .swListtbody");
            const $rows = $table.find("tr").toArray();
            const $th = $(this);
            const index = $th.index();
            const sortDirection = $th.data("sort") || 1;

            // 행 정렬
            $rows.sort(function (a, b) {
                const aText = $(a).find("td").eq(index).text();
                const bText = $(b).find("td").eq(index).text();
                if (index === 0) {
                    return aText.localeCompare(bText) * sortDirection;
                } else if (index === 2) {
                    // 처리할 N/A 값 확인
                    const naValue = "N/A";

                    // N/A 값 처리 및 정렬
                    if (aText === naValue && bText !== naValue) {
                        return 1 * sortDirection; // aText가 N/A이면 bText를 더 앞으로 보냄
                    } else if (aText !== naValue && bText === naValue) {
                        return -1 * sortDirection; // bText가 N/A이면 aText를 더 앞으로 보냄
                    } else if (aText === naValue && bText === naValue) {
                        return 0; // 둘 다 N/A이면 유지
                    } else {
                        // 일반적인 날짜 비교
                        const aDate = new Date(aText);
                        const bDate = new Date(bText);
                        return (bDate - aDate) * sortDirection;
                    }
                }
            });

            // 정렬 순서 업데이트
            $table.empty().append($rows);
            $th.data("sort", sortDirection === 1 ? -1 : 1);
        });


    ////////////////////////////검색한거로 SW 보이게
    $(document).on("keyup", "#searchInput_swList", function (e) {
        var searchText = $(this).val().toLowerCase(); // 입력된 검색어를 소문자로 변환
        var userRows = $("#swList_Modal .swListtable .swListtbody tr");
        userRows.each(function () {
            var swList = $(this).find("td:first-child").text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var swList_Ver = $(this).find("td:first-child").next().next().text().toLowerCase(); // 첫 번째 열의 텍스트를 가져와 소문자로 변환
            var shouldShow = searchText.length >= 2 && swList.includes(searchText);
            var shouldShow_Ver = searchText.length >= 2 && swList_Ver.includes(searchText);

            if (searchText.length === 0 || shouldShow ||shouldShow_Ver) {
                // 검색어가 3글자 이상이고 일치하는 경우 표시
                $(this).show();
            } else {
                // 그 외의 경우 숨김
                $(this).hide();
            }
        });
    });

//     // Input 상자 값에 따라 해당 값을 노란색으로 처리
//    $("#searchInput_swList").on("input", function () {
//        const searchValue = $(this).val().trim().toLowerCase();
//        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
//        if (searchValue === "") {
//            $("#swList_Modal .swListtbody tr").removeClass("highlight");
//            return;
//        };
//        $("#swList_Modal .swListtbody tr").each(function () {
//
//            const rowData = $(this).text().toLowerCase();
//            if (rowData.includes(searchValue)) {
//                $(this).addClass("highlight");
//            } else {
//                $(this).removeClass("highlight");
//            }
//        });
//    });
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
