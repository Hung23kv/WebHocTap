from django.urls import path
from . import views
urlpatterns = [
    path('',views.homeChat,name='homeChat'),
    path('chat/<int:id>',views.ChatDetail,name = 'detailChat'),
    path('save-back/',views.save,name = 'save'),
    path('creatChat/',views.creatChat,name = 'create_chat'),
    path('ChatUser/<int:id>', views.ChatUser,name = 'chatuser'),
    path('chat_results/<int:id>', views.chat_results, name='chat_results'),
]