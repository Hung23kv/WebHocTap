from django.urls import path
from . import views
urlpatterns = [
    path('',views.homeChat,name='homeChat'),
    path('chat/<int:id>',views.ChatDetail,name = 'detailChat'),
    path('save-back/',views.save,name = 'save'),
    path('creatChat/',views.save,name = 'create_chat'),
]