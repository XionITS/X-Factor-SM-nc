
var hw_asset_list = function () {
	var hs_asset_list_Data = $('#hs_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
		lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
		pageLength: 10,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,
        autoWidth: false,
        // buttons: [
        //     {
        //         text: 'Select All',
        //         className: 'ms-1',
        //         action: function () {
        //             hs_asset_list_Data.rows().select();
        //         }
        //     },
        //     {
        //         text: 'Select None',
        //         className: 'ms-1',
        //         action: function () {
        //             hs_asset_list_Data.rows().deselect();
        //         }
        //     }
        // ],
        select: true,
		ajax: {
			url: 'hwpaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                            1: 'logged_name_id__deptName',
                            2: 'logged_name_id__userName',
                            3: 'logged_name_id__userId',
                            4: 'computer_name',
                            5: 'ip_address',
                            6: 'mac_address',
                            8: 'cache_date',
                            9: 'memo',

                        };
                data.filter = {
                    column: column,
                    columnmap: columnMap[orderColumn],
                    direction: orderDir,
                    value : $('#search-input-hs').val(),
                    value2 : $('#hs_asset_list_filter input[type="search"]').val(),
                    regex : false, // OR 조건을 사용하지 않을 경우에는 false로 설정
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
//			{ data: 'chassistype', title: '구분', searchable: true },
			{ data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{ data: 'ncdb_data.userName', title: '이름', searchable: true },
			{ data: 'ncdb_data.userId', title: '계정', searchable: true },
			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
            { data: 'ip_address', title: 'IPv4' , searchable: true},
            { data: 'mac_address', title: 'MAC' , searchable: true},
			{ data: 'hw', title: '하드웨어 목록', searchable: true },
			{ data: 'cache_date', title: '온/오프라인', searchable: true },
//			{ data: 'hw_mb', title: 'Mainboard', searchable: true },
//			{ data: 'hw_ram', title: 'RAM', searchable: true },
//			{ data: 'hw_disk', title: 'DISK', searchable: true },
//			{ data: 'hw_gpu', title: 'VGA', searchable: true },
			{ data: 'memo', title: '메모', searchable: true },
		],
		rowCallback: function (row, data, index) {
            var api = this.api();
            var page = api.page.info().page;
            var pageLength = api.page.info().length;
            var index = (page * pageLength) + (index + 1);
            $('td:eq(0)', row).html(index);
        },
		columnDefs: [
            {targets: 0, width: "5%", orderable: false, searchable: false, className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 1, width: "15%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.deptName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 2, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.userName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 3, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {var title = row.ncdb_data && row.ncdb_data.userId || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 4, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.mac_address+'" data-toggle="tooltip">'+data+'</span>'}},
            {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_name = row.computer_name;
		        const hw_cpu = row.hw_cpu;
                const hw_mb = row.hw_mb;
                const hw_ram = row.hw_ram;
                const hw_disk = row.hw_disk;
                const hw_gpu = row.hw_gpu;
		        return '<span data-toggle="tooltip"></span><div class="hwmore swmore-font text-center new-text-truncate flex-cloumn align-middle " data-hw_cpu="' + hw_cpu + '" data-hw_mb="' + hw_mb + '"  data-hw_ram="' + hw_ram + '"  data-hw_disk="' + hw_disk + '"  data-hw_gpu="' + hw_gpu + '"data-computer_name="' + computer_name +'">더보기...</div>'}},
		    {targets: 8, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+data+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 9, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
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
         // row 전체 선택
//        buttons: [
//            {
//                text: 'Select all',
//                action: function (){
//                    hs_asset_list_Data.rows({page:'all'}).select();
//                }
//            },
//            {
//                text: 'Select none',
//                action: function (){
//                    hs_asset_list_Data.rows({page:'all'}).deselect();
//                }
//            },
//        ],
//        select: true,
        pagingType: 'numbers',//이전 다음 버튼 히든처리

        //페이징 10칸식 이동 로직
        drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination big-pagination'}).appendTo($pagination);

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
        }
});
      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
      $('.dropdown-menu a').click(function() {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
      });

  // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
$('#search-button-hs').click(function() {
    var column = $('#column-dropdown').data('column');
    var searchValue = $('#search-input-hs').val().trim();

    performSearch(column, searchValue, hs_asset_list_Data)
});

$('#search-input-hs').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-hs').val().trim();

            performSearch(column, searchValue, hs_asset_list_Data);
        }
    });

	$(document).on('click', '#nexts_hw, #after_hw', function() {
        var current_page_hw = hs_asset_list_Data.page();
        var total_pages_hw = hs_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_hw') {
                if (current_page_hw + 10 < total_pages_hw) {
                    hs_asset_list_Data.page(current_page_hw + 10).draw('page');
                } else {
                    hs_asset_list_Data.page(total_pages_hw - 1).draw('page');
                }
                } else {
                    hs_asset_list_Data.page(Math.max(current_page_hw - 10, 0)).draw('page');
                }
});
    var customStyle = '<style>#nexts_hw, #after_hw {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};


