from django.urls import path
from . import views

urlpatterns = [
  path('',views.homeLecturer,name = 'lecturer'),
  path('manage-lession/',views.manageLession,name = 'manage-lession'),
  path('manage-vocab/<int:lesson_id>/', views.manage_vocab, name='manage_vocab'),
  path('add-vocab/<int:lesson_id>/', views.add_vocab, name='add_vocab'),
  path('add-lesson/', views.add_lesson, name='add_lesson'),
  path('manage-conversation/', views.manage_conversation, name='manage-conversation'),
  path('add-conversation/', views.add_conversation, name='add_conversation'),
  path('manage-dialogue/<int:conversation_id>/', views.manage_dialogue, name='manage_dialogue'),
  path('delete-dialogue/<int:dialogue_id>/', views.delete_dialogue, name='delete-dialogue'),
  path('delete-vocab/<int:vocab_id>/', views.delete_vocab, name='delete-vocab'),
]