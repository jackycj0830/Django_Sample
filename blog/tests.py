from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Category, Tag, Post, Comment


class BlogModelTests(TestCase):
    """部落格模型測試"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='測試分類',
            description='這是一個測試分類'
        )
        self.tag = Tag.objects.create(name='測試標籤')
        
    def test_category_creation(self):
        """測試分類建立"""
        self.assertEqual(self.category.name, '測試分類')
        self.assertEqual(str(self.category), '測試分類')
        
    def test_tag_creation(self):
        """測試標籤建立"""
        self.assertEqual(self.tag.name, '測試標籤')
        self.assertEqual(str(self.tag), '測試標籤')
        
    def test_post_creation(self):
        """測試文章建立"""
        post = Post.objects.create(
            title='測試文章',
            slug='test-post',
            author=self.user,
            content='這是測試文章內容',
            category=self.category,
            status='published'
        )
        post.tags.add(self.tag)
        
        self.assertEqual(post.title, '測試文章')
        self.assertEqual(str(post), '測試文章')
        self.assertTrue(post.is_published)
        self.assertIsNotNone(post.published_at)
        
    def test_comment_creation(self):
        """測試評論建立"""
        post = Post.objects.create(
            title='測試文章',
            slug='test-post',
            author=self.user,
            content='這是測試文章內容',
            status='published'
        )
        
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content='這是測試評論'
        )
        
        self.assertEqual(comment.content, '這是測試評論')
        self.assertTrue(comment.is_approved)


class BlogViewTests(TestCase):
    """部落格視圖測試"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='測試分類')
        self.post = Post.objects.create(
            title='測試文章',
            slug='test-post',
            author=self.user,
            content='這是測試文章內容',
            category=self.category,
            status='published'
        )
        
    def test_post_list_view(self):
        """測試文章列表頁面"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '測試文章')
        
    def test_post_detail_view(self):
        """測試文章詳細頁面"""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': 'test-post'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '測試文章')
        self.assertContains(response, '這是測試文章內容')
        
    def test_category_detail_view(self):
        """測試分類詳細頁面"""
        response = self.client.get(
            reverse('blog:category_detail', kwargs={'pk': self.category.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '測試分類')
        
    def test_about_view(self):
        """測試關於頁面"""
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)