var sw_asset_list = function () {
	var sw_asset_list_Data = $('#hs_asset_list').DataTable({
		dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><''p>>",
		lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
        pageLength: 10,
		responsive: false,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,
        autoWidth: false,
		ajax: {
			url: 'swpaging/',
			type: "POST",
            data: function (data) {
                var column = $('#column-dropdown').data('column');
                var orderColumn = data.order[0].column;
                var orderDir = data.order[0].dir;
                var columnMap = {
                            1: 'logged_name_id__deptName',
                            2: 'logged_name_id__userName',
                            3: 'logged_name_id__userId',
                            4: 'computer_name',
                            5: 'ip_address',
                            6: 'mac_address',
                            8: 'cache_date',
                            9: 'memo',

                        };
                data.filter = {
                    column: column,
                    value : $('#search-input-hs').val(),
                    value2 : $('#hs_asset_list_filter input[type="search"]').val(),
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

//		columns: [
//		    { data: '', title: 'No', searchable: true },
//			{ data: 'chassistype', title: '구분', searchable: true },
//			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
//			{ data: 'logged_name', title: '사용자', searchable: true },
//            { data: 'ip_address', title: 'IPv4' , searchable: true},
//			{ data: 'sw_list', title: '소프트웨어 목록', searchable: true },
//			{ data: 'memo', title: '메모', searchable: true },
//
//		],
        columns: [
            { data: '', title: 'No', searchable: true },
//			{ data: 'chassistype', title: '구분', searchable: true },
			{ data: 'ncdb_data.deptName', title: '부서', searchable: true },
			{ data: 'ncdb_data.userName', title: '이름', searchable: true },
			{ data: 'ncdb_data.userId', title: '계정', searchable: true },
			{ data: 'computer_name', title: '컴퓨터 이름', searchable: true },
            { data: 'ip_address', title: 'IPv4' , searchable: true},
            { data: 'mac_address', title: 'MAC' , searchable: true},
            { data: 'sw', title: '소프트웨어 목록', searchable: true },
    //			{ data: 'hw_mb', title: 'Mainboard', searchable: true },
    //			{ data: 'hw_ram', title: 'RAM', searchable: true },
    //			{ data: 'hw_disk', title: 'DISK', searchable: true },
    //			{ data: 'hw_gpu', title: 'VGA', searchable: true },
            { data: 'cache_date', title: '온/오프라인', searchable: true },
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
            {targets: 0, width: "5%", orderable: false, searchable: false, className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
            {targets: 1, width: "15%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.deptName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 2, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) { var title = row.ncdb_data && row.ncdb_data.userName || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},
		    {targets: 3, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {var title = row.ncdb_data && row.ncdb_data.userId || ''; return '<span title="'+title+'" data-toggle="tooltip">'+title+'</span>'}},{targets: 4, width: "10%", className: 'sorting_asc text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 5, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 6, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.mac_address+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {
		        const computer_name = row.computer_name;
		        const swList = row.sw_list;
                const swVer = row.sw_ver_list;
		        return '<span data-toggle="tooltip"></span><div class="swmore swmore-font align-middle text-center " data-swlist="' + swList + '" data-swver="' + swVer + '" data-computer_name="' + computer_name +'">더보기...</div>'}},
            {targets: 8, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.cache_date+'" data-toggle="tooltip">'+data+'</span>'}},
		    {targets: 9, width: "10%", className: 'text-center new-text-truncate flex-cloumn align-middle', render: function(data, type, row) {
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
            pagingType: 'numbers',//이전 다음 버튼 히든처리

            //페이징 10칸식 이동 로직
            drawCallback: function (settings) {
            var api = this.api();
            var pageInfo = api.page.info();
            var $pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate');

            // 기존 페이지네이션 제거
            $pagination.empty();

            // 부트스트랩 페이징 컨테이너 생성
            var $ul = $('<ul>', {class: 'pagination big-pagination'}).appendTo($pagination);

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
        }
});

      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
      $('.dropdown-menu a').click(function() {
        var column = $(this).data('column');
        $('#column-dropdown').text($(this).text());
        $('#column-dropdown').data('column', column);
      });

      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
    $('#search-button-hs').click(function() {
    var column = $('#column-dropdown').data('column');
    var searchValue = $('#search-input-hs').val().trim();

    performSearch(column, searchValue, sw_asset_list_Data)
});

    $('#search-input-hs').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var column = $('#column-dropdown').data('column');
            var searchValue = $('#search-input-hs').val().trim();

            performSearch(column, searchValue, sw_asset_list_Data);
        }
    });

	$(document).on('click', '#nexts_sw, #after_sw', function() {
        var current_page_sw = sw_asset_list_Data.page();
        var total_pages_sw = sw_asset_list_Data.page.info().pages;
        if ($(this).attr('id') == 'nexts_sw') {
                if (current_page_sw + 10 < total_pages_sw) {
                    sw_asset_list_Data.page(current_page_sw + 10).draw('page');
                } else {
                    sw_asset_list_Data.page(total_pages_sw - 1).draw('page');
                }
                } else {
                    sw_asset_list_Data.page(Math.max(current_page_sw - 10, 0)).draw('page');
                }
});
    var customStyle = '<style>#nexts_sw, #after_sw {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
};



function hwbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>No</th><th>부서</th><th>이름</th><th>계정</th><th>컴퓨터 이름</th><th>IPv4</th><th>MAC</th><th>하드웨어 목록</th><th>온/오프라인</th><th>memo</th></tr></thead><tbody></tbody>';
    $('#hs_asset_list').DataTable().destroy();
    $('#hs_asset_list').html(newTableContent);
    hw_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');

}

function swbutton(btn) {
    let newTableContent = '';
    newTableContent = '<thead><tr class="table-active text-white text-opacity-75"><th>No</th><th>부서</th><th>이름</th><th>계정</th><th>컴퓨터 이름</th><th>IPv4</th><th>MAC</th><th>소프트웨어 목록</th><th>온/오프라인</th><th>memo</th></tr></thead><tbody></tbody>';
    $('#hs_asset_list').DataTable().destroy();
    $('#hs_asset_list').html(newTableContent);
    sw_asset_list();
    $(btn).addClass('active');
    $('.hsbutton').not(btn).removeClass('active');

}

//S/W 자산현황 더보기 정렬 기능
function sortTable(n) {
    var table = document.getElementById("hsTable");
    var tbody = table.querySelector(".hstbody");
    var rows = Array.from(tbody.querySelectorAll("tr"));
    var ascending = tbody.getAttribute("data-ascending") === "true";

    rows.sort((a, b) => {
        var textA = a.getElementsByTagName("TD")[n].innerText.toLowerCase();
        var textB = b.getElementsByTagName("TD")[n].innerText.toLowerCase();

        if (textA < textB) return ascending ? -1 : 1;
        if (textA > textB) return ascending ? 1 : -1;
        return 0;
    });

    ascending = !ascending;
    tbody.setAttribute("data-ascending", ascending.toString());

    rows.forEach(row => {
        tbody.appendChild(row);
    });
}


$(document).ready(function () {
    user_list_popup();
    hw_asset_list();
    //sidebar();
    //initEvent();

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
        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
        if (searchValue === "") {
            $("#swListModal .hstbody tr").removeClass("highlight");
            return;
        };
        $("#swListModal .hstbody tr").each(function () {
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


$(document).on("click",".hwmore", function (e){
    const computer_name = $(this).data("computer_name");
    const hw_cpu = $(this).data("hw_cpu");
    const hw_mb = $(this).data("hw_mb");
    const hw_ram = $(this).data("hw_ram");
    const hw_disk = $(this).data("hw_disk");
    const hw_gpu = $(this).data("hw_gpu");
//    swList2 = swList.split('<br>')
//    swVer2 = swVer.split('<br>')
//    const swListHTML = "<ul>" + swList2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
//    const swVerHTML = "<ul>" + swVer2.map(item => "<li>" + item + "</li>").join("") + "</ul>";
    //const combinedData = hw_cpu.map((item, index) => [item, hw_cpu[index]]);

    // Generate the table HTML
    const tableHTML = `
        <tr>
            <td class=text-center>CPU</td>
            <td class=text-center>${hw_cpu}</td>
        </tr>
        <tr>
            <td class=text-center>메인보드</td>
            <td class=text-center>${hw_mb}</td>
        </tr>
        <tr>
            <td class=text-center>RAM</td>
            <td class=text-center>${hw_ram}</td>
        </tr>
        <tr>
            <td class=text-center>디스크</td>
            <td class=text-center>${hw_disk}</td>
        </tr>
        <tr>
            <td class=text-center>그래픽카드</td>
            <td class=text-center>${hw_gpu}</td>
        </tr>

    `;



    //console.log(swVer[1]);
    // Assuming you have a modal with the ID "swListModal" to display the detailed sw_list
    $("#hwListModal .modal-title").html(computer_name+"의 하드웨어");
    $("#hwListModal .hstbody").html(tableHTML);
    //$("#swListModal .modal-body-2").html(swVerHTML);
    $("#hwListModal").modal("show");

     // Input 상자 값에 따라 해당 값을 노란색으로 처리
//    $("#searchInput2").on("input", function () {
//        const searchValue = $(this).val().trim().toLowerCase();
//        // 검색어가 빈 문자열일 경우 모든 행에서 highlight 클래스 제거 후 함수 종료
//        if (searchValue === "") {
//            $("#hwListModal .hstbody tr").removeClass("highlight");
//            return;
//        };
//        $("#hwListModal .hstbody tr").each(function () {
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