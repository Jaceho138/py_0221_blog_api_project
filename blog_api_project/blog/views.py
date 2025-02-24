from django.shortcuts import render  # 渲染模板 / Render templates
from django.contrib.auth.decorators import login_required  # 确保用户登录 / Ensure user is logged in
from rest_framework import viewsets, permissions  # 视图集和权限模块 / Viewsets and permissions modules
from .models import Post, Category  # 导入文章和分类模型 / Import Post and Category models
from .serializers import PostSerializer, CategorySerializer  # 导入序列化器 / Import serializers


@login_required  # 仅登录用户可访问 / Only logged-in users can access
def profile_view(request):
    """
    渲染当前登录用户的信息，使用 HTML 模板。
    Renders information about the current logged-in user using an HTML template.
    """
    user = request.user
    context = {
        'username': user.username,
        'email': user.email or 'Not provided',  # 如果没有邮箱，提供默认值 / Provide default if no email
        'date_joined': user.date_joined,
        'posts_count': user.posts.count(),  # 获取用户文章数量 / Get user’s post count
    }
    return render(request, 'profile.html', context)  # 渲染 profile.html 模板 / Render profile.html template


# 文章视图集 / Post viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]  # 只读或登录用户可写 / Read-only or authenticated users can write

    def perform_create(self, serializer):
        # 创建时自动设置当前用户 / Set current user on create
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # 只允许用户编辑自己的文章 / Allow users to edit only their own posts
        if self.request.user.is_authenticated:
            return Post.objects.filter(user=self.request.user)
        return Post.objects.all()

    @action(detail=False, methods=['get'])
    def search(self, request):
        # 搜索功能 / Search functionality
        keyword = request.query_params.get('keyword', '')
        posts = Post.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


# 分类视图集 / Category viewset
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]  # 只读或登录用户可写 / Read-only or authenticated users can write
