///*
//Template Name: HUD - Responsive Bootstrap 5 Admin Template
//Version: 1.8.0
//Author: Sean Ngu
//
//*/

//var asset_list = function () {
//	var asset_list_Data = $('#asset_table').DataTable({
//		dom: "<'d-flex justify-content-between mb-3'<'col-md-0 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-0 mb-md-0 mt-n2 'i><'mb-0 col-md-0'p>>",
//		responsive: false,
//		serverSide: true,
//		displayLength: false,
//
//		ajax: {
//			url: 'search/',
//			type: "POST",
////            data: function (data) {
////                var column = $('#column-dropdown').data('column');
////                var orderColumn = data.order[0].column;
////                var orderDir = data.order[0].dir;
////                var columnMap = {
////                            1: 'computer_id',
////                            2: 'computer_name',
////                            3: 'memo',
////                            4: 'ip_address',
////                            5: 'hw_mb',
////                            6: 'hw_ram',
////                            7: 'hw_disk',
////                            8: 'hw_gpu',
////                            9: 'memo'
////
////                        };
////                data.filter = {
////                    column: column,
////                    columnmap: columnMap[orderColumn],
////                    direction: orderDir,
////                    value : $('#search-input-hs').val(),
////                    value2 : $('#hs_asset_list_filter input[type="search"]').val(),
////                    regex : false // OR 조건을 사용하지 않을 경우에는 false로 설정
////                };
////                data.page = (data.start / data.length) + 1;
////                data.page_length = data.length;
////            },
//			dataSrc: function (res) {
//				var data = res.data;
//				return data;
//			}
//		},
//
//		columns: [
//            { data: 'computer_name', title: '컴퓨터 이름', searchable: true },
//			{ data: 'computer_id', title: '사용자', searchable: true },
//			{ data: 'memo', title: '메모', searchable: true },
//            { data: 'ip_address', title: 'IP 주소' , searchable: true},
//            { data: 'mac_address', title: 'MAC 주소' , searchable: true},
//			{ data: 'os_total', title: 'OS 정보', searchable: true },
//			{ data: 'os_build', title: 'OS 버전', searchable: true },
//			{ data: 'office.', title: 'Office 버전', searchable: true },
//			{ data: 'ram_use', title: '메모리 사용률', searchable: true },
//			{ data: 'disk_use', title: '디스크 사용률', searchable: true },
//			{ data: 'hw_cpu', title: 'CPU', searchable: true },
//			{ data: 'hw_ram', title: 'RAM', searchable: true },
//			{ data: 'hw_mb', title: '메인보드', searchable: true },
//			{ data: 'hw_disk', title: '디스크', searchable: true },
//			{ data: 'hw_gpu', title: '그래픽카드', searchable: true },
//
//		],
////		rowCallback: function (row, data, index) {
////            var api = this.api();
////            var page = api.page.info().page;
////            var pageLength = api.page.info().length;
////            var index = (page * pageLength) + (index + 1);
////            $('td:eq(0)', row).html(index);
////        },
////        columnDefs: [
////		    {targets: 0, width: "10%", className: 'text-start text-truncate'},
////		    {targets: 1, width: "20%", className: 'text-start text-truncate'},
////		    {targets: 2, width: "10%", className: 'text-start text-truncate'},
////            {targets: 3, width: "10%", className: 'text-start text-truncate'},
////		    {targets: 4, width: "40%", className: 'text-start text-truncate'},
////		    {targets: 5, width: "10%", className: 'text-start text-truncate'},
////		],
//		columnDefs: [
//            {targets: 0, width: "3%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.index+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 1, width: "3%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.chassistype+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 2, width: "10%", className: 'sorting_asc text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.computer_name+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 3, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.ip_address+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 4, width: "10%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_cpu+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 5, width: "5%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_mb+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 6, width: "3%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_ram+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 7, width: "10%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_disk+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 8, width: "10%", className: 'text-center text-truncate flex-cloumn column_hidden', render: function(data, type, row) {return '<span title="'+row.hw_gpu+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 9, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 10, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 11, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 12, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 13, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
//		    {targets: 14, width: "5%", className: 'text-center text-truncate flex-cloumn align-middle', render: function(data, type, row) {return '<span title="'+row.memo+'" data-toggle="tooltip">'+data+'</span>'}},
//		],
//		language: {
//			"decimal": "",
//			"info": "전체 _TOTAL_건",
//			"infoEmpty": "데이터가 없습니다.",
//			"emptyTable": "데이터가 없습니다.",
//			"thousands": ",",
//			"loadingRecords": "로딩 중입니다.",
//			"processing": "",
//			"zeroRecords": "검색 결과 없음",
//
//			"search": "검색:",
//			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//			"infoPostFix": "",
//            },
//
//});
//
////      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
////      $('.dropdown-menu a').click(function() {
////        var column = $(this).data('column');
////        $('#column-dropdown').text($(this).text());
////        $('#column-dropdown').data('column', column);
////      });
//
//// 검색 버튼 클릭 시 선택한  검색어로 검색 수행
//var searchButton = document.getElementById('asset_search');
//// 검색 버튼이 클릭되면 실행할 함수를 설정합니다.
//searchButton.addEventListener('click', function() {
//    // input 요소의 참조를 가져옵니다.
//    var searchInput = document.getElementById('asset_search_result');
//    // input 요소에서 값을 가져옵니다.
//    var inputValue = searchInput.value;
//    // 값이 있으면 저장하고 콘솔에 출력합니다.
//    if (inputValue) {
//        localStorage.setItem('searchValue', inputValue);
//        console.log("Saved value: " + inputValue);
//    }
//});
//
//$('#search-input-hs').on('keyup', function(event) {
//        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
//            var column = $('#column-dropdown').data('column');
//            var searchValue = $('#search-input-hs').val().trim();
//
//            performSearch(column, searchValue, hs_asset_list_Data);
//        }
//    });
//
//$(document).on('click', '#nexts, #after', function() {
//    var current_page = hs_asset_list_Data.page();
//    var total_pages = hs_asset_list_Data.page.info().pages;
//    if ($(this).attr('id') == 'nexts') {
//            if (current_page + 10 < total_pages) {
//                hs_asset_list_Data.page(current_page + 10).draw('page');
//            } else {
//                hs_asset_list_Data.page(total_pages - 1).draw('page');
//            }
//            } else {
//                hs_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
//            }
//});
//};
//
//      // 드롭다운 메뉴 클릭 시 선택한 컬럼 텍스트 변경
//      $('.dropdown-menu a').click(function() {
//        var column = $(this).data('column');
//        $('#column-dropdown').text($(this).text());
//        $('#column-dropdown').data('column', column);
//      });
//
//      // 검색 버튼 클릭 시 선택한 컬럼과 검색어로 검색 수행
//    $('#search-button-hs').click(function() {
//    var column = $('#column-dropdown').data('column');
//    var searchValue = $('#search-input-hs').val().trim();
//
//    performSearch(column, searchValue, sw_asset_list_Data)
//});
//
//    $('#search-input-hs').on('keyup', function(event) {
//        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
//            var column = $('#column-dropdown').data('column');
//            var searchValue = $('#search-input-hs').val().trim();
//
//            performSearch(column, searchValue, sw_asset_list_Data);
//        }
//    });
//
//	$(document).on('click', '#nexts, #after', function() {
//        var current_page = hs_asset_list_Data.page();
//        var total_pages = hs_asset_list_Data.page.info().pages;
//        if ($(this).attr('id') == 'nexts') {
//                if (current_page + 10 < total_pages) {
//                    hs_asset_list_Data.page(current_page + 10).draw('page');
//                } else {
//                    hs_asset_list_Data.page(total_pages - 1).draw('page');
//                }
//                } else {
//                    hs_asset_list_Data.page(Math.max(current_page - 10, 0)).draw('page');
//                }
//});





