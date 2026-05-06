from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Workspace
from .forms import WorkspaceForm


class OwnerQuerysetMixin(LoginRequiredMixin):
    """Restrict the queryset to objects owned by the current user."""
    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)


class WorkspaceListView(OwnerQuerysetMixin, ListView):
    model = Workspace
    template_name = 'workspaces/workspace_list.html'
    context_object_name = 'workspaces'


class WorkspaceDetailView(OwnerQuerysetMixin, DetailView):
    model = Workspace
    template_name = 'workspaces/workspace_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tasks'] = self.object.tasks.all()
        return ctx


class WorkspaceCreateView(LoginRequiredMixin, CreateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'workspaces/workspace_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkspaceUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'workspaces/workspace_form.html'


class WorkspaceDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Workspace
    template_name = 'workspaces/workspace_confirm_delete.html'
    success_url = reverse_lazy('workspace_list')
