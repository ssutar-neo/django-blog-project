from django import forms
from django.contrib.auth.forms import UserCreationForm, \
AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Post,Comment

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.
                PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.
                PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'username': 'User Name', 'first_name': 'First Name', 
                'last_name': 'Last Name', 'email': 'Email'}
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
            }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"), strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        label = {'title': 'Title', 'description': 'Description'}
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        label = {'text': 'Text'}
        widgets = {
            # 'title': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
