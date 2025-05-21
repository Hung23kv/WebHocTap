from django.urls import path
from . import views

urlpatterns = [
  path('',views.homeLecturer,name = 'lecturer'),
  path('manage-lession/',views.manageLession,name = 'manage-lession'),
  path('manage-vocab/<int:lesson_id>/', views.manage_vocab, name='manage_vocab'),
]