$(document).ready(function(){
  $('#asset_search_result').autocomplete({
    source: function(request, response) {
      $.ajax({
        url: 'search_box/',
        method: 'POST',
        data: {
          searchText: request.term
        },
        success: function(data){
          var autocompleteData = data.data.map(function(item) {
            return item.computer_name;
          });

          response(autocompleteData);
        }
      });
    },
    minLength: 2  // 최소 문자 수 설정
  });
});


$('#asset_search').on('click', function(event) {
    // console.log(searchInput)
    var searchInput = document.getElementById('asset_search_result');
    var inputValue = searchInput.value;
    if (inputValue.trim().length < 2) {
      alert("최소 2글자 이상 입력하세요.");
    } else {
      searchPer(inputValue);
    }
});


$('#asset_search_result').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var searchInput = document.getElementById('asset_search_result');
            var inputValue = searchInput.value;
            if (inputValue.trim().length < 2) {
        alert("최소 2글자 이상 입력하세요.");
      } else {
        searchPer(inputValue);
      }
    }
    });


function searchPer(inputValue){
    $.ajax({
        type: "POST",
        url: "search/",
        data: {
            searchText: inputValue
        },
        success: function(res) {
            if (res.data[0] !== undefined){
                var data = res.data[0]; // 첫 번째 객체 선택

                var valueMap = {
                    '사용자': data.computer_name,
                    '메모': data.memo,
                    'IP 주소': data.ip_address,
                    'Mac 주소': data.mac_address,
                    'OS 종류': data.os_simple,
                    'OS 버전': data.os_version,
                    'Office 365 버전': data.essential5,
                    '메모리 사용량': data.mem_use,
                    '디스크 사용량': data.disk_use,
                    '최초 네트워크 접속일': data.first_network,
                    '내 컴퓨터 정보' :data.hw_cpu
                };

            // 각 <td> 요소에 값 설정
            var ipAddressElement = document.getElementById("asset_ip_address");
            if (ipAddressElement) {
              ipAddressElement.textContent = valueMap['IP 주소'];
            }
            var computerNameElement = document.getElementById("asset_computer_name");
            if (computerNameElement) {
              computerNameElement.textContent = data.computer_name;
            }

            var memoElement = document.getElementById("asset_memo");
            if (memoElement) {
              memoElement.value = data.memo || "";
            }

            var ipAddressElement = document.getElementById("asset_ip_address");
            if (ipAddressElement) {
              ipAddressElement.textContent = data.ip_address;
            }
            var macAddressElement = document.getElementById("asset_mac_address");
            if (macAddressElement) {
             macAddressElement.textContent = data.mac_address;
            }

            var osTypeElement = document.getElementById("asset_os_simple");
            if (osTypeElement) {
             osTypeElement.textContent = data.os_simple;
            }

            var osVersionElement = document.getElementById("asset_os_version");
            if (osVersionElement) {
             osVersionElement.textContent = data.os_version;
            }

            var office365VersionElement= document.getElementById("asset_office_version");
            if (office365VersionElement) {
             office365VersionElement.textContent= data.essential5 || "";
            }

            var memoryUsageElement=document.getElementById('asset_mem_use');
            if(memoryUsageElement){
            memoryUsageElement.textContent=valueMap['메모리 사용량']||"";
            }

            var diskUsageElement=document.getElementById('asset_disk_use');
            if(diskUsageElement){
            diskUsageElement.textContent=valueMap['디스크 사용량']||"";
            }

            var firstNetworkAccessDateElement=document.getElementById('asset_first_network');
            if(firstNetworkAccessDateElement){
            firstNetworkAccessDateElement.textContent=data.first_network||"";
            }


            var myComputerInfoElemnt=document.getElementById('asset_hw_cpu');
            if(myComputerInfoElemnt){
             myComputerInfoElemnt.innerText="CPU: "+data.hw_cpu + " \n RAM : "+data.hw_ram+ " \n 메인보드 : "+data.hw_mb+ " \n 디스크 : "+data.hw_disk+ " \n 그래픽카드 : "+data.hw_gpu;
           }
        } else {
                return
            }

        }
    });
}

