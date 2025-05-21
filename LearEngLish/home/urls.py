from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('hoso/', views.hoso, name='hoso'),
    path('hoctumoi/<int:bai_hoc_id>/', views.hoctumoi, name='hoctumoi'), 
    path('hoanthanh/<int:bai_hoc_id>/', views.hoan_thanh_bai_hoc, name='hoanthanh'),
    path('ontap/', views.ontap, name='ontap'),
    path('hoanthanh/ontap/', views.hoan_thanh_ontap, name='hoan_thanh_ontap'),
    path('boqua/<int:bai_hoc_id>/', views.bo_qua_bai_hoc, name='bo_qua_bai_hoc'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
]