from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('mission/', views.mission, name='mission'),
  path('training/', views.training_list, name='training_list'),
  path('side-hustle/', views.side_hustle, name='side_hustle'),
  path("roadmap/", views.roadmap_home, name="roadmap_home"),
  path("roadmap/<slug:roadmap_slug>/<slug:page_slug>/", views.roadmap_page_detail, name="roadmap_page_detail"),
  path('ai-tools/', views.ai_tools, name='ai_tools'),
  path('calendar/', views.calendar, name='calendar'),
  path('gate/', views.gate, name='gate'),
  path('gate/logout/', views.gate_logout, name='gate_logout'),
  path("news/", views.news_list, name="news_list"),
  path("news/<slug:slug>/", views.news_detail, name="news_detail"),
  path("question-box/", views.question_box, name="question_box"),
]