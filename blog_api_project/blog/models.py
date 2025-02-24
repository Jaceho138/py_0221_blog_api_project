from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# 用户模型 / User model
class User(AbstractUser):
    pass


# 分类模型 / Category model
class Category(models.Model):
    name = models.CharField(max_length=50, null=False)  # 分类名称 / Category name

    def __str__(self):
        return self.name


# 文章模型 / Post model
class Post(models.Model):
    title = models.CharField(max_length=100, null=False)  # 标题 / Title
    content = models.TextField(null=False)  # 内容 / Content
    created_at = models.DateTimeField(default=timezone.now)  # 创建时间 / Creation time
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # 作者 / Author
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')  # 分类 / Category

    def __str__(self):
        return self.title
