from django.urls import path
from . import views

urlpatterns = [
  path('',views.homeAdmin,name = 'admin'),
  path('manage-coures/',views.manageCoures,name = 'manage-coures'),
]