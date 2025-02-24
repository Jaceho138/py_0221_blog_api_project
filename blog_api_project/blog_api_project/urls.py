from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import PostViewSet, CategoryViewSet, profile_view  # 导入 profile_view / Import profile_view

# 创建路由器 / Create router
router = DefaultRouter()
router.register(r'posts', PostViewSet)  # 注册文章 API / Register posts API
router.register(r'categories', CategoryViewSet)  # 注册分类 API / Register categories API

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # API 根路径 / API root path
    path('api-auth/', include('rest_framework.urls')),  # DRF 登录/登出 / DRF login/logout
    path('accounts/profile/', profile_view, name='profile'),  # 定义 profile 路由 / Define profile route
]
