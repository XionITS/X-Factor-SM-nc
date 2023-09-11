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
                var computer_id = data.computer.computer_id;
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
                        1: 'computer.chassistype',
                        2: 'computer.os_simple',
                        3: 'computer.computer_name',
                        4: 'computer.ip_address',
                        5: 'computer.mac_address',
                        6: 'ext_chr',
                        7: '',
                        };
                data.filter = {
                    defaultColumn : defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input-sec_list').val(),
                    value2 : $('#sec_asset_list2_filter input[type="search"]').val(),
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
		    { data: 'computer.chassistype', title: '구분', searchable: true },
			{ data: 'computer.os_simple', title: 'OS', searchable: true },
            { data: 'computer.computer_name', title: '컴퓨터 이름', searchable: true },
			{ data: 'computer.ip_address', title: 'IPv4', searchable: true },
			{ data: 'computer.mac_address', title: 'MAC주소', searchable: true },
            { data: 'ext_chr', title: '확장프로그램' , searchable: true},
            { data: 'computer.sw_list', title: '소프트웨어' , searchable: true},
            { data: 'computer.hotfix', title: 'Hotfix' , searchable: true}
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(1)', row).html(index);
        },
		columnDefs: [
		    {targets: 0, width: "2%", orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_id = row.computer.computer_id;
		        return '<input type="checkbox" class="form-check-input" name="'+row.computer.computer_name+'" id="'+row.computer.computer_id+'" data-computer-id="' + computer_id + '" data-computer-name="' + row.computer.computer_name + '">'
		        }},
            {targets: 1, width: "3%",orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer.os_simple+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.security1+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.security2+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.security3+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
                return '<a class="extmore swmore-font" data-ext_chr="' + row.ext_chr +'" ' +
                    'data-ext_chr_ver="' + row.ext_chr_ver + '" data-ext_edg="' + row.ext_edg + '" data-ext_edg_ver="' + row.ext_edg_ver + '" ' +
                    'data-ext_fir="' + row.ext_fir +'" data-ext_fir_ver="' + row.ext_fir_ver +'" data-computer_name="' + row.computer.computer_name +'" >더보기</a>'}},
		    {targets: 8, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
                return '<a class="swListmore swmore-font" ' +
                    'data-computer_name="' + row.computer.computer_name + '" data-sw_list="' + row.computer.sw_list + '" data-sw_ver_list="' + row.computer.sw_ver_list + '" ' +
                    'data-sw_install="' + row.computer.sw_install + '">더보기</a>'}},
		    {targets: 9, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
                return '<a class="hotmore swmore-font" ' +
                    'data-computer_name="' + row.computer.computer_name + '" data-hotfix="' + row.computer.hotfix + '" data-hotfix_date="' + row.computer.hotfix_date + '">더보기</a>'}},
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

//-----------------------------------브라우저 확장 프로그램------------------------------------------------
    $(document).on("click",".extmore", function (e){

        const computer_name = $(this).data("computer_name");
        const extList1 = $(this).data("ext_chr").split('<br>');
        const extVer1 = $(this).data("ext_chr_ver").split('<br>');
        const extList2 = $(this).data("ext_edg").split('<br>');
        const extVer2 = $(this).data("ext_edg_ver").split('<br>');
        const extList3 = $(this).data("ext_fir").split('<br>');
        const extVer3= 	$(this).data("ext_fir_ver").split('<br>');

        let maxLength = Math.max(extList1.length, extList2.length, extList3.length);

        let tableHTML ='';
        for(let i=0; i<maxLength; i++){
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
        $("#ext_Modal .modal-title").html(computer_name+"의 브라우저 확장프로그램 및 버전");
        $("#ext_Modal .exttbody").html(tableHTML);
        //$("#swListModal .modal-body-2").html(swVerHTML);
        $("#ext_Modal").modal("show");

         // Input 상자 값에 따라 해당 값을 노란색으로 처리
        $("#searchInput_ext").on("input", function () {
            const searchValue = $(this).val().trim().toLowerCase();
            $("#ext_Modal .exttbody tr").each(function () {
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


//--------------------------핫픽스 목록-------------------------------
$(document).on("click",".hotmore", function (e){
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
    $("#hotModal .modal-title").html(computer_name+"의 Hotfix 리스트");
    $("#hotModal .hottbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#hotModal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput_hot").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        $("#hotModal .hottbody tr").each(function () {
            const rowData = $(this).text().toLowerCase();
            if (rowData.includes(searchValue)) {
                $(this).addClass("highlight");
            } else if(!rowData.includes(searchValue)) {
                $(this).removeClass("highlight");
            } else {
                $("#hotModal .hottbody").removeClass("highlight");
            }
        });
    });
});
    //-----------------------------------------------------------------------------------


    //-----------------------------------sw 설치된 프로그램------------------------------------------------
    $(document).on("click",".swListmore", function (e){

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
    $("#swList_Modal .modal-title").html(computer_name+"의 소프트웨어 및 버전");
    $("#swList_Modal .swListtbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#swList_Modal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        $("#pur_swListModal .hstbody tr").each(function () {
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
    $('#search-button-sec_list').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-sec_list').val().trim();

        performSearch(column, searchValue, sec_asset_list2_Data);
    });

    // 검색창 enter 작동
    $('#search-input-sec_list').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-sec_list').val().trim();

            performSearch(column, searchValue, sec_asset_list2_Data);
        }
    });

	$(document).on('click', '#nexts, #after', function() {
        var current_page = sec_asset_list2_Data.page();
        var total_pages = sec_asset_list2_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    sec_asset_list2_Data.page(current_page + 10).draw('page');
                } else {
                    sec_asset_list2_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    sec_asset_list2_Data.page(Math.max(current_page - 10, 0)).draw('page');
                }
    });

};

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
    sec_asset_list2();
    // checkbox_check($('#sec_asset_list tbody'))
    //initializeDataTable();
});