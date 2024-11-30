from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile model to store additional user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    id_proof = models.ImageField(upload_to='id_proofs/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

# Automatically create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Automatically save the Profile when the User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
# representing a blog post with fields for title, content, image, status, and visibility
class Blog(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blogs')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def is_accessible(self):
        """Check if the blog is accessible."""
        return self.status == 'publish' and self.is_visible and self.author.is_active


# Comment model to represent comments on blog posts
class Comment(models.Model):
    SHOW = 'show'
    HIDE = 'hide'
    STATUS_CHOICES = [
        (SHOW, 'Show'),
        (HIDE, 'Hide'),
    ]
    
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SHOW)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'


