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
from gestion_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     # page d'accueil   
    path('', views.HomeView.as_view(), name='home'),    
    # formulaire de création de tâche
    path('form_task/', views.CreateTask.as_view(), name='form_task'),
    # liste des tâches
    path('tasks/', views.TaskListView.as_view(), name='list_task'),
    # détail d'une tâche
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='detail_task'),
    # édition d'une tâche
    path('task/<int:pk>/edit/', views.TaskEditView.as_view(), name  ='edit_task'), 
    # mise à jour du statut d'une tâche
    path('task/<int:pk>/status/', views.TaskStatusUpdateView.as_view(), name='update_status'),
    # ajout d'un commentaire à une tâche
    path('task/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    # suppression d'un commentaire
    path('comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    # liste des tâches créées par l'utilisateur connecté
    path('my_tasks/', views.MyTaskListView.as_view(), name='my_task_list'),
    # suppression d'une tâche
    path('task/<int:pk>/delete/', views.DeleteTask.as_view(), name='delete_task'),
    # authentification
    path('login/', views.LoginView.as_view(), name='login'),
    # déconnexion
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # inscription d'utilisateur
    path('register/', views.register, name='register'), 
    # liste des tâches assignées à un utilisateur
    path('user_tasks/', views.ListTaskByUser.as_view(), name='user_task_list'),
    #dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # gestion des rôles
    path('roles/', views.RoleListView.as_view(), name='list_role'),
    path('roles/create/', views.RoleCreateView.as_view(), name='form_role'),
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='detail_role'),
    path('roles/<int:pk>/edit/', views.RoleUpdateView.as_view(), name='role_edit'),
    path('roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='role_delete'),

    # gestion des profils
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/edit-role/', views.ProfileUpdateRoleView.as_view(), name='profile_role_edit'),
    
    # réinitialisation du mot de passe
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
