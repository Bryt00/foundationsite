from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('about/', views.about, name='about'),
    path('impact/', views.impact, name='impact'),
    path('programs/', views.programs, name='programs'),
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.story_detail, name='story_detail'),
    path('join/', views.join, name='join'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('stories/<slug:slug>/', views.success_story_detail, name='success_story_detail'),
]
