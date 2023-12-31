/*
Template Name: HUD - Responsive Bootstrap 5 Admin Template
Version: 1.8.0
Author: Sean Ngu

*/



// 전역 변수로 체크박스 값을 저장할 객체를 생성합니다.
var checkedItems = {};

var os_asset_list = function () {
    var os_asset_list_Data = $('#os_asset_list').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
		lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
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
                    var computer_id = data.computer_id;

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
                        2: 'computer_name',
                        3: 'os_simple',
                        4: 'os_version',
                        5: 'ip_address',
                        6: 'mac_address',
                        7: 'memo'
                        };
                data.filter = {
                    defaultColumn : defaultColumn,
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input').val(),
                    value2 : $('#os_asset_list_filter input[type="search"]').val(),
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
            { data: 'computer_name', title: '컴퓨터 이름', searchable: true },
			{ data: 'os_simple', title: '구분', searchable: true },
            { data: 'os_version', title: '버전' , searchable: true},
			{ data: 'ip_address', title: 'IPv4', searchable: true },
			{ data: 'mac_address', title: 'Mac주소', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
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
		        const computer_id = row.computer_id;
		        return '<input type="checkbox" class="form-check-input" name="'+row.computer_name+'" id="'+row.computer_id+'" data-computer-id="' + computer_id + '" data-computer-name="' + row.computer_name + '">'
		        }},
            {targets: 1, width: "3%",orderable: false, searchable:false, className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 2, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 3, width: "15%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_simple+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 4, width: "25%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.os_version+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "15%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "15%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.mac_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
                if (data === null || data === undefined || data.trim() === '') { return '';
                } else {return '<span title="' + row.memo + '" data-toggle="tooltip">' + data + '</span>';}}},
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

    // row 선택시 체크박스 체크 및 해제
    // os_checkbox_check();

    // var column = $('#column-dropdown').data('column');
    // var searchValue = $('#search-input').val().trim();
    // // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    // $('#search-button').click(function() {
    //
    //     performSearch(column, searchValue, os_asset_list_Data);
    // });


	$(document).on('click', '#nexts, #after', function() {
        var current_page = os_asset_list_Data.page();
        var total_pages = os_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    os_asset_list_Data.page(current_page + 10).draw('page');
                } else {
                    os_asset_list_Data.page(total_pages - 1).draw('page');
                }
                } else {
                    os_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
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
    os_asset_list();
    //sidebar();
    //initEvent();
    checkbox_check($('#os_asset_list tbody'))


    //initializeDataTable();
});

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


