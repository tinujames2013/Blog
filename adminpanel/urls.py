from django.urls import path
from . import views


app_name = 'adminpanel'

urlpatterns = [
    path('home/', views.admin_home, name='admin_home'),
    path('user-list/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.view_user, name='view_user'),
    path('blog-list/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_view, name='blog_view'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('edit-blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('toggle_blog_visibility/<int:blog_id>/', views.toggle_blog_visibility, name='toggle_blog_visibility'),
    path('toggle-comment/<int:comment_id>/', views.toggle_comment_visibility, name='toggle_comment_visibility'),
    path('logout/', views.sign_out, name='sign_out'),
    path('change-password/', views.change_admin_password, name='change_admin_password'),
 
]
