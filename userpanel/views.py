from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from adminpanel.models import Profile, Blog, Comment
from .forms import ProfileForm, BlogForm, CommentForm, RegistrationForm, ResetPasswordForm,DeleteConfirmationForm
from django.contrib.auth import logout

# User Home
@login_required
def user_home(request):
    blogs = Blog.objects.filter(author=request.user)
    context = {
        'blogs': blogs
    }
    return render(request, 'userpanel/user_home.html', context)


# Public Home View for All Blogs
def home(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs
    }
    return render(request, 'userpanel/home.html', context)


# View Profile
@login_required
def view_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'userpanel/view_profile.html', context)

# Edit Profile
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('userpanel:view_profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'userpanel/edit_profile.html', context)

@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()  # Save the blog before accessing blog.id
            messages.success(request, "Blog created successfully!")
            return redirect('userpanel:view_blog', blog_id=blog.id)  # Use the saved blog's ID
        else:
            messages.error(request, "There was an error creating the blog.")
    else:
        form = BlogForm()
    return render(request, 'userpanel/add_blog.html', {'form': form})

# Edit Blog
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect('userpanel:user_home')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully.")
            return redirect('userpanel:view_blog', blog_id=blog.id)
        else:
            messages.error(request, "There was an error updating the blog.")
    else:
        form = BlogForm(instance=blog)

    return render(request, 'userpanel/edit_blog.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        messages.error(request, "You are not authorized to delete this blog.")
        return redirect('userpanel:user_home')

    if request.method == 'POST':
        form = DeleteConfirmationForm(request.POST)
        if form.is_valid():
            blog.delete()
            messages.success(request, "Blog deleted successfully.")
            return redirect('userpanel:user_home')
    else:
        form = DeleteConfirmationForm()

    return render(request, 'userpanel/delete_blog.html', {'form': form, 'blog': blog})

def view_blog(request, blog_id):
    # Fetch the blog post using the provided blog_id
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Fetch comments for the blog, with status 'show'
    comments = Comment.objects.filter(blog=blog, status='show')
    
    comment_form = CommentForm()
    
    # Include the last updated timestamp in the context
    last_updated = blog.updated_at  

    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'last_updated': last_updated 
    }
    return render(request, 'userpanel/view_blog.html', context)

# Add Comment to Blog
@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.status = 'show'
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Failed to add comment.')
    return HttpResponseRedirect(reverse('userpanel:view_blog', args=[blog_id]))


# View My Blogs
@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user)
    context = {
        'blogs': blogs
    }
    return render(request, 'userpanel/my_blogs.html', context)

# List All Blogs (Published and Draft)
def blog_list(request):
    # Get published blogs and draft blogs
    published_blogs = Blog.objects.filter(status='published').order_by('-created_at')
    draft_blogs = Blog.objects.filter(status='draft').order_by('-created_at')
    
    context = {
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs
    }
    
    return render(request, 'userpanel/blog_list.html', context)

# Reset Password
@login_required
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('userpanel:user_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ResetPasswordForm(user=request.user)

    context = {'form': form}
    return render(request, 'userpanel/reset_password.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('userpanel:view_blog', blog_id=comment.blog.id)
        else:
            messages.error(request, 'Failed to update comment.')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'userpanel/comment_form.html', {'form': form, 'comment': comment})

# Delete Comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    blog_id = comment.blog.id
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('userpanel:view_blog', blog_id=blog_id)
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')
def blog_list(request):
    """List blogs visible to site visitors or users."""
    blogs = Blog.objects.filter(status='publish', is_visible=True, author__is_active=True)
    return render(request, 'userpanel/blog_list.html', {'blogs': blogs})

@login_required
def user_blog_list(request):
    """Display user's own published blogs."""
    blogs = Blog.objects.filter(author=request.user, status='publish')
    return render(request, 'userpanel/my_blogs.html', {'blogs': blogs})
