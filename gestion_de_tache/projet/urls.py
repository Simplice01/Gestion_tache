"""
URL configuration for gestion_de_tache project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='list_project'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='form_project'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='detail_project'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='edit_project'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete_project'),
    path('projects/<int:pk>/update-status/', views.UpdateStatusProjectView.as_view(), name='update_status_project'), 
]