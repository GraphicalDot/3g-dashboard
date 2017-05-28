from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class MyUserCreationForm(UserCreationForm):
    """
    Form extends  UserCreationForm  for add email field.
    """
    email = forms.EmailField(label="Email", initial='@3gl.me')
    # owner = forms.IntegerField(label="Owner", required=False)

    class Meta:
        model = User
        fields = ('email', )


class MyUserChangeForm(UserChangeForm):
    """
    Extends UserCreationForm to change fields label.
    """
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].label = 'Mark as Admin'
        self.fields['is_superuser'].label = 'Mark as SuperUser'


