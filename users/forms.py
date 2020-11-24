from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput, TextInput, URLInput
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    # university = forms.TextChoice()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'birthday': DateInput(attrs={'type': 'date-local'}, format='%Y-%m-%d'),
            'bio': TextInput(attrs={'style': 'max-width: 300em'}),
            'university': TextInput(attrs={'style': 'max-width: 100em'}),
        }
        fields = ['image', 'telephone', 'birthday', 'bio', 'university', 'facebookURL', 'instagramURL', 'linkedinURL', 'twitterURL']
