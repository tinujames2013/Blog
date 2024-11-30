from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import Blog,Comment,create_profile
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm

def home(request):
    """Display only published blogs."""
    blogs = Blog.objects.filter(status='publish', author__is_active=True)
    return render(request, 'sitevisitor/home.html', {'blogs': blogs})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('sitevisitor:home')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'sitevisitor/login.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('sitevisitor:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'sitevisitor/registration.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request, use_https=request.is_secure())
            messages.success(request, "Password reset email sent.")
            return redirect('sitevisitor:login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'sitevisitor/forgot_password.html', {'form': form})

def reset_password(request):
    return render(request, 'sitevisitor/reset_password.html')
def otp(request):
    return render(request, 'sitevisitor/otp.html')

def comments_for_blog(request, blog_id):
    """Show comments only for visible blogs."""
    blog = get_object_or_404(Blog, id=blog_id, status='publish', is_visible=True, author__is_active=True)
    comments = Comment.objects.filter(blog=blog, status='show')
    return render(request, 'userpanel/comments.html', {'blog': blog, 'comments': comments})

def blog_list(request):
    """Display only blogs that are published and belong to active users."""
    blogs = Blog.objects.filter(status='publish', author__is_active=True)
    return render(request, 'sitevisitor/blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    """
    Display a single blog if it is published, visible, and authored by an active user.
    """
    blog = get_object_or_404(Blog, id=blog_id, status='publish', is_visible=True, author__is_active=True)
    comments = Comment.objects.filter(blog=blog, status='show')
    return render(request, 'sitevisitor/blog_detail.html', {'blog': blog, 'comments': comments})

