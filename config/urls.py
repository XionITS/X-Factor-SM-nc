
from django.contrib import admin
from django.urls import path
from common import views

urlpatterns = [
    path('', views.dashboard),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index/paging/', views.index_paging),
]
