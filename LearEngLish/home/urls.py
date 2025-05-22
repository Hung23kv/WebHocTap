from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('hoso/', views.hoso, name='hoso'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
]