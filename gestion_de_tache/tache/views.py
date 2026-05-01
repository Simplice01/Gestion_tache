from django import contrib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from .models import Task, Comment
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import Group 
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.db.models import Count, IntegerField, Value
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.db.models import Case, When, Value, IntegerField


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
        queryset = (
            Task.objects
            .select_related('assigned_to', 'created_by')
            .annotate(
                is_my_task=Case(
                    When(assigned_to=self.request.user, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            )
        )

        filter_type = self.request.GET.get('filter')

        if filter_type == 'my':
            queryset = queryset.filter(assigned_to=self.request.user)

        elif filter_type == 'my_todo':
            queryset = queryset.filter(
                assigned_to=self.request.user,
                status='todo'
            )

        elif filter_type == 'my_in_progress':
            queryset = queryset.filter(
                assigned_to=self.request.user,
                status='in_progress'
            )

        elif filter_type == 'my_done':
            queryset = queryset.filter(
                assigned_to=self.request.user,
                status='done'
            )

        elif filter_type == 'my_valid':
            queryset = queryset.filter(
                assigned_to=self.request.user,
                status='valid'
            )    

        elif filter_type == 'created_by_me':
            queryset = queryset.filter(created_by=self.request.user)

        return queryset.order_by('is_my_task', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_filter'] = self.request.GET.get('filter', 'all')

        context['count_my_tasks'] = Task.objects.filter(
            assigned_to=self.request.user
        ).count()

        context['count_my_todo'] = Task.objects.filter(
            assigned_to=self.request.user,
            status='todo'
        ).count()

        context['count_my_in_progress'] = Task.objects.filter(
            assigned_to=self.request.user,
            status='in_progress'
        ).count()

        context['count_my_done'] = Task.objects.filter(
            assigned_to=self.request.user,
            status='done'
        ).count()

        context['count_my_valid'] = Task.objects.filter(
            assigned_to=self.request.user,
            status='valid'
        ).count()

        return context

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


        