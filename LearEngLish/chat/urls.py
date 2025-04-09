from django.urls import path
from . import views
urlpatterns = [
    path('',views.homeChat,name='homeChat'),
    path('chat',views.ChatDetail,name = 'detailChat'),
]