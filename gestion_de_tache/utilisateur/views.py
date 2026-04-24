from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm, CustomSetPasswordForm, CustomSetPasswordForm, CustomUserCreationForm, RoleForm, ProfileRoleForm, PERMISSION_TRANSLATIONS
from .models import Profile
from tache.models import Task, Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required






# Create your views here.
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
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_tasks_total'] = Task.objects.count()
        context['count_tasks_todo'] = Task.objects.filter(status='todo').count()
        context['count_tasks_in_progress'] = Task.objects.filter(status='in_progress').count()
        context['count_tasks_done'] = Task.objects.filter(status='done').count()
        context['count_active_users'] = User.objects.filter(assigned_tasks__isnull=False).distinct().count()
        context['count_projects'] = Project.objects.count()

        return context
    
# authentification


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