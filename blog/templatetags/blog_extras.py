from django import template
from django.db.models import Count
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/recent_posts.html')
def get_recent_posts(count=5):
    """取得最新文章"""
    recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:count]
    return {'recent_posts': recent_posts}


@register.simple_tag
def get_categories():
    """取得所有分類"""
    return Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)


@register.simple_tag
def get_popular_tags(count=10):
    """取得熱門標籤"""
    return Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:count]


@register.filter
def wordcount(value):
    """計算字數"""
    return len(str(value).split())


@register.simple_tag
def get_archive_dates():
    """取得文章歸檔日期"""
    from django.db.models import DateTimeField
    from django.db.models.functions import TruncMonth
    
    dates = Post.objects.filter(status='published').annotate(
        month=TruncMonth('published_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')
    
    return dates[:12]  # 最近12個月
