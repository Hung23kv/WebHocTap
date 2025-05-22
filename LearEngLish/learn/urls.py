from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeLear, name='homeLear'),
    path('vocab/<int:lesson_id>/', views.vocab, name='vocab'),
    path('complete_lesson/<int:lesson_id>/', views.complete_lesson, name='complete_lesson'),
]