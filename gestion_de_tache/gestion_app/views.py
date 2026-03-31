from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from .models import Task, Comment
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task/form_task.html'
    fields = ['title', 'description', 'assigned_to']
    success_url = reverse_lazy('list_task')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.status = 'todo'
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/list_task.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_queryset(self):
        return Task.objects.all().order_by('-created_at')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/detail_task.html'
    context_object_name = 'task'
    login_url = 'login'


class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task/form_task.html'
    fields = ['title', 'description', 'assigned_to']
    success_url = reverse_lazy('list_task')
    login_url = 'login'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task/task_status_form.html'
    fields = ['status']
    success_url = reverse_lazy('list_task')
    login_url = 'login'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'task/comment_form.html'
    fields = ['content']
    login_url = 'login'

    def form_valid(self, form):
        task_id = self.kwargs['pk']
        form.instance.task_id = task_id
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_task', kwargs={'pk': self.kwargs['pk']})    

class CommentupdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'task/comment_form.html'
    fields = ['content']
    login_url = 'login'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('detail_task', kwargs={'pk': self.object.task.pk})    

class detail_comment(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'task/comment_detail.html'
    context_object_name = 'comment'
    login_url = 'login'   

class list_comment(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'task/comment_list.html'
    context_object_name = 'comments'
    login_url = 'login'

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Comment.objects.filter(task_id=task_id).order_by('-created_at')        

class delete_comment(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'task/comment_confirm_delete.html'
    fields = []
    login_url = 'login'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('detail_task', kwargs={'pk': self.object.task.pk})    
    
class delete_task(LoginRequiredMixin, UpdateView):  
    model = Task
    template_name = 'task/detail_task.html'
    fields = []
    login_url = 'login'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('list_task')

class list_task_by_user(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/user_task_list.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(assigned_to_id=user_id).order_by('-created_at')

class login_view(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'users/login.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_queryset(self):
        return Task.objects.all().order_by('-created_at')

class login_view(View):
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

class logout_view(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class register_view(View):
    def get(self, request):
        return render(request, 'users/register.html')
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
         return render(request, 'users/register.html', {'error': 'Remplissez tous les champs'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'Nom d\'utilisateur déjà pris'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')

class dashboard_view(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/dashboard.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by('-created_at')                  