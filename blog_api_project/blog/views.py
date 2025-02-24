from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer


# Post viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Read-only or authenticated users can write

    def perform_create(self, serializer):
        # Set current user on create
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Allow users to edit only their own posts
        if self.request.user.is_authenticated:
            return Post.objects.filter(user=self.request.user)
        return Post.objects.all()

    @action(detail=False, methods=['get'])
    def search(self, request):
        # Search functionality
        keyword = request.query_params.get('keyword', '')
        posts = Post.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

# Category viewset
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Read-only or authenticated users can write
