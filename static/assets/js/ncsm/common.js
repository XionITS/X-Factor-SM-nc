
// ----------------------------------------- user_list_popup start -----------------------------------------

function user_list_popup() {
    var user_list_popup = function () {
        var user_list_popupData = $('#user_list_popupTable').DataTable({
            dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
            lengthMenu: [[5, 10, 15, 20, 25], [5, 10, 15, 20, 25]],
            responsive: true,
            searching: true,
            ordering: false,
            serverSide: true,
            displayLength: false,

            ajax: {
                url: 'paging/',
                type: "POST",
                dataSrc: function (res) {
                    var data = res.item;
                    return data;
                }
            },
            columns: [
                {data: 'group_id'},
                {data: 'group_name'},
                {data: 'group_note'},
            ],
            columnDefs: [
                {targets: 0, width: "30%", className: 'text-start text-truncate flex-cloumn'},
                {targets: 1, width: "30%", className: 'text-start text-truncate flex-cloumn'},
                {targets: 2, width: "40%", className: 'text-start text-truncate flex-cloumn'},
            ],
    //		columnDefs: [
    //		    {targets: 0, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.group_id+'" data-toggle="tooltip">'+data+'</span>'}},
    //		    {targets: 1, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.group_name+'" data-toggle="tooltip">'+data+'</span>'}},
    //		    {targets: 2, width: "70%", className: 'text-start text-truncate', render: function(data, type, row) {return '<span title="'+row.group_note+'" data-toggle="tooltip">'+data+'</span>'}},
    //		],
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
    };
}
// ----------------------------------------- user_list_popup end -----------------------------------------

// ----------------------------------------- delploy_popup end -----------------------------------------



//function sidebar() {
//    const appElement = document.getElementById('app');
//    $('html').click(function(e){
//            var sidebar = $('#sidebar');
//            var app = $('#app');
//            if(!$(e.target).hasClass('app-sidebar-content') && !$(e.target).hasClass('menu-toggler') && !$(e.target).hasClass('app-sidebar')){
//                sidebar.css({'display':'none'});
//                app.removeClass("app-sidebar-toggled");
//                app.addClass("app-sidebar-collapsed");
//            }
//            else{
//                sidebar.css({'display':'block'});
//            }
//        });
//}

//     console.log($tbody +"_checkbox_check() called");
//     $tbody.off('click', 'tr');
//     $tbody.on('click', 'tr', function () {
//         var checkbox = $(this).find('input[type="checkbox"]');
//         var hidden = $(this).find('input[type="hidden"]');
//         var computer_id = checkbox.attr('id');
//         console.log(computer_id)
//         var computer_name = checkbox.attr("name");
//         checkbox.prop('checked', !checkbox.prop('checked'));
//         if (checkbox.prop('checked')) {
//             checkedItems[computer_id] = computer_name;
//         } else {
//             delete checkedItems[computer_id];
//         }
//     });

// ----------------------------------------- check box start -----------------------------------------
function checkbox_check($tbody){
    $tbody.on('click', 'input[type="checkbox"]', function (event) {
        event.stopPropagation(); // Prevent the row click event from firing when clicking the checkbox
        var computer_id = $(this).data('computer-id');
        var computer_name = $(this).data('computer-name');
        // console.log("Clicked checkbox for computer ID:", computer_id);
        if ($(this).prop('checked')) {
            checkedItems[computer_id] = computer_name;
        } else {
            delete checkedItems[computer_id];
        }
    });
}

// $(document).ready(function () {
//     var $tbody_os = $('#os_asset_list tbody');
//     var $tbody_ver = $('#ver_asset_list tbody');
//
//     checkbox_check($tbody_os);
//     checkbox_check($tbody_ver);
// });
// ----------------------------------------- check box end -----------------------------------------
// ------------------------------------------ create group start ------------------------------------------

$(document).on("click","#creategroup", function (e){
    $("#groupName").val("");
    $("#groupDescription").val("");
    const check_id = [];
    const check_name = [];
    var modalbody = "";
    for (const computer_id in checkedItems) {
        const computer_name = checkedItems[computer_id];
        //modalbody += '<div><input type="hidden" name="'+computer_id+'" id="'+computer_id+'" value="'+computer_id+'">'+computer_name+'</div>'
        //modalbody += '<input type="hidden" name="'+computer_name+'" id="'+computer_name+'" value="'+computer_name+'">'
        //modalbody += '컴퓨터아이디'+computer_id + '<br/>';
        //modalbody += '컴퓨터이름'+computer_name + '<br/>';
        modalbody += '<div id="'+computer_id+'"><input class="form-check-input" type="checkbox" value="'+computer_id+'" id="'+computer_id+'" computer-name="' + computer_name +'" checked><label class="form-check-label" for="'+computer_id+'">'+computer_name+'</label><br></div>'
    }
    $("#groupModal .modal-title").html("그룹 생성 팝업창");
    $("#groupModal .form-check").html(modalbody);
    $("#groupModal").modal("show");
    $(document).on('change', '.form-check-input', function() {
        var x_id = $(this).val();
        if (!this.checked) { // 체크박스가 해제된 경우
            // 해당 체크박스를 #group_insert_modal .form-check2에서 제거
            // $('label[for="'+x_id+'"]').remove();
            $('div[id="'+x_id+'"]').remove();
            // $(".user-checkbox[data-x-id='" + escapeSelector(x_id) + "']").prop('checked', false);
        }
    });
});



$(document).on("click","#groupCreate", function(event) {
    event.preventDefault(); // 기본 제출 동작을 막습니다.
    // 폼 데이터를 가져옵니다.
    var form = document.getElementById("GroupCreateForm");
    var group_name = form.elements.groupName.value;
    var group_description = form.elements.groupDescription.value;
    let computerIds = []
    let computerNames = []
    const computerElements = $('#groupModal .form-check').find('.form-check-input');
    computerElements.each(function () {
        const computer_id = $(this).attr("id");

        //console.log(computer_id);
        const computer_name = $(this).attr('computer-name');
        computerIds.push(computer_id);
        computerNames.push(computer_name);
    });
    if (group_name === ''){
        alert('그룹이름을 작성해 주세요.')
        return
    }
    if (computerNames.length === 0 || computerIds.length === 0){
        alert('자산을 선택해 주세요.')
        return
    }
    $.ajax({
    url: '../create/', // views.py 파일의 URL을 여기에 넣으세요.
    type: 'POST',
    dataType: 'json',
    data:  {
         'group_name' : group_name,
         'group_description' : group_description,
         'computerIds' : JSON.stringify(computerIds),
         'computerNames' : JSON.stringify(computerNames),
    },
    data:  {
         'group_name' : group_name,
         'group_description' : group_description,
         'computerIds' : JSON.stringify(computerIds),
         'computerNames' : JSON.stringify(computerNames),
    },
    success: function (response) {
    // response에 따른 처리 - 예: 경고창 띄우기
        if (response.success == "success") {
            alert(response.message);
            $('#groupModal').modal('hide');
        } else {
            alert('실패 : ' + response.message);
        }
    }
    });
});
// ------------------------------------------ create group end ------------------------------------------
// ------------------------------------------ setting start ------------------------------------------


// setting_ver 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#settingVerBtn", function (e) {
    $.ajax({
        url: 'setting_ver_list/',
        method: 'POST',
        success: function (res) {
            var modalbody = '<br><div class=h5>&nbsp;&nbsp;&nbsp; Windows 버전별 자산현황</div><br>';
            modalbody += '<div style="display: flex; align-items:center; justify-content: center;"> <div class=h6>Version : &nbsp;</div><select class="form-select form-select-lg form-setting h5">';
            for (var i = 0; i < res.ver_list.length; i++) {
                if (res.ver_list[i] === res.current_value) {
                    modalbody += '<option value="' + res.ver_list[i] + '" class=h6 selected> 현재값 : ' + res.ver_list[i] + '</option>';
                }else if (res.ver_list[i] === res.next_value) {
                    modalbody += '<option value="' + res.ver_list[i] + '" class=h6> 다음값 : ' + res.ver_list[i] + '</option>';
                }else {
                    modalbody += '<option value="' + res.ver_list[i] + '" class=h6>' + res.ver_list[i] + '</option>';
                }
            }

            modalbody += '</select></div><br><br>';
            $("#settingsModal .setting_modal-body").html(modalbody);
            $("#settingsModal .Save_changes").attr("id", "setting_ver_save");
            $("#settingsModal").modal("show");
        }
    });
});

