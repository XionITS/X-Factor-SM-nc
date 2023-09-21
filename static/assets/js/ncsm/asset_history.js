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

    $("#aa").click(function(){
        $("#datepicker1").focus(); // input에 포커스를 줍니다. 이로써 데이터피커가 표시될 수 있습니다.
    });
    $("#datepicker1").datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
    }).on('changeDate', function(e) {
        date1 = e.format()
    });

    $("#bb").click(function(){
        $("#datepicker2").focus(); // input에 포커스를 줍니다. 이로써 데이터피커가 표시될 수 있습니다.
    });
    $("#datepicker2").datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
    }).on('changeDate', function(e) {
        date2 = e.format()
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
});



$('#search_his_btn').on('click', function(event) {
    var searchInput = document.getElementById('search_his');
    var inputValue = searchInput.value;
    searchPer_h(inputValue, date1, date2)
});

$('#search_his').on('keyup', function(event) {
    if (event.keyCode === 13) { // 엔터 키의 키 코드는 13
        var searchInput = document.getElementById('search_his');
        var inputValue = searchInput.value;
        searchPer_h(inputValue, date1, date2)
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
            if (res.data1[0] !== undefined){
                var data1 = res.data1[0]; // 첫 번째 객체 선택
                var data2 = res.data2[0]; // 첫 번째 객체 선택

                // var valueMap = {
                //     '사용자': data1.computer.computer_name,
                //     '메모': data1.computer.memo,
                //     'IP 주소': data1.computer.ip_address,
                //     'Mac 주소': data1.computer.mac_address,
                //     'OS 종류': data1.computer.os_simple,
                //     'OS 버전': data1.computer.os_version,
                //     'Office 365 버전': data1.essential5,
                //     '메모리 사용량': data1.mem_use,
                //     '디스크 사용량': data1.disk_use,
                //     '최초 네트워크 접속일': data1.computer.first_network,
                //     '내 컴퓨터 정보' :data1.hw_cpu
                // };

            // 각 <td> 요소에 값 설정
                var ipAddressElement = document.getElementById("asset_ip_address");
                var ipAddressElement2 = document.getElementById("asset_ip_address2");
                if (ipAddressElement && ipAddressElement2) {
                    ipAddressElement.textContent = data1.ip_address;
                    ipAddressElement2.textContent = data2.ip_address;
                    if (ipAddressElement.textContent !== ipAddressElement2.textContent) {
                        ipAddressElement2.style.color = 'red';
                    }
                }
                var computerNameElement = document.getElementById("asset_computer_name");
                var computerNameElement2 = document.getElementById("asset_computer_name2");
                if (computerNameElement && computerNameElement2) {
                    computerNameElement.textContent = data1.computer_name;
                    computerNameElement2.textContent = data2.computer_name;
                    if (computerNameElement.textContent !== computerNameElement2.textContent) {
                            computerNameElement2.style.color = 'red';
                    }
                }

                // var memoElement = document.getElementById("asset_memo");
                // var memoElement2 = document.getElementById("asset_memo2");
                // if (memoElement && memoElement2) {
                //   memoElement.textContent = data1.computer.memo || "";
                //   memoElement2.textContent = data2.computer.memo || "";
                // }

                var macAddressElement = document.getElementById("asset_mac_address");
                var macAddressElement2 = document.getElementById("asset_mac_address2");
                if (macAddressElement && macAddressElement2) {
                    macAddressElement.textContent = data1.mac_address;
                    macAddressElement2.textContent = data2.mac_address;
                    if (macAddressElement.textContent !== macAddressElement2.textContent) {
                            macAddressElement2.style.color = 'red';
                    }
                }

                var osTypeElement = document.getElementById("asset_os_simple");
                var osTypeElement2 = document.getElementById("asset_os_simple2");
                if (osTypeElement && osTypeElement) {
                    osTypeElement.textContent = data1.os_simple;
                    osTypeElement2.textContent = data2.os_simple;
                    if (osTypeElement.textContent !== osTypeElement2.textContent) {
                            osTypeElement2.style.color = 'red';
                    }
                }

                var osVersionElement = document.getElementById("asset_os_version");
                var osVersionElement2 = document.getElementById("asset_os_version2");
                if (osVersionElement && osVersionElement2) {
                    osVersionElement.textContent = data1.os_version;
                    osVersionElement2.textContent = data2.os_version;
                    if (osVersionElement.textContent !== osVersionElement2.textContent) {
                            osVersionElement2.style.color = 'red';
                    }
                }

                var office365VersionElement= document.getElementById("asset_office_version");
                var office365VersionElement2= document.getElementById("asset_office_version2");
                if (office365VersionElement && office365VersionElement2) {
                    office365VersionElement.textContent= data1.essential5 || "";
                    office365VersionElement2.textContent= data2.essential5 || "";
                    if (office365VersionElement.textContent !== office365VersionElement2.textContent) {
                            office365VersionElement2.style.color = 'red';
                    }
                }

                var memoryUsageElement=document.getElementById('asset_mem_use');
                var memoryUsageElement2=document.getElementById('asset_mem_use2');
                if(memoryUsageElement && memoryUsageElement2){
                memoryUsageElement.textContent=data1.mem_use ||"";
                memoryUsageElement2.textContent=data2.mem_use ||"";
                    if (memoryUsageElement.textContent !== memoryUsageElement2.textContent) {
                            memoryUsageElement2.style.color = 'red';
                    }
                }

                var diskUsageElement=document.getElementById('asset_disk_use');
                var diskUsageElement2=document.getElementById('asset_disk_use2');
                if(diskUsageElement && diskUsageElement2){
                diskUsageElement.textContent=data1.disk_use ||"";
                diskUsageElement2.textContent=data2.disk_use ||"";
                    if (diskUsageElement.textContent !== diskUsageElement2.textContent) {
                            diskUsageElement2.style.color = 'red';
                    }
                }

                var firstNetworkAccessDateElement=document.getElementById('asset_first_network');
                var firstNetworkAccessDateElement2=document.getElementById('asset_first_network2');
                if(firstNetworkAccessDateElement && firstNetworkAccessDateElement2){
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
});