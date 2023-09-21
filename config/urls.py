
from django.contrib import admin
from django.urls import path
from common import views_user, views_sec
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



urlpatterns = [
    path('', views_user.login, name=''),
    path('login/', views_user.login, name='login'),
    path('signup/', views_user.signup, name='signup'),
    path('logout/', views_user.logout, name='logout/'),
    path('updateform/', views_user.updateform, name='updateform'),
    path('update/', views_user.update, name='update'),
    ############################################
    path('dashboard/', views_main_hs.dashboard),
    path('dashboard1/', views_main_hs.dashboard1),
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

    #history 페이지
    path('history/', views_history.history),
    path('history/search_h/', views_history.search_h),
    path('history/search_box_h/', views_history.search_box_h),
    # path('history/history1/', views_history.select_date_l),
    # path('history/history2/', views_history.select_date_r),


    #Setting 페이지
    path('user_management', views_user_management.user),
    path('group_management', views_group_management.group),
    path('log_management/', views_log_management.log),
    path('log_management/paging/', views_log_management.log_paging),
]

