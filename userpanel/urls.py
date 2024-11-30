from django.urls import path
from . import views

app_name = 'userpanel' 

urlpatterns = [
    path('user-home/', views.user_home, name='user_home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('add-blog/', views.add_blog, name='add_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('view-blog/<int:blog_id>/', views.view_blog, name='view_blog'),
    path('blog/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('blog-list/', views.blog_list, name='blog_list'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
]