// search.addEventListener('input', function() {
//     var inputValue = search.value;
//
//     $.ajax({
//         type: "POST",
//         url: "search/",
//         data: {
//             searchText: inputValue
//         },
//         success: function(res) {
//             $('#autocompleteList').empty();
//             var data = res.data[0]; // 첫 번째 객체 선택
//             console.log(data);
//             //console.log(data.disk_use);
//             res.data.forEach(function(data){
//                 $('#autocompleteList').append('<option value="' + data.computer.computer_name + '">');
//             });
            //
        //
        //     var valueMap = {
        //         '사용자': data.computer.computer_name,
        //         '메모': data.computer.memo,
        //         'IP 주소': data.computer.ip_address,
        //         'Mac 주소': data.computer.mac_address,
        //         'OS 종류': data.computer.os_simple,
        //         'OS 버전': data.computer.os_version,
        //         'Office 365 버전': data.essential2,
        //         '메모리 사용량': data.mem_use,
        //         '디스크 사용량': data.disk_use,
        //         '최초 네트워크 접속일': data.first_network,
        //         '내 컴퓨터 정보' :data.hw_cpu
        //     };
        //
        //
        //     // 각 <td> 요소에 값 설정
        //     var ipAddressElement = document.getElementById("asset_ip_address");
        //     if (ipAddressElement) {
        //       ipAddressElement.textContent = valueMap['IP 주소'];
        //     }
        //     var computerNameElement = document.getElementById("asset_computer_name");
        //     if (computerNameElement) {
        //       computerNameElement.textContent = data.computer.computer_name;
        //     }
        //
        //     var memoElement = document.getElementById("asset_memo");
        //     if (memoElement) {
        //       memoElement.textContent = data.computer.memo || "";
        //     }
        //
        //     var ipAddressElement = document.getElementById("asset_ip_address");
        //     if (ipAddressElement) {
        //       ipAddressElement.textContent = data.computer.ip_address;
        //     }
        //     var macAddressElement = document.getElementById("asset_mac_address");
        //     if (macAddressElement) {
        //      macAddressElement.textContent = data.computer.mac_address;
        //     }
        //
        //     var osTypeElement = document.getElementById("asset_os_simple");
        //     if (osTypeElement) {
        //      osTypeElement.textContent = data.computer.os_simple;
        //     }
        //
        //     var osVersionElement = document.getElementById("asset_os_version");
        //     if (osVersionElement) {
        //      osVersionElement.textContent = data.computer.os_version;
        //     }
        //
        //     var office365VersionElement= document.getElementById("asset_office_version");
        //     if (office365VersionElement) {
        //      office365VersionElement.textContent= data.essential2 || "";
        //     }
        //
        //     var memoryUsageElement=document.getElementById('asset_mem_use');
        //     if(memoryUsageElement){
        //     memoryUsageElement.textContent=valueMap['메모리 사용량']||"";
        //     }
        //
        //     var diskUsageElement=document.getElementById('asset_disk_use');
        //     if(diskUsageElement){
        //     diskUsageElement.textContent=valueMap['디스크 사용량']||"";
        //     }
        //
        //     var firstNetworkAccessDateElement=document.getElementById('asset_first_network');
        //     if(firstNetworkAccessDateElement){
        //     firstNetworkAccessDateElement.textContent=data.first_network||"";
        //     }
        //
        //
        //     var myComputerInfoElemnt=document.getElementById('asset_hw_cpu');
        //     if(myComputerInfoElemnt){
        //      myComputerInfoElemnt.innerText="CPU: "+data.computer.hw_cpu + " \n RAM : "+data.computer.hw_ram+ " \n 메인보드 : "+data.computer.hw_mb+ " \n 디스크 : "+data.computer.hw_disk+ " \n 그래픽카드 : "+data.computer.hw_vga;
        //    }

    //     }
    // });
    // $.ajax({
    //     url:
    // })
// });



$(document).ready(function () {
    user_list_popup();
    //asset_list();
    $('#memo_save').click(function() {
    var memoValue = $('#asset_memo').val();
    var computernameValue = $('#asset_computer_name').text();
    var macaddressValue = $('#asset_mac_address').text();

    // Function to escape HTML entities in the memoValue
    function escapeHtml(unsafe) {
        return $('<div/>').text(unsafe).html();
    }

    memoValue = escapeHtml(memoValue);

    if (computernameValue === '-'){
              alert('Computer Name을 선택해 주세요.');
              return
          }
    $.ajax({
      url: 'save_memo/',  // 저장할 URL 주소로 변경해야 합니다.
      method: 'POST',
      data: { memo: memoValue,
                computername: computernameValue,
                macaddress: macaddressValue
                            },
      success: function(response) {
          // console.log(computernameValue)
          //console.log(response)

        alert('저장 완료')
        console.log('메모가 성공적으로 저장되었습니다.');
        // 원하는 작업 수행
      },
      error: function(xhr, status, error) {
        console.error('메모 저장 중 오류가 발생했습니다:', error);
        // 에러 처리 로직 추가
      }
    });
  });
});