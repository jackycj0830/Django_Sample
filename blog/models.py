from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """文章分類模型"""
    name = models.CharField('分類名稱', max_length=100, unique=True)
    description = models.TextField('分類描述', blank=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '分類'
        verbose_name_plural = '分類'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'pk': self.pk})


class Tag(models.Model):
    """文章標籤模型"""
    name = models.CharField('標籤名稱', max_length=50, unique=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '標籤'
        verbose_name_plural = '標籤'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """部落格文章模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已發布'),
    ]

    title = models.CharField('標題', max_length=200)
    slug = models.SlugField('網址別名', max_length=200, unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
        verbose_name='作者'
    )
    content = models.TextField('內容')
    excerpt = models.TextField('摘要', max_length=300, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='posts',
        verbose_name='分類'
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        related_name='posts',
        verbose_name='標籤'
    )
    status = models.CharField(
        '狀態', 
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    featured_image = models.ImageField(
        '特色圖片', 
        upload_to='blog/images/', 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)
    published_at = models.DateTimeField('發布時間', blank=True, null=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == 'published'


class Comment(models.Model):
    """文章評論模型"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='文章'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='作者'
    )
    content = models.TextField('評論內容')
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    is_approved = models.BooleanField('已核准', default=True)

    class Meta:
        verbose_name = '評論'
        verbose_name_plural = '評論'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} 對 "{self.post.title}" 的評論'
