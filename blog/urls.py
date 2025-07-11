from django.urls import path
from . import views, api

app_name = 'blog'

urlpatterns = [
    # 首頁 - 文章列表
    path('', views.post_list, name='post_list'),

    # 文章詳細頁面
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # 分類頁面
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    # 標籤頁面
    path('tag/<int:pk>/', views.tag_detail, name='tag_detail'),

    # 關於頁面
    path('about/', views.about, name='about'),

    # API 文件
    path('api-docs/', views.api_docs, name='api_docs'),

    # 刪除評論
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # API 路由
    path('api/posts/', api.api_posts, name='api_posts'),
    path('api/posts/<slug:slug>/', api.api_post_detail, name='api_post_detail'),
    path('api/categories/', api.api_categories, name='api_categories'),
    path('api/tags/', api.api_tags, name='api_tags'),
    path('api/posts/<int:post_id>/comments/', api.api_create_comment, name='api_create_comment'),
    path('api/search/', api.api_search, name='api_search'),
    path('api/stats/', api.api_stats, name='api_stats'),
]
