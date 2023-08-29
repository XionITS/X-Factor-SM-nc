
// ----------------------------------------- deploy popup start -----------------------------------------
$(document).on("click","#createdeploy", function (e) {
    var computerGroupSelect = $('#computerGroupData');
    var selectedGroup = ''
    var selectedPackage = ''
    $.ajax({
        url: '../group/list/',
        method: 'POST',
        success: function (res) {
                var data = res.item;
                $.each(data, function(index, group) {
                    computerGroupSelect.append($('<option>', {
                        text: group.Name
                    }));
                });
        }
    });

    $.ajax({
        url: '../package/list/',
        method: 'POST',
        success: function (res) {
                var packageSelect = $('#packageData');
                var data = res.item;
                $.each(data, function(index, package) {
                    packageSelect.append($('<option>', {
                        text: package.Name
                    }));
                });

        }
    });
    console.log(packageData)
    // 셀렉트 박스 값이 변경되었을 때 이벤트 리스너 추가
    $('#computerGroupData').on('change', function() {
        selectedGroup = $(this).val();
        $.ajax({

        })
        console.log('Selected Group ID:', selectedGroup);
    });

    $('#packageData').on('change', function() {
        selectedPackage = $(this).val();
        console.log('Selected Package ID:', selectedPackage);
    });

    $("#deployModal").modal("show");

    $(document).on("click","#deployCreate", function(event) {
        $.ajax({
            url: '../deploy_action/',
            method: 'POST',
            data: {
                selectedGroup: selectedGroup,
                selectedPackage: selectedPackage
            },
            success: function(res) {
                console.log(res)
            }
        });
        let computerIds = []
        let computerNames = []
        const computerElements = $('#deployModal .form-check').find('.form-check-input');
    });
});


// ----------------------------------------- deploy popup end -----------------------------------------

