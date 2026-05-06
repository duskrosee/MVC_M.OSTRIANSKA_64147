from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from workspaces.models import Workspace
from .models import Task
from .forms import TaskForm


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pw12345!')
        self.ws = Workspace.objects.create(name='Personal', owner=self.user)

    def test_create_task(self):
        t = Task.objects.create(
            title='Write report', content='Quarterly report',
            workspace=self.ws, owner=self.user, status='todo',
        )
        self.assertEqual(str(t), 'Write report')
        self.assertEqual(self.ws.tasks.count(), 1)


class TaskFormValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pw12345!')
        self.ws = Workspace.objects.create(name='W', owner=self.user)

    def test_past_deadline_rejected(self):
        form = TaskForm(data={
            'title': 'Test', 'content': '', 'deadline': date.today() - timedelta(days=1),
            'status': 'todo', 'workspace': self.ws.id,
        }, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('deadline', form.errors)

    def test_short_title_rejected(self):
        form = TaskForm(data={
            'title': 'A', 'content': '', 'deadline': '',
            'status': 'todo', 'workspace': self.ws.id,
        }, user=self.user)
        self.assertFalse(form.is_valid())


class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='carol', password='pw12345!')
        self.ws = Workspace.objects.create(name='Work', owner=self.user)
        Task.objects.create(title='Find bug', workspace=self.ws, owner=self.user, status='todo')
        Task.objects.create(title='Ship feature', workspace=self.ws, owner=self.user, status='done')

    def test_list_requires_login(self):
        resp = self.client.get(reverse('task_list'))
        self.assertEqual(resp.status_code, 302)

    def test_search_filters_results(self):
        self.client.login(username='carol', password='pw12345!')
        resp = self.client.get(reverse('task_list'), {'q': 'bug'})
        self.assertContains(resp, 'Find bug')
        self.assertNotContains(resp, 'Ship feature')
