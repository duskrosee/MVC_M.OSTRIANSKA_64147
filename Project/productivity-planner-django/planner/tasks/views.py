from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView,
)

from .models import Task
from .forms import TaskForm, TaskFilterForm, RegisterForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class OwnerTaskMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related('workspace')


class TaskListView(OwnerTaskMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_form = TaskFilterForm(self.request.GET or None, user=self.request.user)
        if self.filter_form.is_valid():
            q = self.filter_form.cleaned_data.get('q')
            status = self.filter_form.cleaned_data.get('status')
            workspace = self.filter_form.cleaned_data.get('workspace')
            if q:
                qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
            if status:
                qs = qs.filter(status=status)
            if workspace:
                qs = qs.filter(workspace=workspace)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = self.filter_form
        return ctx


class TaskDetailView(OwnerTaskMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(OwnerTaskMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDeleteView(OwnerTaskMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
