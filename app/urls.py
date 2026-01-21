from django.urls import path, reverse
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path("projects/vision-ia/", views.project_vision, name="project_vision"),
    path("projects/newsletter-ia/", views.project_newsletter, name="project_newsletter"),
    path("projects/midai/", views.project_midai, name="project_midai"),
    path("about/", views.about, name="about"),
]