// setting_ver 세팅 세이브 버튼 클릭 이벤트 핸들러
$(document).on("click", "#setting_ver_save", function (e) {
    var selectedValue = $(".form-setting").val(); // 선택한 버전 값 가져오기
    $.ajax({
        url: 'update_ver_module/',
        method: 'POST',
        data: { value: selectedValue }, // 선택한 버전을 서버로 전달
        success: function (res) {
            alert("Windows 버전 기준 수정이 변경되었습니다.")
            $("#settingsModal").modal("hide");
        },
        error: function (err) {
            alert("Windows 버전 기준 수정 중 오류가 발생했습니다.");
            $("#settingsModal").modal("hide");
        }
    });
})


// setting_hot 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#settingHotBtn", function (e) {
    $.ajax({
        url: 'setting_hot_list/',
        method: 'POST',
        success: function (res) {
            var modalbody = '<br><div class=h5>&nbsp;&nbsp;&nbsp; 보안 패치별 자산현황</div><br>';
            modalbody += '<div style="display: flex; align-items:center; justify-content: center;"><select class="form-select form-select-lg form-setting h5">';
            for (var i = 0; i < res.hot_list.length; i++) {
                if (res.hot_list[i] === res.current_value) {
                    modalbody += '<option value="' + res.hot_list[i] + '" class=h6 selected> 현재값 : ' + res.hot_list[i] + '</option>';
                }else if (res.hot_list[i] === res.next_value) {
                    modalbody += '<option value="' + res.hot_list[i] + '" class=h6> 다음값 : ' + res.hot_list[i] + '</option>';
                }else {
                    modalbody += '<option value="' + res.hot_list[i] + '" class=h6>' + res.hot_list[i] + '</option>';
                }
            }

            modalbody += '</select><div class=h6>&nbsp; 개월</div></div><br><br>';
            $("#settingsModal .setting_modal-body").html(modalbody);
            $("#settingsModal .Save_changes").attr("id", "setting_hot_save");
            $("#settingsModal").modal("show");
        }
    });
});


