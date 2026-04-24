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
    # page d'accueil   
    path('', views.HomeView.as_view(), name='home'),  
    #authentification
    path('login/', views.LoginView.as_view(), name='login'),
    # déconnexion
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # inscription d'utilisateur
    path('register/', views.register, name='register'), 

    #dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # gestion des rôles
    path('roles/', views.RoleListView.as_view(), name='list_role'),
    path('roles/create/', views.RoleCreateView.as_view(), name='form_role'),
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='detail_role'),
    path('roles/<int:pk>/edit/', views.RoleUpdateView.as_view(), name='role_edit'),
    path('roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='role_delete'),

    # gestion des profils
    path('profiles/', views.UserListView.as_view(), name='list_users'),
    path('profiles/<int:pk>/edit-role/', views.ProfileUpdateRoleView.as_view(), name='edit_profile'),
    path('users/<int:pk>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    # réinitialisation du mot de passe
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('historyconnexion/', views.ListhystconnexionView.as_view(), name='historyconnexion'),
    
]