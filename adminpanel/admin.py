from django.contrib import admin
from .models import Profile, Blog, Comment

# Register Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')  # Fields to display in the admin list view
    search_fields = ('user__username', 'phone')  # Enable searching by username and phone
    list_filter = ('user',)

# Register Blog model
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')  # Fields to display
    search_fields = ('title', 'author__username')  # Search by title and author username
    list_filter = ('status', 'created_at', 'author')  # Filters for status and author
    prepopulated_fields = {'title': ('title',)}  # Automatically populate slug from title

# Register Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'blog', 'status', 'created_at')  # Fields to display
    search_fields = ('comment', 'user__username', 'blog__title')  # Search by comment, user, and blog title
    list_filter = ('status', 'created_at')  # Filters for status and creation date


