from django import forms
from adminpanel.models import Blog
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from adminpanel.models import Blog, Profile, Comment
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'status']

class AdminLoginForm(AuthenticationForm):
    """Custom admin login form."""
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))

class AdminPasswordChangeForm(PasswordChangeForm):
    """Form for admins to change their password."""
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ToggleUserStatusForm(forms.ModelForm):
    """Form to toggle user active status."""
    class Meta:
        model = User
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class ToggleBlogVisibilityForm(forms.ModelForm):
    """Form to toggle blog visibility."""
    class Meta:
        model = Blog
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[('publish', 'Publish'), ('draft', 'Draft')]),
        }
