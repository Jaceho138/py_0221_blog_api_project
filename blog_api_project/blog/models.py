from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# User model
class User(AbstractUser):
    # Specify unique related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='blog_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='blog_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )


# Category model
class Category(models.Model):
    name = models.CharField(max_length=50, null=False)  # Category name

    def __str__(self):
        return self.name


# Post model
class Post(models.Model):
    title = models.CharField(max_length=100, null=False)  # Title
    content = models.TextField(null=False)  # Content
    created_at = models.DateTimeField(default=timezone.now)  # Creation time
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # Author
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')  # Category

    def __str__(self):
        return self.title
