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
        onGenerate:function(current_time, $input) {
            var currentDate = new Date();
            // 현재 날짜와 선택된 날짜를 비교
            var isSameDay = current_time.getDate() === currentDate.getDate() && current_time.getMonth() === currentDate.getMonth() && current_time.getFullYear() === currentDate.getFullYear();

            // 현재 시간보다 뒤의 시간들을 숨기기 (현재 날짜일 경우에만)
            $(".xdsoft_time_variant .xdsoft_time").each(function () {
                var hour = $(this).data('hour');
                if (isSameDay && hour > currentDate.getHours()) {
                    $(this).css('pointer-events', 'none');
                    $(this).css('color', '#c1c1c1');
                } else {
                    $(this).show();
                }
            });
        },
        onChangeDateTime:function(dp,$input){
            if (!dp){
                return
            }
            var selectedTime = dp.getTime();
            var currentTime = new Date();

            if (selectedTime > currentTime.getTime()) {
                // 선택된 시간이 현재 시간보다 뒤인 경우, 다시 이전의 시간으로 설정
                var futureTime = new Date();

                $input.val('');
            } else {
            date1 = $input.val();
                }
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
        onGenerate:function(current_time, $input) {
            var currentDate = new Date();
            // 현재 날짜와 선택된 날짜를 비교
            var isSameDay = current_time.getDate() === currentDate.getDate() && current_time.getMonth() === currentDate.getMonth() && current_time.getFullYear() === currentDate.getFullYear();

            // 현재 시간보다 뒤의 시간들을 숨기기 (현재 날짜일 경우에만)
            $(".xdsoft_time_variant .xdsoft_time").each(function () {
                var hour = $(this).data('hour');
                if (isSameDay && hour > currentDate.getHours()) {
                    $(this).css('pointer-events', 'none');
                    $(this).css('color', '#c1c1c1');
                } else {
                    $(this).show();
                }
            });
        },
        onChangeDateTime:function(dp,$input){
            if (!dp){
                return
            }
            var selectedTime = dp.getTime();
            var currentTime = new Date();

            if (selectedTime > currentTime.getTime()) {
                // 선택된 시간이 현재 시간보다 뒤인 경우, 다시 이전의 시간으로 설정
                var futureTime = new Date();

                $input.val('');
            } else {
                date2 = $input.val();
                }
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
        // alert('검색어를 입력해주세요');
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
            // alert('검색어를 입력해주세요');
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
            if (res === 'None') {
                alert('선택하신 시간대에 데이터가 없습니다.\n' +
                    '다른 시간대를 선택해주세요.')
            } else if ( res === 'null'){
                alert('검색어를 입력해주세요.')
            }
            if (res.data1 !== undefined){
                var data1 = res.data1[0]; // 첫 번째 객체 선택
                var data2 = res.data2[0]; // 첫 번째 객체 선택
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
                var computerNameElement = document.getElementById("search_his");

                    computerNameElement.value = data1.computer_name;

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
                var myComputerInfoCpu1=document.getElementById('cpu1');
                var myComputerInfoRam1=document.getElementById('ram1');
                var myComputerInfoDisk1=document.getElementById('disk1');
                var myComputerInfoGpu1=document.getElementById('gpu1');
                var myComputerInfoMainboard1=document.getElementById('mainboard1');
                 var myComputerInfoCpu2=document.getElementById('cpu2');
                var myComputerInfoRam2=document.getElementById('ram2');
                var myComputerInfoDisk2=document.getElementById('disk2');
                var myComputerInfoGpu2=document.getElementById('gpu2');
                var myComputerInfoMainboard2=document.getElementById('mainboard2');
                if(myComputerInfoElemnt && myComputerInfoElemnt2){
                    myComputerInfoCpu2.style.color = '';
                    myComputerInfoRam2.style.color = '';
                    myComputerInfoMainboard2.style.color = '';
                    myComputerInfoGpu2.style.color = '';
                    myComputerInfoDisk2.style.color = '';
                    myComputerInfoCpu1.innerText = "CPU: "+data1.hw_cpu
                    myComputerInfoRam1.innerText = "RAM : "+data1.hw_ram
                    myComputerInfoMainboard1.innerText = "메인보드 : "+data1.hw_mb
                    myComputerInfoGpu1.innerText = "그래픽카드 : "+data1.hw_gpu
                    myComputerInfoDisk1.innerText = "디스크 : "+data1.hw_disk
                    myComputerInfoCpu2.innerText = "CPU: "+data2.hw_cpu
                    myComputerInfoRam2.innerText = "RAM : "+data2.hw_ram
                    myComputerInfoMainboard2.innerText = "메인보드 : "+data2.hw_mb
                    myComputerInfoGpu2.innerText = "그래픽카드 : "+data2.hw_gpu
                    myComputerInfoDisk2.innerText = "디스크 : "+data2.hw_disk
                    // myComputerInfoElemnt.innerText="CPU: "+data1.hw_cpu + " \n RAM : "+data1.hw_ram+ " \n 메인보드 : "+data1.hw_mb+ " \n 디스크 : "+data1.hw_disk+ " \n 그래픽카드 : "+data1.hw_gpu;
                    // myComputerInfoElemnt2.innerText="CPU: "+data2.hw_cpu + " \n RAM : "+data2.hw_ram+ " \n 메인보드 : "+data2.hw_mb+ " \n 디스크 : "+data2.hw_disk+ " \n 그래픽카드 : "+data2.hw_gpu;
                    highlightDifferentValue(myComputerInfoCpu1, myComputerInfoCpu2);
                    highlightDifferentValue(myComputerInfoRam1, myComputerInfoRam2);
                    highlightDifferentValue(myComputerInfoDisk1, myComputerInfoDisk2);
                    highlightDifferentValue(myComputerInfoGpu1, myComputerInfoGpu2);
                    highlightDifferentValue(myComputerInfoMainboard1, myComputerInfoMainboard2);
                }
            } else {
                return
            }

        }
    });
}

function highlightDifferentValue(element1, element2) {
    var value1 = element1.innerText;
    var value2 = element2.innerText;

    // 값이 다를 경우에만 색을 변경
    if (value1 !== value2) {
        element2.style.color = 'red';
    }
}


    user_list_popup();
    //asset_list();
});
