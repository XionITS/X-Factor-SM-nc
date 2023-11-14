///*
//Template Name: HUD - Responsive Bootstrap 5 Admin Template
//Version: 1.8.0
//Author: Sean Ngu
//
//*/

var search = document.getElementById('asset_search_result');
var date1 = ''
var date2 = ''
$(document).ready(function(){
    var currentDateTime = new Date();
    currentDateTime.setMinutes(0);
    currentDateTime.setSeconds(0);
    $("#aa").click(function(){
        $("#datepicker1").focus(); // input에 포커스를 줍니다. 이로써 데이터피커가 표시될 수 있습니다.
    });
    $("#datepicker1").datetimepicker({
        format: 'Y-m-d H시',
        formatTime: 'H시',
        minDate: '2023/10/18',
        maxDate: currentDateTime,
        roundTime:'floor',
        onChangeDateTime:function(dp,$input){
            date1 = $input.val();
        }
    });

    $("#bb").click(function(){
        $("#datepicker2").focus(); // input에 포커스를 줍니다. 이로써 데이터피커가 표시될 수 있습니다.
    });
    $("#datepicker2").datetimepicker({
        format: 'Y-m-d H시',
        formatTime: 'H시',
        minDate: '2023/10/18',
        maxDate: currentDateTime,
        roundTime:'floor',
        onChangeDateTime:function(dp,$input){
            date2 = $input.val();
        }
    });

  $('#search_his').autocomplete({
    source: function(request, response) {
      $.ajax({
        url: 'search_box_h/',
        method: 'POST',
        data: {
          searchText: request.term
        },
        success: function(data){
          // 데이터 변환 후 반환
          var autocompleteData = data.data.map(function(item) {
            return item.computer_name;
          });
          response(autocompleteData);
        }
      });
    },
    minLength: 2  // 최소 문자 수 설정
  });


$('#search_his_btn').on('click', function(event) {
    var searchInput = document.getElementById('search_his');
    var inputValue = searchInput.value;
    if (!date1 || !date2) {
        alert('날짜를 선택해주세요')
        return;
    }
    else if (!inputValue) {
        alert('검색어를 입력해주세요');
    }
    searchPer_h(inputValue, date1, date2)
    $('#search_his').val('')
});

$('#search_his').on('keyup', function(event) {
    if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
        var searchInput = document.getElementById('search_his');
        var inputValue = searchInput.value;
        if (!date1 || !date2) {
            alert('날짜를 선택해주세요')
            return;
        }
        else if (!inputValue) {
            alert('검색어를 입력해주세요');
        }
        searchPer_h(inputValue, date1, date2)
        $('#search_his').val('')
    }
});


function searchPer_h(inputValue, date1, date2){
    $.ajax({
        type: "POST",
        url: "search_h/",
        data: {
            searchText: inputValue,
            date1: date1,
            date2: date2
        },
        success: function(res) {
            // if (res === 'None') {
            //     alert('computer name을 입력하여 선택해 주세요')
            // }
            if (res.data1 !== undefined){
                var data1 = res.data1; // 첫 번째 객체 선택
                var data2 = res.data2; // 첫 번째 객체 선택
                var ipAddressElement = document.getElementById("asset_ip_address");
                var ipAddressElement2 = document.getElementById("asset_ip_address2");
                if (ipAddressElement && ipAddressElement2) {
                    ipAddressElement2.style.color = '';
                    ipAddressElement.textContent = data1.ip_address;
                    ipAddressElement2.textContent = data2.ip_address;
                    if (ipAddressElement.textContent !== ipAddressElement2.textContent) {
                        ipAddressElement2.style.color = 'red';
                    }
                }
                // var computerNameElement = document.getElementById("asset_computer_name");
                // var computerNameElement2 = document.getElementById("asset_computer_name2");
                // if (computerNameElement && computerNameElement2) {
                //     computerNameElement2.style.color = '';
                //     computerNameElement.textContent = data1.computer_name;
                //     computerNameElement2.textContent = data2.computer_name;
                //     if (computerNameElement.textContent !== computerNameElement2.textContent) {
                //             computerNameElement2.style.color = 'red';
                //     }
                // }
                var userElement = document.getElementById("asset_user");
                var userElement2 = document.getElementById("asset_user2");
                if (userElement && userElement2) {
                    userElement2.style.color = '';
                    userElement.textContent = data1.ncdb_data.userName;
                    userElement2.textContent = data2.ncdb_data.userName;
                    if (userElement.textContent !== userElement2.textContent) {
                            userElement2.style.color = 'red';
                    }
                }
                var macAddressElement = document.getElementById("asset_mac_address");
                var macAddressElement2 = document.getElementById("asset_mac_address2");
                if (macAddressElement && macAddressElement2) {
                    macAddressElement2.style.color = '';
                    macAddressElement.textContent = data1.mac_address;
                    macAddressElement2.textContent = data2.mac_address;
                    if (macAddressElement.textContent !== macAddressElement2.textContent) {
                            macAddressElement2.style.color = 'red';
                    }
                }

                var osTypeElement = document.getElementById("asset_os_simple");
                var osTypeElement2 = document.getElementById("asset_os_simple2");
                if (osTypeElement && osTypeElement) {
                    osTypeElement2.style.color = '';
                    osTypeElement.textContent = data1.os_simple;
                    osTypeElement2.textContent = data2.os_simple;
                    if (osTypeElement.textContent !== osTypeElement2.textContent) {
                            osTypeElement2.style.color = 'red';
                    }
                }

                var osVersionElement = document.getElementById("asset_os_version");
                var osVersionElement2 = document.getElementById("asset_os_version2");
                if (osVersionElement && osVersionElement2) {
                    osVersionElement2.style.color = '';
                    osVersionElement.textContent = data1.os_version;
                    osVersionElement2.textContent = data2.os_version;
                    if (osVersionElement.textContent !== osVersionElement2.textContent) {
                            osVersionElement2.style.color = 'red';
                    }
                }

                var office365VersionElement= document.getElementById("asset_office_version");
                var office365VersionElement2= document.getElementById("asset_office_version2");
                if (office365VersionElement && office365VersionElement2) {
                    office365VersionElement2.style.color = '';
                    office365VersionElement.textContent= data1.essential5 || "";
                    office365VersionElement2.textContent= data2.essential5 || "";
                    if (office365VersionElement.textContent !== office365VersionElement2.textContent) {
                            office365VersionElement2.style.color = 'red';
                    }
                }

                var memoryUsageElement=document.getElementById('asset_mem_use');
                var memoryUsageElement2=document.getElementById('asset_mem_use2');
                if(memoryUsageElement && memoryUsageElement2){
                    memoryUsageElement2.style.color = '';
                memoryUsageElement.textContent=data1.mem_use ||"";
                memoryUsageElement2.textContent=data2.mem_use ||"";
                    if (memoryUsageElement.textContent !== memoryUsageElement2.textContent) {
                            memoryUsageElement2.style.color = 'red';
                    }
                }

                var diskUsageElement=document.getElementById('asset_disk_use');
                var diskUsageElement2=document.getElementById('asset_disk_use2');
                if(diskUsageElement && diskUsageElement2){
                    diskUsageElement2.style.color = '';
                diskUsageElement.textContent=data1.disk_use ||"";
                diskUsageElement2.textContent=data2.disk_use ||"";
                    if (diskUsageElement.textContent !== diskUsageElement2.textContent) {
                            diskUsageElement2.style.color = 'red';
                    }
                }

                var firstNetworkAccessDateElement=document.getElementById('asset_first_network');
                var firstNetworkAccessDateElement2=document.getElementById('asset_first_network2');
                if(firstNetworkAccessDateElement && firstNetworkAccessDateElement2){
                    firstNetworkAccessDateElement2.style.color = '';
                    firstNetworkAccessDateElement.textContent=data1.first_network||"";
                    firstNetworkAccessDateElement2.textContent=data2.first_network||"";
                    if (firstNetworkAccessDateElement.textContent !== firstNetworkAccessDateElement2.textContent) {
                        firstNetworkAccessDateElement2.style.color = 'red';
                    }
                }


                var myComputerInfoElemnt=document.getElementById('asset_hw_cpu');
                var myComputerInfoElemnt2=document.getElementById('asset_hw_cpu2');
                if(myComputerInfoElemnt && myComputerInfoElemnt2){
                    myComputerInfoElemnt.innerText="CPU: "+data1.hw_cpu + " \n RAM : "+data1.hw_ram+ " \n 메인보드 : "+data1.hw_mb+ " \n 디스크 : "+data1.hw_disk+ " \n 그래픽카드 : "+data1.hw_gpu;
                    myComputerInfoElemnt2.innerText="CPU: "+data2.hw_cpu + " \n RAM : "+data2.hw_ram+ " \n 메인보드 : "+data2.hw_mb+ " \n 디스크 : "+data2.hw_disk+ " \n 그래픽카드 : "+data2.hw_gpu;
                }
            } else {
                return
            }

        }
    });
}



    user_list_popup();
    //asset_list();
});