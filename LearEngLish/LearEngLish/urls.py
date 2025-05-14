"""
URL configuration for LearEngLish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home.dang_nhap, name="dang_nhap"),
    path('home/', home.trang_chu, name='trang_chu'),
    path('hoso/', home.hoso, name='hoso'),
    path('hoctumoi/<int:bai_hoc_id>/', home.hoctumoi, name='hoctumoi'), 
    path('hoanthanh/<int:bai_hoc_id>/', home.hoan_thanh_bai_hoc, name='hoanthanh'),
    path('ontap/', home.ontap, name='ontap'),
    path('hoanthanh/ontap/', home.hoan_thanh_ontap, name='hoan_thanh_ontap'),
    path('boqua/<int:bai_hoc_id>/', home.bo_qua_bai_hoc, name='bo_qua_bai_hoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

