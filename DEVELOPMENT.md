# Django 部落格開發文件

本文件提供 Django 部落格專案的詳細技術說明，適合開發者深入了解專案架構和開發流程。

## 📋 目錄

- [專案架構](#專案架構)
- [資料模型設計](#資料模型設計)
- [視圖與 URL 設計](#視圖與-url-設計)
- [模板系統](#模板系統)
- [Django 核心概念](#django-核心概念)
- [開發最佳實踐](#開發最佳實踐)
- [API 設計](#api-設計)
- [測試策略](#測試策略)

## 🏗️ 專案架構

### MVC 架構模式

Django 採用 MTV (Model-Template-View) 架構模式：

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Model     │    │   Template  │    │    View     │
│  (資料層)    │    │  (展示層)    │    │  (邏輯層)    │
│             │    │             │    │             │
│ - 資料模型   │    │ - HTML 模板 │    │ - 業務邏輯   │
│ - 資料庫操作 │    │ - 模板標籤  │    │ - 請求處理   │
│ - 資料驗證   │    │ - 靜態檔案  │    │ - 回應生成   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 應用程式結構

```
blog/                          # Django 應用程式
├── models.py                  # 資料模型定義
├── views.py                   # 視圖邏輯
├── urls.py                    # URL 路由配置
├── admin.py                   # 管理後台配置
├── forms.py                   # 表單定義
├── tests.py                   # 測試程式碼
├── apps.py                    # 應用程式配置
├── templatetags/              # 自定義模板標籤
│   └── blog_extras.py
└── migrations/                # 資料庫遷移檔案
    └── 0001_initial.py
```

## 🗄️ 資料模型設計

### 實體關係圖 (ERD)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Category  │     │    Post     │     │     Tag     │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ id (PK)     │────▶│ id (PK)     │◀────│ id (PK)     │
│ name        │ 1:N │ title       │ M:N │ name        │
│ description │     │ slug        │     │ created_at  │
│ created_at  │     │ content     │     └─────────────┘
└─────────────┘     │ author (FK) │
                    │ category(FK)│
                    │ status      │
                    │ created_at  │
                    │ updated_at  │
                    │ published_at│
                    └─────────────┘
                           │
                           │ 1:N
                           ▼
                    ┌─────────────┐
                    │   Comment   │
                    ├─────────────┤
                    │ id (PK)     │
                    │ post (FK)   │
                    │ author (FK) │
                    │ content     │
                    │ created_at  │
                    │ is_approved │
                    └─────────────┘
```

### 模型詳細說明

#### Post 模型
```python
class Post(models.Model):
    title = models.CharField(max_length=200)           # 文章標題
    slug = models.SlugField(unique=True)               # URL 友善的別名
    author = models.ForeignKey(User)                   # 作者 (外鍵)
    content = models.TextField()                       # 文章內容
    excerpt = models.TextField(blank=True)             # 文章摘要
    category = models.ForeignKey(Category)             # 分類 (外鍵)
    tags = models.ManyToManyField(Tag)                 # 標籤 (多對多)
    status = models.CharField(choices=STATUS_CHOICES)  # 發布狀態
    featured_image = models.ImageField()               # 特色圖片
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True)
```

#### 關聯關係說明
- **一對多 (1:N)**: Category → Post, User → Post, Post → Comment
- **多對多 (M:N)**: Post ↔ Tag
- **外鍵約束**: 使用 `on_delete` 參數控制刪除行為

## 🎯 視圖與 URL 設計

### URL 路由架構

```
django_sample/urls.py (主 URL 配置)
├── admin/                     # Django Admin
├── ''                         # 根路徑，包含 blog.urls
└── blog/urls.py (應用程式 URL)
    ├── ''                     # 文章列表 (首頁)
    ├── post/<slug>/           # 文章詳細頁面
    ├── category/<int:pk>/     # 分類頁面
    ├── tag/<int:pk>/          # 標籤頁面
    ├── about/                 # 關於頁面
    └── comment/delete/<int>/  # 刪除評論
```

### 視圖類型與功能

#### 函數式視圖 (Function-Based Views)
```python
def post_list(request):
    """文章列表視圖 - 支援搜尋、篩選、分頁"""
    posts = Post.objects.filter(status='published')
    
    # 搜尋功能
    if search_query := request.GET.get('search'):
        posts = posts.filter(Q(title__icontains=search_query))
    
    # 分頁處理
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})
```

#### 視圖設計原則
1. **單一職責**: 每個視圖只處理一個主要功能
2. **DRY 原則**: 避免重複程式碼，使用繼承和 Mixin
3. **錯誤處理**: 使用 `get_object_or_404` 處理不存在的物件
4. **效能優化**: 使用 `select_related` 和 `prefetch_related`

## 🎨 模板系統

### 模板繼承結構

```
templates/
├── base.html                  # 基礎模板
└── blog/
    ├── post_list.html         # 繼承 base.html
    ├── post_detail.html       # 繼承 base.html
    ├── category_detail.html   # 繼承 base.html
    ├── tag_detail.html        # 繼承 base.html
    ├── about.html             # 繼承 base.html
    └── sidebar.html           # 包含模板
```

### 模板標籤與過濾器

#### 自定義模板標籤
```python
# blog/templatetags/blog_extras.py

@register.inclusion_tag('blog/recent_posts.html')
def get_recent_posts(count=5):
    """取得最新文章"""
    recent_posts = Post.objects.filter(status='published')[:count]
    return {'recent_posts': recent_posts}

@register.simple_tag
def get_categories():
    """取得所有分類"""
    return Category.objects.annotate(post_count=Count('posts'))

@register.filter
def wordcount(value):
    """計算字數"""
    return len(str(value).split())
```

#### 使用方式
```html
{% load blog_extras %}

<!-- 使用 inclusion_tag -->
{% get_recent_posts 5 %}

<!-- 使用 simple_tag -->
{% get_categories as categories %}

<!-- 使用 filter -->
{{ post.content|wordcount }} 字
```

### 模板最佳實踐

1. **模板繼承**: 使用 `{% extends %}` 避免重複 HTML
2. **區塊定義**: 合理使用 `{% block %}` 提供擴展點
3. **包含模板**: 使用 `{% include %}` 重用模板片段
4. **條件渲染**: 使用 `{% if %}` 控制內容顯示
5. **迴圈處理**: 使用 `{% for %}` 遍歷資料

## 🧠 Django 核心概念

### 1. 模型 (Models)

#### ORM 查詢
```python
# 基本查詢
posts = Post.objects.all()
post = Post.objects.get(id=1)
posts = Post.objects.filter(status='published')

# 複雜查詢
from django.db.models import Q, Count

# Q 物件查詢
posts = Post.objects.filter(
    Q(title__icontains='Django') | Q(content__icontains='Django')
)

# 聚合查詢
categories = Category.objects.annotate(
    post_count=Count('posts')
).filter(post_count__gt=0)

# 關聯查詢優化
posts = Post.objects.select_related('author', 'category').prefetch_related('tags')
```

#### 模型方法
```python
class Post(models.Model):
    # ... 欄位定義
    
    def get_absolute_url(self):
        """取得文章的絕對 URL"""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """覆寫 save 方法，自動設定發布時間"""
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        """檢查文章是否已發布"""
        return self.status == 'published'
```

### 2. 視圖 (Views)

#### 類別式視圖 (Class-Based Views)
```python
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
```

#### Mixin 使用
```python
class LoginRequiredMixin:
    """要求使用者登入的 Mixin"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
```

### 3. 表單 (Forms)

#### ModelForm
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '請輸入您的評論...',
            }),
        }
    
    def clean_content(self):
        """自定義驗證"""
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise forms.ValidationError('評論內容至少需要 10 個字元')
        return content
```

### 4. 管理後台 (Admin)

#### 自定義 Admin
```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('內容', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
    )
```

## 🚀 開發最佳實踐

### 1. 程式碼組織

#### 設定檔分離
```python
# settings/
├── __init__.py
├── base.py          # 基礎設定
├── development.py   # 開發環境
├── production.py    # 生產環境
└── testing.py       # 測試環境
```

#### 環境變數管理
```python
# 使用 python-decouple
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')
```

### 2. 資料庫最佳化

#### 查詢最佳化
```python
# 避免 N+1 查詢問題
posts = Post.objects.select_related('author', 'category').prefetch_related('tags')

# 使用 only() 和 defer() 控制欄位
posts = Post.objects.only('title', 'slug', 'created_at')

# 使用 exists() 檢查存在性
if Post.objects.filter(slug=slug).exists():
    # 處理邏輯
```

#### 索引設計
```python
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)  # 自動建立索引
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['category', 'created_at']),
        ]
```

### 3. 安全性考量

#### CSRF 保護
```html
<!-- 表單中必須包含 CSRF token -->
<form method="post">
    {% csrf_token %}
    <!-- 表單欄位 -->
</form>
```

#### XSS 防護
```html
<!-- Django 自動轉義 HTML -->
{{ user_input }}  <!-- 安全 -->
{{ user_input|safe }}  <!-- 不安全，需謹慎使用 -->
```

#### SQL 注入防護
```python
# 使用 ORM 查詢（安全）
Post.objects.filter(title__icontains=search_term)

# 避免原始 SQL（除非必要）
Post.objects.raw("SELECT * FROM blog_post WHERE title LIKE %s", [search_term])
```

### 4. 效能優化

#### 快取策略
```python
from django.core.cache import cache

def get_popular_posts():
    posts = cache.get('popular_posts')
    if posts is None:
        posts = Post.objects.filter(status='published')[:10]
        cache.set('popular_posts', posts, 3600)  # 快取 1 小時
    return posts
```

#### 分頁優化
```python
from django.core.paginator import Paginator

def post_list(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 10)  # 每頁 10 篇
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})
```

## 🧪 測試策略

### 測試類型

#### 單元測試
```python
class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content',
            status='published'
        )
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertTrue(self.post.is_published)
    
    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/test-post/')
```

#### 整合測試
```python
class PostViewTest(TestCase):
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
```

### 測試工具

#### Factory Boy
```python
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    
    title = factory.Faker('sentence', nb_words=4)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('text')
    status = 'published'
```

## 📚 進階主題

### 1. 自定義管理命令
```python
# management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from blog.models import Post, Category

class Command(BaseCommand):
    help = '建立範例資料'
    
    def handle(self, *args, **options):
        # 建立範例資料的邏輯
        self.stdout.write(self.style.SUCCESS('範例資料建立完成'))
```

### 2. 信號 (Signals)
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def post_published(sender, instance, created, **kwargs):
    if instance.status == 'published' and not created:
        # 發送通知或執行其他操作
        pass
```

### 3. 中介軟體 (Middleware)
```python
class BlogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 請求處理前的邏輯
        response = self.get_response(request)
        # 回應處理後的邏輯
        return response
```

---

這份開發文件涵蓋了 Django 部落格專案的核心技術概念和最佳實踐。建議開發者根據專案需求逐步深入學習各個主題。
