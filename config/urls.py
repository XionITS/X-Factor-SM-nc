
from django.contrib import admin
from django.urls import path
from common import views_user
from common import views_main_hs
from common import views_os_ver

from common import views_export
from common import views_group


urlpatterns = [
    path('', views_user.login, name=''),
    path('login/', views_user.login, name='login'),
    path('signup/', views_user.signup, name='signup'),
    path('logout/', views_user.logout, name='logout/'),
    path('updateform/', views_user.updateform, name='updateform'),
    path('update/', views_user.update, name='update'),
    ############################################
    path('dashboard/', views_main_hs.dashboard),
    #path('admin/', admin.site.urls),
    #path('index/', views_main_hs.index),
    #path('index/paging/', views_main_hs.index_paging),
    path('hs_asset/', views_main_hs.hs_asset),
    path('hs_asset/hwpaging/', views_main_hs.hs_asset_paginghw),
    path('hs_asset/swpaging/', views_main_hs.hs_asset_pagingsw),
    path('export/<str:model>/', views_export.export, name='export'),


    path('ver_asset/', views_os_ver.ver_asset),
    path('ver_asset/paging/', views_os_ver.ver_asset_paging),
    path('ver_asset/create/', views_group.create),
    path('export/<str:model>/', views_export.export, name='export'),
]