//
// //deploy 페이지
// var deploy_package = function () {
//     var packSelectBox = document.querySelector('.content_selec');
//     var dashboardpopupTable = $('#packageDataTable').DataTable({
//         dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>t",
//         lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
//         responsive: true,
//         searching: true,
//         ordering: false,
//         serverSide: true,
//         displayLength: false,
//         paging: false,
//         destroy: true,
//         order: [
//             [ 2, "desc"],
//             [ 0, "asc"]
//         ],
//         ajax: {
//             url: 'list/',
//             type: "POST",
//             data: function (data) {
//                     // 선택한 옵션의 값을 가져옵니다.
//                     var id = packSelectBox.value;
//                     // 가져온 값을 콘솔에 출력하거나 다른 작업을 수행합니다.
//                     return {'id': id,
//                             'search': data.search.value}
//             },
//             dataSrc: function (res) {
//                 var data = res.item;
//                 return data;
//             }
//         },
//         columns: [
//             {data: 'Name', width: "15%"},
//             {data: 'Content_set', width: "10%"},
//             {data: 'Command', width: "35%"},
//         ],
//         columnDefs: [
//             {targets: 0, className: 'text-center', render: function (data, type, row) {
//                     return '<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 200px;" title="' + row.Name + '" data-toggle="tooltip">' + data + '</span>'
//                 }},
//             {targets: 1, className: 'text-center', render: function (data, type, row) {
//                     return '<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 100px;" title="' + row.Content_set + '" data-toggle="tooltip">' + data + '</span>'
//                 }},
//             {targets: 2, className: 'text-center', render: function (data, type, row) {
//                     return '<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 300px;" title="' + row.Command + '" data-toggle="tooltip">' + data + '</span>'
//                 }}
//         ],
//         language: {
//             "decimal": "",
//             "info": "전체 _TOTAL_건",
//             "infoEmpty": "데이터가 없습니다.",
//             "emptyTable": "데이터가 없습니다.",
//             "thousands": ",",
//             "lengthMenu": "페이지당 _MENU_ 개씩 보기",
//             "loadingRecords": "로딩 중입니다.",
//             "processing": "",
//             "zeroRecords": "검색 결과 없음",
//             "paginate": {
//                 "first": "처음",
//                 "last": "끝",
//                 "next": "다음",
//                 "previous": "이전"
//             },
//             "search": "검색:",
//             "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//             "infoPostFix": "",
//         },
//         pagingType: 'numbers',
//     });
//     packSelectBox.addEventListener('change', function() {
//         // 셀렉트 박스의 값이 변경될 때마다 DataTables 테이블을 다시 그립니다.
//         dashboardpopupTable.ajax.reload();
//     });
// };
//
// var deploy_computerGroup = function () {
//     var groupSelectBox = document.querySelector('.group_selec');
//     var dashboardpopupTable = $('#computerGroupDataTable').DataTable({
//         dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'fB>><'align-items-center d-flex justify-content-between'<'mr-auto col-md-6 mb-md-0 mt-n2'i><'mb-0 col-md-6'p>>t",
//         lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
//         responsive: true,
//         searching: true,
//         ordering: false,
//         serverSide: true,
//         displayLength: false,
//         paging: false,
//         ajax: {
//             url: 'list/',
//             type: "POST",
//             data: function (data) {
//                     // 선택한 옵션의 값을 가져옵니다.
//                     var id = groupSelectBox.value;
//                     // 가져온 값을 콘솔에 출력하거나 다른 작업을 수행합니다.
//                     return {'id': id,
//                             'search': data.search.value}
//             },
//             dataSrc: function (res) {
//                 var data = res.item;
//                 return data;
//             }
//         },
//         columns: [
//             {data: 'Name', width: "15%"},
//             {data: 'Content_set', width: "10%"},
//             {data: 'Expression', width: "35%"},
//         ],
//         columnDefs: [
//             {targets: 0, className: 'text-center', render: function (data, type, row) {
//                     return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 200px;" title="' + row.Name + '" data-toggle="tooltip">' + data + '</div>'
//                 }},
//             // , render: funct'<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.Name + '" data-toggle="tooltip">'+data+'</div>'}
//             {targets: 1, className: 'text-center', render: function (data, type, row) {
//                     return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 100px;" title="' + row.Content_set + '" data-toggle="tooltip">' + data + '</div>'
//                 }},
//             {targets: 2, className: 'text-center', render: function (data, type, row) {
//                     return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 300px;" title="' + row.Expression + '" data-toggle="tooltip">' + data + '</div>'
//                 }}
//         ],
//         language: {
//             "decimal": "",
//             "info": "전체 _TOTAL_건",
//             "infoEmpty": "데이터가 없습니다.",
//             "emptyTable": "데이터가 없습니다.",
//             "thousands": ",",
//             "loadingRecords": "로딩 중입니다.",
//             "processing": "",
//             "zeroRecords": "검색 결과 없음",
//             "paginate": {
//                 "first": "처음",
//                 "last": "끝",
//                 "next": "다음",
//                 "previous": "이전"
//             },
//             "search": "검색:",
//             "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//             "infoPostFix": "",
//         },
//         pagingType: 'numbers',
//
//     });
//     // groupSelectBox.addEventListener('change', function() {
//     //     // 셀렉트 박스의 값이 변경될 때마다 DataTables 테이블을 다시 그립니다.
//     //     dashboardpopupTable.ajax.reload();
//     // });
// };
//
//
// // $(document).ready(function () {
// //
// //     var $clickedRow = ''
// //     var resultP = document.getElementById('outputP');
// //     var resultC = document.getElementById('outputC');
// //     var isRegistryEnabled = true;
// //     var spanElement = document.getElementById('registry');
// //     $("#packageDataTable").on('click', 'tbody tr', function () {
// //         $clickedRow = $(this);
// //         var isClicked = $clickedRow.hasClass('clicked');
// //
// //         // 원래 클릭했던 곳의 색을 없애기 위해 다른 행들의 클래스를 제거합니다.
// //         $('#packageDataTable tbody tr').not($clickedRow).removeClass('clicked').css('background-color', '');
// //
// //         $clickedRow.addClass('clicked');
// //         var tdValue = $clickedRow.find('td:eq(0)').text();
// //         var parentElement = document.getElementById("colval3");
// //         var parentElement1 = document.getElementById("pack");
// //          // 클릭한 행의 상태에 따라 동작을 처리합니다.
// //         spanElement.classList.remove('disabled-span');
// //         if (isClicked) {
// //             var divElement1 = document.getElementById("colVal1");
// //             //버튼 클릭 시 span 태그의 활성화/비활성화 상태 변경
// //             document.getElementById("registry").disabled = false;
// //             divElement1 = document.getElementById("colVal1");
// //             var divElement3 = document.getElementById("colVal3");
// //             divElement1.classList.remove("col-3"); // 기존 클래스 제거
// //             divElement1.classList.add("col-5"); // 새로운 클래스 추가
// //             divElement3.style.display = "none";
// //             divElement1.style.paddingRight = colVal2OriginalPaddingRight;// 새로운 클래스 추가
// //             // colval3 안에 있는 div 태그 모두 삭제
// //             while (parentElement.firstChild) {
// //                 parentElement.removeChild(parentElement.firstChild);
// //             }
// //             // pack 안에 있는 div 태그 모두 삭제
// //             while (parentElement1.firstChild) {
// //                 parentElement1.removeChild(parentElement1.firstChild);
// //             }
// //             // 클릭한 행이 이미 선택된 상태인 경우 선택 해제
// //             $clickedRow.removeClass('clicked');
// //             $clickedRow.css('background-color', '');
// //             resultP.innerHTML = resultP.innerHTML.replace(tdValue + '<br>', '');
// //             // $('tbody tr').removeClass('disabled');
// //             $('#packageDataTable tbody tr').css('pointer-events', 'auto');
// //         } else {
// //             divElement1 = document.getElementById("colVal1");
// //
// //             // colval3 안에 있는 div 태그 모두 삭제
// //             while (parentElement.firstChild) {
// //                 parentElement.removeChild(parentElement.firstChild);
// //             }
// //             // pack 안에 있는 div 태그 모두 삭제
// //             while (parentElement1.firstChild) {
// //                 parentElement1.removeChild(parentElement1.firstChild);
// //             }
// //             document.getElementById("registry").disabled = true;
// //             // 클릭한 행을 선택 상태로 하이라이트하고 다른 행의 클릭을 비활성화
// //             // $('#packageDataTable tbody tr').not($clickedRow).css('pointer-events', 'none');
// //             // $('tbody tr').not($clickedRow).addClass('disabled');
// //             $clickedRow.addClass('clicked');
// //             resultP.innerHTML = tdValue + '<br>';
// //             $clickedRow.css('background-color', 'orange');
// //             var id = tdValue;
// //
// //           // Ajax 요청을 보냅니다.
// //             $.ajax({
// //                 type: 'POST', // HTTP 요청 방식을 선택합니다.
// //                 url: 'packCheck/', // 데이터를 처리할 서버 엔드포인트 URL을 입력합니다.
// //                 data: { 'id': id }, // 서버로 보낼 데이터를 설정합니다.
// //                 success: function(response) {
// //                   // 성공적인 응답을 받았을 때 수행할 동작을 정의합니다.
// //                     console.log('성공:', response);
// //                     if (typeof response.a === 'number' && response.a > 0) {
// //                         param(response.a)
// //                         //버튼 클릭 시 span 태그의 활성화/비활성화 상태 변경
// //                         if (divElement1.classList.contains('col-3')) {
// //                             spanElement.classList.add('disabled-span');
// //                         }
// //                     } else {
// //                         if (divElement1.classList.contains('col-5')) {
// //                             spanElement.classList.remove('disabled-span');
// //                         }
// //                         // colval3 안에 있는 div 태그 모두 삭제
// //                         while (parentElement.firstChild) {
// //                             parentElement.removeChild(parentElement.firstChild);
// //                         }
// //                         // pack 안에 있는 div 태그 모두 삭제
// //                         while (parentElement1.firstChild) {
// //                             parentElement1.removeChild(parentElement1.firstChild);
// //                         }
// //                         divElement1 = document.getElementById("colVal1");
// //                         divElement3 = document.getElementById("colVal3");
// //                         divElement1.classList.remove("col-3"); // 기존 클래스 제거
// //                         divElement1.classList.add("col-5"); // 새로운 클래스 추가
// //                         divElement3.style.display = "none";
// //                         divElement1.style.paddingRight = colVal2OriginalPaddingRight;// 새로운 클래스 추가
// //                         return
// //                     }
// //                 },
// //                 error: function(xhr, status, error) {
// //                   // 오류가 발생했을 때 수행할 동작을 정의합니다.
// //                     console.error('오류:', status, error);
// //                 }
// //             });
// //         }
// //     });
// //
// //     function param(count){
// //         var divElement1 = document.getElementById("colVal1");
// //         var divElement3 = document.getElementById("colVal3");
// //         divElement1.classList.remove("col-5"); // 기존 클래스 제거
// //         divElement1.classList.add("col-3"); // 새로운 클래스 추가
// //         divElement3.style.display = "none";
// //         divElement1.style.paddingRight = "0";// 새로운 클래스 추가
// //         divElement3.removeAttribute("style");
// //         var parentElement = document.getElementById("colval3"); // input 박스를 추가할 부모 요소를 가져옴
// //         var parentElement1 = document.getElementById("pack"); // input 박스를 추가할 부모 요소를 가져옴
// //         for (var i = 1; i <= count; i++) {
// //             // div 태그 생성
// //             var divElement = document.createElement("div");
// //             divElement.textContent = "parameter " + i;
// //             // input 요소 생성
// //             var inputElement = document.createElement("input");
// //             var inputHidden = document.createElement("input");
// //             inputElement.type = "text";
// //             inputHidden.type = "hidden";
// //             inputElement.name = "param" + i;
// //             inputHidden.name = "hiddenn" + i;
// //             inputElement.classList.add("form-control");
// //             // div 태그에 input 요소 추가
// //             divElement.appendChild(inputElement);
// //             // div 태그를 부모 요소에 추가
// //             parentElement.appendChild(divElement);
// //             parentElement1.appendChild(inputHidden);
// //             // 줄 바꿈
// //             var brElement = document.createElement("br");
// //             parentElement.appendChild(brElement);
// //         }
// //     }
// //
// //
// //     $("#computerGroupDataTable").on('click', 'tbody tr', function () {
// //         var $clickedRow = $(this);
// //         var isClicked = $clickedRow.hasClass('clicked');
// //         var tdValue = $clickedRow.find('td:eq(0)').text();
// //         // 클릭한 행의 상태에 따라 동작을 처리합니다.
// //         if (isClicked) {
// //
// //         // 클릭한 행이 이미 선택된 상태인 경우 선택 해제
// //         $clickedRow.removeClass('clicked');
// //         $clickedRow.css('background-color', '');
// //         resultC.innerHTML = resultC.innerHTML.replace(tdValue + '<br>', '');
// //         $('tbody tr').removeClass('disabled');
// //         // $('tbody tr').css('pointer-events', 'auto');
// //         } else {
// //         // 클릭한 행을 선택 상태로 하이라이트하고 다른 행의 클릭을 비활성화
// //         // $('tbody tr').not($clickedRow).css('pointer-events', 'none');
// //         $('tbody tr').not($clickedRow).addClass('disabled');
// //         $clickedRow.addClass('clicked');
// //         resultC.innerHTML += tdValue + '<br>';
// //         $clickedRow.css('background-color', 'orange');
// //         }
// //     });
// //
// //
// //     // if ($("#sbom_dataTable").length > 0) {
// //     var outputCValue = document.getElementById('outputC').textContent;
// //     document.getElementById('outputCValue').value = outputCValue;
// //     var errorMsgDiv = document.getElementById('errorMsg');
// //     var outputP = document.getElementById('cb1');
// //     var outputC = document.getElementById('cb2');
// //     var inputs = document.querySelectorAll('.outputP, .outputC');
// //     var parentElement1 = document.getElementById("pack");
// //
// //     inputs.forEach(function (input) {
// //         input.addEventListener('input', function () {
// //             errorMsgDiv.textContent = '';
// //         });
// //     });
// //
// //     document.getElementById('action_btn').addEventListener('click', function (event) {
// //         var outputPValue = document.getElementById('outputP').textContent;
// //         var outputCValue = document.getElementById('outputC').textContent;
// //         var inputElements = document.querySelectorAll("#colval3 input");
// //         var parentElement = document.getElementById("colval3");
// //
// //         inputs.forEach(function (input) {
// //             if (input.value === '') {
// //                 input.classList.add('error-border');
// //                 event.preventDefault();
// //             }
// //         });
// //
// //         // 에러 메시지 출력
// //         if (outputPValue === '' || outputCValue === '') {
// //             event.preventDefault();
// //             errorMsgDiv.textContent = 'package 또는 computer group을 선택해주세요.';
// //
// //         }else {
// //             // 두 개의 값이 모두 있는 경우 에러 메시지 제거
// //             errorMsgDiv.innerHTML = '<br/><br/>';
// //             document.getElementById('outputPValue').value = outputPValue;
// //             document.getElementById('outputCValue').value = outputCValue;
// //         }
// //
// //         inputElements.forEach(function(inputElement, index) {
// //             var hiddenInput = document.querySelector('input[name="hiddenn' +(index+1)+'"]');
// //             var paramInput = document.querySelector('input[name="param' +(index+1)+'"]');
// //             if (hiddenInput.length > 1) {
// //                 hiddenInput.value = inputElement.value;
// //                 paramInput.classList.remove("error")
// //                 alert(inputElement.value)
// //             }else {
// //                 event.preventDefault();
// //                 paramInput.classList.add("error")
// //                 errorMsgDiv.textContent = '파라미터 값을 입력해 주세요.';
// //             }
// //
// //         });
// //             if (confirm("배포하시겠습니까?") == true){
// //            //true는 확인버튼을 눌렀을 때 코드 작성
// //             }else{
// //                 event.preventDefault();
// //                 return;
// //             }
// //     });
// //         deploy_package();
// //         deploy_computerGroup();
// //         // sbom_detail_dataTable();
// //     // }
// // });
//
