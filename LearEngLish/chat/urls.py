from django.urls import path
from . import views
urlpatterns = [
    path('',views.homeChat,name='homeChat'),
    path('chat/<int:idQ>',views.ChatDetail,name = 'detailChat'),
]