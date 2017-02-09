from django import forms
from .models import Task


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TaskAssignForm(forms.Form):

    class Meta:
        model = Task
        fields = ['title', 'description', 'assign_to', 'due_date']