// setting_hot 세팅 세이브 버튼 클릭 이벤트 핸들러
$(document).on("click", "#setting_hot_save", function (e) {
    var selectedValue = $(".form-setting").val(); // 선택한 버전 값 가져오기
    $.ajax({
        url: 'update_hot_module/',
        method: 'POST',
        data: { value: selectedValue }, // 선택한 버전을 서버로 전달
        success: function (res) {
            alert("보안패치 기간 기준 수정이 변경되었습니다.")
            $("#settingsModal").modal("hide");
        },
        error: function (err) {
            alert("보안패치 기간 기준 수정 중 오류가 발생했습니다.");
            $("#settingsModal").modal("hide");
        }
    });
})


// setting_discover 모달 열기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#settingDiscoverBtn", function (e) {
    $.ajax({
        url: 'setting_discover_list/',
        method: 'POST',
        success: function (res) {
            var modalbody = '<br><div class=h5>&nbsp;&nbsp;&nbsp; 장기 미접속 자산</div><br>';
            modalbody += '<div style="display: flex; align-items:center; justify-content: center;"><select class="form-select form-select-lg form-setting h5">';
            for (var i = 0; i < res.discover_list.length; i++) {
                if (res.discover_list[i] === res.current_value) {
                    modalbody += '<option value="' + res.discover_list[i] + '" class=h6 selected> 현재값 : ' + res.discover_list[i] + '</option>';
                }else if (res.discover_list[i] === res.next_value) {
                    modalbody += '<option value="' + res.discover_list[i] + '" class=h6> 다음값 : ' + res.discover_list[i] + '</option>';
                }else {
                    modalbody += '<option value="' + res.discover_list[i] + '" class=h6>' + res.discover_list[i] + '</option>';
                }
            }

            modalbody += '</select><div class=h6>&nbsp; 일</div></div><br><br>';
            $("#settingsModal .setting_modal-body").html(modalbody);
            $("#settingsModal .Save_changes").attr("id", "setting_discover_save");
            $("#settingsModal").modal("show");
        }
    });
});


// setting_discover 세팅 세이브 버튼 클릭 이벤트 핸들러
$(document).on("click", "#setting_discover_save", function (e) {
    var selectedValue = $(".form-setting").val(); // 선택한 버전 값 가져오기
    $.ajax({
        url: 'update_discover_module/',
        method: 'POST',
        data: { value: selectedValue }, // 선택한 버전을 서버로 전달
        success: function (res) {
            alert("장기미접속 기간 기준 수정이 변경되었습니다.")
            $("#settingsModal").modal("hide");
        },
        error: function (err) {
            alert("장기미접속 기간 기준 수정 중 오류가 발생했습니다.");
            $("#settingsModal").modal("hide");
        }
    });
})



// setting_ver 모달 닫기 버튼 클릭 이벤트 핸들러
$(document).on("click", "#settingCloseBtn", function (e) {
    $("#settingsModal").modal("hide");
});


// 모달 외부 클릭 시 닫기 이벤트 핸들러
window.onclick = function (event) {
    if (event.target == modal) {
        $("#settingsModal").modal("hide");
    }
};

//  ------------------------------------------ setting end ------------------------------------------












// 검색 버튼 클릭, 엔터 키로 선택한 컬럼과 검색어로 검색 수행
function performSearch(column, searchValue, list_Data) {
    //console.log(column)
    //console.log(searchValue)
    if (searchValue !== ''){
        list_Data.columns().search('').draw();
        list_Data.column(column).search(searchValue).draw();
    }
}
//////////////////////////////////////////////////////////////////

$(document).ready(function () {
    user_list_popup();
    //sidebar();
    //initEvent();

    //initializeDataTable();
});
