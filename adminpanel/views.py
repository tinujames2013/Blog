from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Blog, Comment,Profile, User
from .forms import AdminLoginForm, AdminPasswordChangeForm, BlogForm

# Helper to ensure the user is staff
def is_admin(user):
    return user.is_staff

# Admin Login
def admin_login(request):
    """Admin login view."""
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            messages.error(request, 'Invalid credentials or not an admin user.')
    else:
        form = AdminLoginForm()
    return render(request, 'adminpanel/login.html', {'form': form})

# Admin Logout
def admin_logout(request):
    """Admin logout view."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('admin_home')

# Admin Dashboard
@login_required
@user_passes_test(is_admin)
def admin_home(request):
    """Admin dashboard."""
    # Fetch all users and assign status labels
    users = User.objects.all()
    for user in users:
        user.status_label = "Active" if user.is_active else "Deactivated"

    # Fetch all blogs and comments
    blogs = Blog.objects.all()
    comments = Comment.objects.all()

    # Render the dashboard with all the required data
    return render(request, 'adminpanel/admin_home.html', {
        'users': users,
        'blogs': blogs,
        'comments': comments,
    })

# Toggle User Active Status
@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_user_status(request, user_id):
    """Toggle user active status and hide blogs of deactivated users."""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    if not user.is_active:
        # Set all blogs by this user to 'draft'
        Blog.objects.filter(author=user).update(status='draft')

    messages.success(request, f"User {'activated' if user.is_active else 'deactivated'} successfully!")
    return redirect('adminpanel:admin_home')

@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_blog_visibility(request, blog_id):
    """Toggle blog visibility."""
    blog = get_object_or_404(Blog, id=blog_id)
    blog.status = 'draft' if blog.status == 'publish' else 'publish'
    blog.save()

    messages.success(request, f"Blog visibility updated to {blog.status}.")
    return redirect('adminpanel:admin_home')

# Toggle Comment Visibility
@login_required
@user_passes_test(is_admin)
def toggle_comment_visibility(request, comment_id):
    """Show or hide a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = 'hide' if comment.status == 'show' else 'show'
    comment.save()
    messages.success(request, f"Comment visibility updated to {comment.status}.")
    return redirect('adminpanel:admin_home')

# View Blog Details
@login_required
@user_passes_test(is_admin)
def blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Fetch the blog post by ID
    context = {
        'blog': blog,
    }
    return render(request, 'adminpanel/blog_view.html', context)

# Edit Blog
@login_required
@user_passes_test(is_admin)
def edit_blog(request, blog_id):
    """Edit a blog post."""
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('adminpanel:admin_home')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'adminpanel/blog_view.html', {'form': form, 'blog': blog})

# Delete Blog
@login_required
@user_passes_test(is_admin)
def delete_blog(request, blog_id):
    """Delete a blog post."""
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, 'Blog post deleted successfully.')
    return redirect('adminpanel:admin_home')

# User List
@login_required
@user_passes_test(is_admin)
def user_list(request):
    """View list of users."""
    users = User.objects.all()
    return render(request, 'adminpanel/user_list.html', {'users': users})

# View User Details
@login_required
@user_passes_test(is_admin)
def view_user(request, user_id):
    """View user details."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'adminpanel/view_user.html', {'user': user})
# Change Admin Password
@login_required
@user_passes_test(is_admin)
def change_admin_password(request):
    """Change the admin's password."""
    if request.method == 'POST':
        form = AdminPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep session active
            messages.success(request, 'Password updated successfully!')
            return redirect('adminpanel:admin_home')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminPasswordChangeForm(request.user)
    return render(request, 'adminpanel/change_password.html', {'form': form})
@login_required
def blog_list(request):
    blogs = Blog.objects.filter(status='publish', author__is_active=True)
    blogs = Blog.objects.all()  # Fetch all blog posts
    context = {
        'blogs': blogs,
    }
    return render(request, 'adminpanel/blog_list.html', context)
def reset_password(request):
    return render(request, 'adminpanel/reset_password.html')
def sign_out(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')
@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_user_status(request, user_id):
    """Activate or deactivate a user. Hide their blogs if deactivated."""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    if not user.is_active:
        # Hide all blogs by the deactivated user
        Blog.objects.filter(author=user).update(is_visible=False)
    messages.success(request, f"User {'activated' if user.is_active else 'deactivated'} successfully!")
    return redirect('adminpanel:admin_home')


