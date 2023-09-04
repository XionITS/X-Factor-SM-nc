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
		lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
		pageLength: 5,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,

		ajax: {
			url: 'pur_hwpaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                            1: 'chassistype',
                            2: 'computer_name',
                            3: 'ip_address',
                            4: 'first_network',
                            5: 'mem_use',
                            6: 'disk_use',
                            7: 'hw',
                            8: 'memo',

                        };
                data.filter = {
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input-hs').val(),
                    value2 : $('#hs_pur_asset_list_filter input[type="search"]').val(),
                    regex : false // OR 조건을 사용하지 않을 경우에는 false로 설정
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
            { data: '', title: 'No', searchable: true },
			{ data: 'computer.chassistype', title: '구분', searchable: true },
			{ data: 'computer.computer_name', title: '컴퓨터 이름', searchable: true },
            { data: 'computer.ip_address', title: 'IPv4' , searchable: true},
			{ data: 'computer.first_network', title: '최초 네트워크 접속일', searchable: true },
			{ data: 'mem_use', title: '메모리 사용률', searchable: true },
			{ data: 'disk_use', title: '디스크 사용률', searchable: true },
			{ data: 'hw', title: '부품 목록',
			    render:function(data,type,row){
			    return "CPU : "+row.computer.hw_cpu +"<br>메인보드 : "+row.computer.hw_mb+"<br>RAM : "+row.computer.hw_ram+"<br>디스크 : "+row.computer.hw_disk+"<br>VGA : "+row.computer.hw_vga;
			    },searchable: true},
			{ data: 'computer.memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
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
            {targets: 0, width: "3%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 1, width: "3%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.chassistype+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "10%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "5%", className: 'text-center text-truncate flex-cloumn column_hidden align-middle', render: function(data, type, row) {return '<span title="'+row.hw_cpu+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "3%", className: 'text-center text-truncate flex-cloumn column_hidden align-middle', render: function(data, type, row) {return '<span title="'+row.hw_mb+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "3%", className: 'text-center text-truncate flex-cloumn column_hidden align-middle', render: function(data, type, row) {return '<span title="'+row.hw_ram+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "20%", className: 'text-start text-truncate flex-cloumn column_hidden align-middle', render: function(data, type, row) {return '<span title="'+row.hw+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 8, width: "3%", className: 'text-center text-truncate flex-cloumn column_hidden align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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

      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

  // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-hs').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input-hs').val().trim();

        performSearch(column, searchValue, hw_pur_asset_list_Data)
    });

$('#search-input-hs').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-hs').val().trim();

            performSearch(column, searchValue, hw_pur_asset_list_Data);
        }
    });

$(document).on('click', '#nexts, #after', function() {
    var current_page = hw_pur_asset_list_Data.page();
    var total_pages = hw_pur_asset_list_Data.page.info().pages;
    if ($(this).attr('id') == 'nexts') {
            if (current_page + 10 < total_pages) {
                hw_pur_asset_list_Data.page(current_page + 10).draw('page');
            } else {
                hw_pur_asset_list_Data.page(total_pages - 1).draw('page');
            }
            } else {
                hw_pur_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
            }
});
};


var sw_pur_asset_list = function () {
	var sw_pur_asset_list = $('#hs_pur_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><''p>>",
		lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
        pageLength: 5,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,


		ajax: {
			url: 'pur_swpaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {

                            1: 'computer_name',
                            2: 'chassistype',
                            3: 'ip_address',
                            4: 'sw_list',
                            5: 'memo'

                        };
                data.filter = {
                    column: column,
                    value : $('#search-input-hs').val(),
                    value2 : $('#hs_pur_asset_list_filter input[type="search"]').val(),
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
		    { data: '', title: 'No', searchable: true },
			{ data: 'chassistype', title: '구분', searchable: true },
			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
            { data: 'ip_address', title: 'IPv4' , searchable: true},
			{ data: 'sw_list', title: '소프트웨어 목록', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },

		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
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
		    {targets: 0, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 1, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.chassistype+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "55%", className: 'text-start text-truncate flex-cloumn column_hidden', render: function(data, type, row) {
		        const computer_name = row.computer_name;
		        const swList = row.sw_list;
                const swVer = row.sw_ver_list;
		        return '<span data-toggle="tooltip">' + swList.split('<br>')[0]+'<br>'+swList.split('<br>')[1]+'<br>'+swList.split('<br>')[2]+'<br>'+swList.split('<br>')[3]+ '</span><br><div class="swmore swmore-font" data-swlist="' + swList + '" data-swver="' + swVer + '" data-computer_name="' + computer_name +'">더보기...</div>'}},
		    {targets: 5, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
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
    // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
    dropdown_text();

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-up').click(function() {
        var column = $('#column-dropdown').data('column');
        var searchValue = $('#search-input').val().trim();

        performSearch(column, searchValue, up_asset_list_Data);
    });

    // 검색창 enter 작동
    $('#search-input').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input').val().trim();

            performSearch(column, searchValue, up_asset_list_Data);
        }
    });

	$(document).on('click', '#nexts, #after', function() {
        var current_page = hs_pur_asset_list_Data.page();
        var total_pages = hs_pur_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    sw_pur_asset_list_Data.page(current_page + 10).draw('page');
                } else {
                    sw_pur_asset_list_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    sw_pur_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
                }
    });
};

function pur_hwbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>No</th><th>구분</th><th>컴퓨터 이름</th><th>IPv4</th><th>first_network</th><th>mem_use</th><th>disk_use</th><th>hw</th><th>메모</th></tr></thead><tbody></tbody>';
    $('#hs_pur_asset_list').DataTable().destroy();
    $('#hs_pur_asset_list').html(newTableContent);
    hw_pur_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
};

function pur_swbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>No</th><th>구분</th><th>컴퓨터 이름</th><th>IPv4</th><th>소프트웨어 목록</th><th>memo</th></tr></thead><tbody></tbody>';
    $('#hs_pur_asset_list').DataTable().destroy();
    $('#hs_pur_asset_list').html(newTableContent);
    sw_pur_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');
};

// 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
function dropdown_text(){
    $('.dropdown-menu a').click(function() {
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

$(document).on("click",".swmore", function (e){
    const computer_name = $(this).data("computer_name");
    const swList = $(this).data("swlist");
    const swVer = $(this).data("swver");
    swList2 = swList.split('<br>')
    swVer2 = swVer.split('<br>')
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
    const combinedData = swList2.map((item, index) => [item, swVer2[index]]);

    // Generate the table HTML
    const tableHTML = combinedData.map(([item, version]) => `
        <tr>
            <td scope="row">${item}</td>
            <td>${version}</td>
        </tr>
    `).join('');



    //console.log(swVer[1]);
    // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
    $("#swListModal .modal-title").html(computer_name+"의 소프트웨어 및 버전");
    $("#swListModal .hstbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#swListModal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
    $("#searchInput").on("input", function () {
        const searchValue = $(this).val().trim().toLowerCase();
        $("#swListModal .hstbody tr").each(function () {
            const rowData = $(this).text().toLowerCase();
            if (rowData.includes(searchValue)) {
                $(this).addClass("highlight");
            } else {
                $(this).removeClass("highlight");
            }
        });
    });
});

