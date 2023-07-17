
from django.contrib import admin
from django.urls import path
from common import views

urlpatterns = [
    path('', views.dashboard),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index/paging/', views.index_paging),
    path('hs_asset/', views.hs_asset),
    path('hs_asset/hwpaging/', views.hs_asset_paginghw),
    path('hs_asset/swpaging/', views.hs_asset_pagingsw),
]
