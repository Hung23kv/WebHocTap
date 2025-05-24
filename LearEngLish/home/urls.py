from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('hoso/', views.hoso, name='hoso'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
    path('ontap/', views.ontap, name='ontap'),
    path('reviewTest/<int:lesson_id>/', views.reviewTest, name='reviewTest'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
    path('dang-ky/', views.dang_ky, name='dang_ky'),
    path('quen-mat-khau/', views.quen_mat_khau, name='quen_mat_khau'),
    path('chon-cap-do/', views.chon_cap_do, name='chon_cap_do'),
]