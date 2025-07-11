from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
import json


@require_http_methods(["GET"])
def api_posts(request):
    """取得文章列表 API"""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    
    # 搜尋功能
    search = request.GET.get('search')
    if search:
        posts = posts.filter(title__icontains=search)
    
    # 分類篩選
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # 分頁
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    
    # 序列化資料
    posts_data = []
    for post in page_obj:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'excerpt': post.excerpt,
            'author': post.author.username,
            'category': post.category.name if post.category else None,
            'tags': [tag.name for tag in post.tags.all()],
            'created_at': post.created_at.isoformat(),
            'published_at': post.published_at.isoformat() if post.published_at else None,
            'url': post.get_absolute_url(),
        })
    
    return JsonResponse({
        'posts': posts_data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    })


@require_http_methods(["GET"])
def api_post_detail(request, slug):
    """取得文章詳細資料 API"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # 取得評論
    comments = post.comments.filter(is_approved=True).select_related('author')
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
        })
    
    # 序列化文章資料
    post_data = {
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content,
        'excerpt': post.excerpt,
        'author': {
            'username': post.author.username,
            'first_name': post.author.first_name,
        },
        'category': {
            'id': post.category.id,
            'name': post.category.name,
        } if post.category else None,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in post.tags.all()],
        'featured_image': post.featured_image.url if post.featured_image else None,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'published_at': post.published_at.isoformat() if post.published_at else None,
        'comments': comments_data,
        'comments_count': len(comments_data),
    }
    
    return JsonResponse({'post': post_data})


@require_http_methods(["GET"])
def api_categories(request):
    """取得分類列表 API"""
    categories = Category.objects.all()
    
    categories_data = []
    for category in categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'post_count': category.posts.filter(status='published').count(),
            'created_at': category.created_at.isoformat(),
        })
    
    return JsonResponse({'categories': categories_data})


@require_http_methods(["GET"])
def api_tags(request):
    """取得標籤列表 API"""
    tags = Tag.objects.all()
    
    tags_data = []
    for tag in tags:
        tags_data.append({
            'id': tag.id,
            'name': tag.name,
            'post_count': tag.posts.filter(status='published').count(),
            'created_at': tag.created_at.isoformat(),
        })
    
    return JsonResponse({'tags': tags_data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def api_create_comment(request, post_id):
    """建立評論 API"""
    try:
        post = get_object_or_404(Post, id=post_id, status='published')
        data = json.loads(request.body)
        
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({'error': '評論內容不能為空'}, status=400)
        
        if len(content) < 5:
            return JsonResponse({'error': '評論內容至少需要 5 個字元'}, status=400)
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            is_approved=True,  # 自動核准（實際應用中可能需要審核）
        )
        
        return JsonResponse({
            'comment': {
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
            },
            'message': '評論發表成功'
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '無效的 JSON 格式'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_search(request):
    """搜尋 API"""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'error': '搜尋關鍵字不能為空'}, status=400)
    
    # 搜尋文章
    posts = Post.objects.filter(
        status='published',
        title__icontains=query
    ).select_related('author', 'category')[:10]
    
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'excerpt': post.excerpt,
            'author': post.author.username,
            'category': post.category.name if post.category else None,
            'published_at': post.published_at.isoformat() if post.published_at else None,
            'url': post.get_absolute_url(),
        })
    
    # 搜尋分類
    categories = Category.objects.filter(name__icontains=query)[:5]
    categories_data = []
    for category in categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
        })
    
    # 搜尋標籤
    tags = Tag.objects.filter(name__icontains=query)[:10]
    tags_data = []
    for tag in tags:
        tags_data.append({
            'id': tag.id,
            'name': tag.name,
        })
    
    return JsonResponse({
        'query': query,
        'results': {
            'posts': posts_data,
            'categories': categories_data,
            'tags': tags_data,
        },
        'total_results': len(posts_data) + len(categories_data) + len(tags_data),
    })


@require_http_methods(["GET"])
def api_stats(request):
    """取得網站統計資料 API"""
    stats = {
        'total_posts': Post.objects.filter(status='published').count(),
        'total_categories': Category.objects.count(),
        'total_tags': Tag.objects.count(),
        'total_comments': Comment.objects.filter(is_approved=True).count(),
        'recent_posts': Post.objects.filter(status='published').count(),
    }
    
    # 最新文章
    recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:5]
    recent_posts_data = []
    for post in recent_posts:
        recent_posts_data.append({
            'title': post.title,
            'slug': post.slug,
            'published_at': post.published_at.isoformat() if post.published_at else None,
        })
    
    stats['recent_posts'] = recent_posts_data
    
    return JsonResponse({'stats': stats})
