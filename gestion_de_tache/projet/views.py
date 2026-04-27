from django import contrib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView,  UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Project 
from tache.models import Task




# Create your views here.

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

        total_tasks = tasks.count()
        todo_tasks = tasks.filter(status='todo').count()
        in_progress_tasks = tasks.filter(status='in_progress').count()
        done_tasks = tasks.filter(status='done').count()

        completion_rate = 0
        if total_tasks > 0:
            completion_rate = round((done_tasks / total_tasks) * 100, 2)

        tasks_by_user = (
            tasks.filter(assigned_to__isnull=False)
            .values('assigned_to__username')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        context['tasks'] = tasks
        context['assigned_users'] = assigned_users

        context['total_tasks'] = total_tasks
        context['todo_tasks'] = todo_tasks
        context['in_progress_tasks'] = in_progress_tasks
        context['done_tasks'] = done_tasks
        context['completion_rate'] = completion_rate

        context['chart_status_labels'] = ['À faire', 'En cours', 'Terminées']
        context['chart_status_data'] = [todo_tasks, in_progress_tasks, done_tasks]

        context['chart_user_labels'] = [
            item['assigned_to__username'] for item in tasks_by_user
        ]
        context['chart_user_data'] = [
            item['total'] for item in tasks_by_user
        ]

        return context
    
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

