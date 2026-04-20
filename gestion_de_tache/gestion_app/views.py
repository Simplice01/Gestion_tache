from django import contrib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from .models import Project, Task, Comment
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import  CustomUserCreationForm,CustomSetPasswordForm,CustomPasswordResetForm,RoleForm, ProfileRoleForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import Group 
from .forms import PERMISSION_TRANSLATIONS
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import views as auth_views

#Creation de projet
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/form_project.html'
    fields = ['name_project', 'deadline']
    success_url = reverse_lazy('list_project')
    

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
# mise à jour du statut d'un projet    
class UpdateStatusProjectView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/update_status_project.html'
    fields = ['statut']
    success_url = reverse_lazy('detail_project')  

# liste des projets
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/list_project.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.annotate(
            number_of_tasks=Count('tasks')
        ).order_by('-created_at')
    
# detail d'un projet
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project/detail_project.html'
    context_object_name = 'project'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(project=self.object).order_by('-created_at')
        assigned_users = (
            tasks.filter(assigned_to__isnull=False)
            .values('assigned_to__id', 'assigned_to__username')
            .distinct()
        )

        context['tasks'] = tasks
        context['assigned_users'] = assigned_users

        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de voir ce projet.")

        return obj
    
# édition d'un projet
class ProjectUpdateView(LoginRequiredMixin, UpdateView):  
    model = Project
    template_name = 'project/form_project.html'
    fields = ['name_project', 'deadline']
    success_url = reverse_lazy('list_project')
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.created_by != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de modifier ce projet.")
        
        return obj
    
# suppression d'un projet
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/list_project.html'
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de supprimer ce projet.")

        return obj

    def get_success_url(self):
        return reverse_lazy('list_project')
# liste des projets créés par l'utilisateur connecté
class MyProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/my_project_list.html'
    context_object_name = 'projects'
    

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user).order_by('-created_at')


# creation de tâche
class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task/form_task.html'
    fields = ['title', 'description', 'assigned_to', 'project']
    success_url = reverse_lazy('list_task')
    

    def form_valid(self, form):
        form.instance.status = 'todo'
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# liste des tâches
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/list_task.html'
    context_object_name = 'tasks'
    
    paginate_by = 5

    def get_queryset(self):
        return Task.objects.all().order_by('-created_at')

# detail d'une tâche
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/detail_task.html'
    context_object_name = 'task'
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                task=self.object,
                content=content,
                author=request.user
            )

        return redirect('detail_task', pk=self.object.id)  
    
# édition d'une tâche
class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task/form_task.html'
    fields = ['title', 'description', 'assigned_to', 'project']
    success_url = reverse_lazy('list_task')
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.created_by != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de modifier cette tâche.")
        
        return obj

# mise à jour du statut d'une tâche
class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task/task_status_form.html'
    fields = ['status']
    success_url = reverse_lazy('list_task')
    

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
# ajout d'un commentaire à une tâche    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'task/comment_form.html'
    fields = ['content']
    

    def form_valid(self, form):
        task_id = self.kwargs['pk']
        form.instance.task_id = task_id
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_task', kwargs={'pk': self.kwargs['pk']})    

# Modification d'un commentaire
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'tasks/comment_form.html'
    fields = ['content']
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de modifier ce commentaire.")

        return obj

    def get_success_url(self):
        return reverse_lazy('detail_task', kwargs={'pk': self.object.task.pk})   

# detail d'un commentaire
class DetailComment(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'task/comment_detail.html'
    context_object_name = 'comment'
       

# liste des commentaires d'une tâche
class ListComment(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'task/comment_list.html'
    context_object_name = 'comments'
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit.")

        return obj      

# suppression d'un commentaire
class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'tasks/detail_task.html'
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de supprimer ce commentaire.")

        return obj

    def get_success_url(self):
        return reverse_lazy('detail_task', kwargs={'pk': self.object.task.pk}) 
    
#  liste des tâches créées par l'utilisateur connecté    
class MyTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/my_task_list.html'
    context_object_name = 'tasks'
    
    
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user).order_by('-created_at')     
 
#suppression d'une tâche   
class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/list_task.html'
    

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise PermissionDenied("Vous n'avez pas le droit de supprimer cette tâche.")

        return obj

    def get_success_url(self):
        return reverse_lazy('list_task')

# liste des tâches assignées à un utilisateur
class ListTaskByUser(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/user_task_list.html'
    context_object_name = 'tasks'
    

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(assigned_to_id=user_id).order_by('-created_at')

# page d'accueil
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_tasks_total'] = Task.objects.count()
        context['count_tasks_todo'] = Task.objects.filter(status='todo').count()
        context['count_tasks_in_progress'] = Task.objects.filter(status='in_progress').count()
        context['count_tasks_done'] = Task.objects.filter(status='done').count()
        context['count_active_users'] = User.objects.filter(assigned_tasks__isnull=False).distinct().count()
        context['count_history_connexions'] = Profile.objects.filter(last_login__isnull=False).count()
        context['count_projects'] = Project.objects.count()

        return context
    
# authentification

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'email ou mot de passe incorrect'})

# déconnexion
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
# inscription d'utilisateur    
@login_required(login_url='login')
def register(request):
    if not request.user.profile.has_permission('add_user', app_label='auth'):
        raise PermissionDenied("Vous n'avez pas le droit de créer un utilisateur.")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
                

#Liste des rôles
class RoleListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'roles/list_role.html'
    context_object_name = 'roles'
    
    paginate_by = 5

    def get_queryset(self):
        return Group.objects.annotate(
            user_count=Count('profiles')
        )

# detail d'un rôle
class RoleDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'roles/detail_role.html'
    context_object_name = 'role'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        translated_permissions = []
        for permission in self.object.permissions.all():
            label = PERMISSION_TRANSLATIONS.get(permission.codename, permission.name)
            translated_permissions.append({
                'codename': permission.codename,
                'label': label
            })

        context['translated_permissions'] = translated_permissions
        return context


# création d'un rôle
class RoleCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = RoleForm
    template_name = 'roles/role_form.html'
    success_url = reverse_lazy('list_role')
    

# édition d'un rôle
class RoleUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = RoleForm
    template_name = 'roles/role_form.html'
    success_url = reverse_lazy('list_role')
    

class RoleDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'roles/role_confirm_delete.html'
    success_url = reverse_lazy('list_role')
    
# liste des profils
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list_users.html'
    context_object_name = 'users'
    
    paginate_by = 5

# édition du rôle d'un profil
class ProfileUpdateRoleView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileRoleForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('list_users')
    

 # page d'accueil          
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')    



@login_required(login_url='login')
def toggle_user_status(request, pk):
    if not request.user.profile.has_permission('change_user', app_label='auth'):
        raise PermissionDenied("Vous n'avez pas le droit de modifier les utilisateurs.")

    user = get_object_or_404(User, pk=pk)

    # éviter de se désactiver soi-même
    if user == request.user:
        raise PermissionDenied("Vous ne pouvez pas désactiver votre propre compte.")

    user.is_active = not user.is_active
    user.save()

    return redirect('list_users')    

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form_CUSTOM.html'
    email_template_name = 'registration/password_reset_email_CUSTOM.html'
    subject_template_name = 'registration/password_reset_subject_CUSTOM.txt'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done_CUSTOM.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm_CUSTOM.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete_CUSTOM.html'


class ListhystconnexionView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/historyconnexion.html'
    context_object_name = 'histories'

        