from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Task
from workspaces.models import Workspace


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'deadline', 'status', 'workspace']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'workspace': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['workspace'].queryset = Workspace.objects.filter(owner=user)

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline


class TaskFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search title or content...'}))
    status = forms.ChoiceField(required=False, choices=[('', 'All statuses')] + Task.STATUS_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    workspace = forms.ModelChoiceField(required=False, queryset=Workspace.objects.none(),
                                       empty_label='All workspaces',
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['workspace'].queryset = Workspace.objects.filter(owner=user)

