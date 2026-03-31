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
    path('tasks/', views.ListTaskView.as_view(), name='list_task'),
]
