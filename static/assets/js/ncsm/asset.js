
// $(document).ready(function(){
//   $('#asset_search_result').autocomplete({
//     source: function(request, response) {
//       $.ajax({
//         url: 'search_box/',
//         method: 'POST',
//         data: {
//           searchText: request.term
//         },
//         success: function(data){
//           var autocompleteData = data.data.map(function(item) {
//             return item.computer_name;
//           });
//
//           response(autocompleteData);
//         }
//       });
//     },
//     minLength: function (term, input) {
//       // 입력된 문자열이 한글인 경우 2글자, 영어인 경우 3글자로 제한
//       return (/[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(input) ? 2 : 3);
//     }
//   });
// });
var result = ''
$(document).ready(function () {
    $('#asset_search_result').autocomplete({
        source: function (request, response) {
            // 사용자가 입력한 문자열의 길이를 체크
            var minLength = /[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(request.term) ? 2 : 3;

            // 최소 길이를 만족하는 경우에만 Ajax 요청 보내기
            if (request.term.length >= minLength) {
            // if (request.term.length >= 2) {
                $.ajax({
                    url: 'search_box/',
                    method: 'POST',
                    data: {
                        searchText: request.term,
                        type: 'asset'
                    },
                    success: function (data) {
                        var autocompleteData = data.data.map(function (item) {
                            return item.computer_name;
                        });

                        response(autocompleteData);
                    }
                });
            }
        },
        minLength: 2  // Autocomplete 내에서의 최소 길이 설정
    });

    $('#asset_user').autocomplete({
        source: function (request, response) {
            // 사용자가 입력한 문자열의 길이를 체크
            var minLength = /[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(request.term) ? 2 : 3;

            // 최소 길이를 만족하는 경우에만 Ajax 요청 보내기
            if (request.term.length >= minLength) {
            // if (request.term.length >= 2) {
                $.ajax({
                    url: 'search_box/',
                    method: 'POST',
                    data: {
                        searchText: request.term,
                        type: 'user'
                    },
                    success: function (data) {
                        var autocompleteData = data.data.map(function (item) {
                            return {
                            label: item.logged_name_id__userName + ' (' + item.computer_name + ')', /// Autocomplete에서 보여질 값,
                            value: item.logged_name_id__userName + ' (' + item.computer_name + ')',
                            computer_name: item.computer_name
                            };
                        });
                         // Autocomplete 초기화
                        $('#asset_user').autocomplete({
                            source: autocompleteData,
                            select: function (event, ui) {
                                // 선택된 항목의 label 및 value 값 가져오기
                                var selectedLabel = ui.item.label;
                                var selectedValue = ui.item.computer_name;
                                result = selectedValue
                                // 선택된 값 콘솔에 출력
                                // 여기에 선택된 값에 대한 추가적인 로직을 구현할 수 있습니다.
                            }
                        });
                        response(autocompleteData);
                    }
                });
            }
        },
        minLength: 2  // Autocomplete 내에서의 최소 길이 설정
    });
});


$('#asset_search').on('click', function(event) {
    // console.log(searchInput)
    var searchInput = document.getElementById('asset_search_result');
    var inputValue = searchInput.value;
    if (inputValue.trim().length < 2 ) {
        alert("최소 2글자 입력해주세요.");
    } else {
      searchPer(inputValue, 'asset');
    }
});


$('#asset_search_result').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var searchInput = document.getElementById('asset_search_result');
            var inputValue = searchInput.value;
            if (inputValue.trim().length < 2) {
        alert("최소 2글자 입력해주세요.");
      } else {
        searchPer(inputValue, 'asset');
      }
    }
});


$('#user_search').on('click', function(event) {
    // console.log(searchInput)
    var searchInput = document.getElementById('asset_user');
    var inputValue = searchInput.value;
    if (inputValue.trim().length < 2 ) {
        alert("최소 2글자 입력해주세요.");
    } else {
      searchPer(result, 'user');
    }
});


$('#asset_user').on('keyup', function(event) {
        if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
            var searchInput = document.getElementById('asset_user');
            var inputValue = searchInput.value;
            if (inputValue.trim().length < 2) {
        alert("최소 2글자 입력해주세요.");
      } else {
        searchPer(result, 'user');
      }
    }
});


function searchPer(inputValue, type){
    $.ajax({
        type: "POST",
        url: "search/",
        data: {
            searchText: inputValue,
            type: type
        },
        success: function(res) {
            if (res === 'error') {
                alert('유효하지 않은 값입니다.')
                return
            }
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
            var statusElement = document.getElementById("asset_status");
            if (statusElement) {
              statusElement.textContent = data.cache_date;
              statusElement.style.color = data.cache_date === "Online" ? "lime" : "red";
            }
            var computerNameElement = document.getElementById("asset_search_result");
            if (computerNameElement) {
              computerNameElement.value = data.computer_name;
            }
            var userElement = document.getElementById("asset_user");
            if (userElement) {
              userElement.value = data.ncdb_data.userName;
            }

            var memoElement = document.getElementById("asset_memo");
            if (memoElement) {
              memoElement.value = data.memo || "";
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
                // 데이터가 없을 때
                // return
                alert("유효하지 않은 값입니다.");
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
    var computernameValue = $('#asset_search_result').val();
    var usernameValue = $('#asset_user').val();
    var macaddressValue = $('#asset_mac_address').text();

    // Function to escape HTML entities in the memoValue
    function escapeHtml(unsafe) {
        return $('<div/>').text(unsafe).html();
    }

    memoValue = escapeHtml(memoValue);

    if (computernameValue === '' || usernameValue === ''){
              alert('컴퓨터 이름이나 사용자를 선택해 주세요.');
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
        if (response.error) {
            alert(response.error)
        } else {
            alert('저장 완료')
        }
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
