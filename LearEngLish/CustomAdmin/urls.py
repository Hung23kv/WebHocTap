from django.urls import path
from . import views

urlpatterns = [
  path('',views.homeAdmin,name = 'Customadmin'),
  path('manage-coures/',views.manageCoures,name = 'manage-coures'),
  path('addLecturer/',views.addLecturer,name = 'addLecturer'),
  path('addCourse/',views.addCourse,name = 'addCourse'),
  path('track-users/',views.track_users,name = 'track_users'),
]