from django.urls import path
from . import views
urlpatterns = [
    path('chat',views.homeChat,name='homeChat'),
    path('chat/<int:id>',views.ChatDetail,name = 'detailChat'),
    path('save-back/',views.save,name = 'save'),
    path('creatChat/',views.creatChat,name = 'create_chat'),
    path('Login/',views.Login,name = 'Login'),
    path('ChatUser/<int:id>', views.ChatUser,name = 'chatuser'),
]