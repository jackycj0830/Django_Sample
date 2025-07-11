from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import CommentForm


def post_list(request):
    """文章列表頁面"""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    
    # 搜尋功能
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # 分類篩選
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # 標籤篩選
    tag_id = request.GET.get('tag')
    if tag_id:
        posts = posts.filter(tags__id=tag_id)
    
    # 分頁
    paginator = Paginator(posts, 5)  # 每頁顯示 5 篇文章
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 取得所有分類和標籤供篩選使用
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'current_category': category_id,
        'current_tag': tag_id,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """文章詳細頁面"""
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(is_approved=True).select_related('author')
    
    # 處理評論表單
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, '評論已成功提交！')
                return redirect('blog:post_detail', slug=slug)
        else:
            messages.error(request, '請先登入才能發表評論。')
            return redirect('blog:post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    # 相關文章（同分類的其他文章）
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, pk):
    """分類詳細頁面"""
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(
        category=category, 
        status='published'
    ).select_related('author')
    
    # 分頁
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, pk):
    """標籤詳細頁面"""
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(
        tags=tag, 
        status='published'
    ).select_related('author')
    
    # 分頁
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_detail.html', context)


def about(request):
    """關於頁面"""
    return render(request, 'blog/about.html')


def api_docs(request):
    """API 文件頁面"""
    return render(request, 'blog/api_docs.html')


@login_required
def delete_comment(request, comment_id):
    """刪除評論（僅限評論作者或管理員）"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.author or request.user.is_staff:
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, '評論已刪除。')
        return redirect('blog:post_detail', slug=post_slug)
    else:
        messages.error(request, '您沒有權限刪除此評論。')
        return redirect('blog:post_detail', slug=comment.post.slug)
