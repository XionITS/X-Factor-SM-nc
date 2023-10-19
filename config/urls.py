
from django.contrib import admin
from django.urls import path
from common import views_user, views_sec, views_dashboard_detail
from common import views_main_hs
from common import views_os_ver
from common import views_up
from common import views_deploy
from common import views_export
from common import views_group

from common import views_pur_asset

from common import views_asset
from common import views_history
from common import views_user_management
from common import views_group_management
from common import views_log_management
from common import views_report
from common.CallbackView import CallbackView
from common.LoginView import LoginView

urlpatterns = [
    #path('', views_user.nano, name=''),
    path('', views_user.login, name=''),
    path('login/', views_user.login, name='login'),
    path('nano/', views_user.nano),
    path('dashboard/', views_user.nano_user),
    path('signup/', views_user.signup, name='signup'),
    path('logout/', views_user.logout, name='logout/'),
    path('updateform/', views_user.updateform, name='updateform'),
    path('update/', views_user.update, name='update'),
    ############################################
    path('home/', views_main_hs.dashboard),
    path('home1/', views_main_hs.dashboard1),
    path('home/all_asset_paging1/', views_dashboard_detail.all_asset_paging1),
    path('home/asset_os_paging1/', views_dashboard_detail.asset_os_paging1),
    path('home/asset_os_paging2/', views_dashboard_detail.asset_os_paging2),
    path('home/oslistPieChart/', views_dashboard_detail.oslistPieChart),
    path('home/osVerPieChart/', views_dashboard_detail.osVerPieChart),
    path('home/office_chart/', views_dashboard_detail.office_chart),
    #path('admin/', admin.site.urls),
    #path('index/', views_main_hs.index),
    #path('index/paging/', views_main_hs.index_paging),
    path('hs_asset/', views_main_hs.hs_asset),
    path('hs_asset/hwpaging/', views_main_hs.hs_asset_paginghw),
    path('hs_asset/swpaging/', views_main_hs.hs_asset_pagingsw),
    path('export/<str:model>/', views_export.export, name='export'),


    path('ver_asset/', views_os_ver.ver_asset),
    path('ver_asset/paging/', views_os_ver.ver_asset_paging),
    path('export/<str:model>/', views_export.export, name='export'),


    path('os_asset/', views_os_ver.os_asset),
    path('os_asset/paging/', views_os_ver.os_asset_paging),

    path('up_asset/', views_up.up_asset),
    path('up_asset/paging/', views_up.up_asset_paging),

    path('sec_asset/', views_sec.sec_asset),
    path('sec_asset/paging/', views_sec.sec_asset_paging),
    path('sec_asset_list/', views_sec.sec_asset_list),
    path('sec_asset_list/paging/', views_sec.sec_asset_list_paging),


    path('create/', views_group.create),
    path('group/list/', views_deploy.group),
    path('package/list/', views_deploy.package),
    path('deploy_action/', views_deploy.deploy_action),
    path('member/list/', views_deploy.group_list),


    #구매팀 페이지
    path('pur_asset/', views_pur_asset.pur_asset),
    path('pur_asset/pur_hwpaging/', views_pur_asset.pur_asset_paginghw),
    path('pur_asset/pur_swpaging/', views_pur_asset.pur_asset_pagingsw),

    #Asset 페이지
    path('asset/', views_asset.asset),
    path('asset/search/', views_asset.search),
    path('asset/search_box/', views_asset.search_box),
    path('asset/save_memo/', views_asset.save_memo),

    #history 페이지
    path('history/', views_history.history),
    path('history/search_h/', views_history.search_h),
    path('history/search_box_h/', views_history.search_box_h),
    # path('history/history1/', views_history.select_date_l),
    # path('history/history2/', views_history.select_date_r),


    #Setting 페이지
    path('user_management/', views_user_management.um, name='user_management'),
    path('user_management/user_auth/', views_user_management.user_auth, name='user_auth'),
    path('user_management/group_auth/', views_user_management.group_auth, name='group_auth'),
    path('user_management/save_user_auth/', views_user_management.save_user_auth, name='save_user_auth'),
    path('user_management/save_group_auth/', views_user_management.save_group_auth, name='save_group_auth'),
    path('user_management/groupcreate_auth/', views_user_management.create_auth, name='create_auth'),
    path('user_management/groupalter_auth/', views_user_management.alter_auth, name='alter_auth'),
    #path('user_management/signup/', views_user.signup, name='um_signup'),
    path('user_management/um_delete/', views_user.delete, name='um_delete'),
    path('user_management/group_delete/', views_user.group_delete, name='group_delete'),
    path('user_management/userpaging/', views_user_management.um_user),
    path('user_management/grouppaging/', views_user_management.um_group),
    path('user_management/search_box/', views_user_management.search_box),
    #path('group_management', views_group_management.group),
    path('log_management/', views_log_management.log),
    path('log_management/paging/', views_log_management.log_paging),

    #Report
    path('report/', views_report.create, name='report_date'),


    # path('login/', LoginView.as_view(), name='login'),
    # path('callback/', CallbackView.as_view(), name='callback'),

]

