
function user_list_popup() {
    var user_list_popup = function () {
        var user_list_popupData = $('#user_list_popupTable').DataTable({
            dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
            lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
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


