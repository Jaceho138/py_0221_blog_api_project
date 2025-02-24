from rest_framework import serializers
from .models import User, Category, Post


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Don't return password


# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# Post serializer
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Display user info
    category = CategorySerializer(read_only=True)  # Display category info
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),
                                                     source='category')  # For create/update

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'user', 'category', 'category_id']
