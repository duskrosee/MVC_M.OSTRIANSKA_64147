from django.conf import settings
from django.db import models
from django.urls import reverse


class Workspace(models.Model):
    """A container for tasks (One-to-Many: Workspace -> Tasks)."""
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workspaces',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('workspace_detail', args=[self.pk])
