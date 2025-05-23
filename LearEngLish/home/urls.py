from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('hoso/', views.hoso, name='hoso'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
    path('ontap/', views.ontap, name='ontap'),
    path('reviewTest/<int:lesson_id>/', views.reviewTest, name='reviewTest'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
]