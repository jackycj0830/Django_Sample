from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from blog.models import Category, Tag, Post, Comment
import random


class Command(BaseCommand):
    help = '建立部落格範例資料'

    def add_arguments(self, parser):
        parser.add_argument(
            '--posts',
            type=int,
            default=10,
            help='要建立的文章數量 (預設: 10)'
        )
        parser.add_argument(
            '--comments',
            type=int,
            default=20,
            help='要建立的評論數量 (預設: 20)'
        )

    def handle(self, *args, **options):
        self.stdout.write('開始建立範例資料...')
        
        # 建立使用者
        users = self.create_users()
        
        # 建立分類
        categories = self.create_categories()
        
        # 建立標籤
        tags = self.create_tags()
        
        # 建立文章
        posts = self.create_posts(users, categories, tags, options['posts'])
        
        # 建立評論
        self.create_comments(users, posts, options['comments'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f'成功建立範例資料：'
                f'{len(users)} 個使用者、'
                f'{len(categories)} 個分類、'
                f'{len(tags)} 個標籤、'
                f'{len(posts)} 篇文章、'
                f'{options["comments"]} 則評論'
            )
        )

    def create_users(self):
        """建立範例使用者"""
        users = []
        user_data = [
            ('admin', 'admin@example.com', '管理員', True),
            ('author1', 'author1@example.com', '作者一', False),
            ('author2', 'author2@example.com', '作者二', False),
            ('reader1', 'reader1@example.com', '讀者一', False),
            ('reader2', 'reader2@example.com', '讀者二', False),
        ]
        
        for username, email, first_name, is_staff in user_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'is_staff': is_staff,
                    'is_superuser': is_staff,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'建立使用者: {username}')
            users.append(user)
        
        return users

    def create_categories(self):
        """建立範例分類"""
        categories = []
        category_data = [
            ('Django 教學', 'Django 框架相關的教學文章'),
            ('Python 程式設計', 'Python 程式語言學習資源'),
            ('Web 開發', '網頁開發技術與工具'),
            ('資料庫設計', '資料庫設計與最佳化'),
            ('專案管理', '軟體專案管理經驗分享'),
        ]
        
        for name, description in category_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'建立分類: {name}')
            categories.append(category)
        
        return categories

    def create_tags(self):
        """建立範例標籤"""
        tags = []
        tag_names = [
            'Django', 'Python', 'Web開發', 'HTML', 'CSS', 'JavaScript',
            '資料庫', 'SQL', 'Bootstrap', '響應式設計', 'API', 'REST',
            '測試', '部署', 'Git', '版本控制', '最佳實踐', '教學'
        ]
        
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f'建立標籤: {name}')
            tags.append(tag)
        
        return tags

    def create_posts(self, users, categories, tags, count):
        """建立範例文章"""
        posts = []
        
        sample_posts = [
            {
                'title': 'Django 入門指南：建立你的第一個網站',
                'content': '''Django 是一個高級的 Python Web 框架，它鼓勵快速開發和乾淨、實用的設計。

## 什麼是 Django？

Django 是一個免費且開源的 Web 框架，使用 Python 編寫。它遵循模型-視圖-模板（MVT）架構模式，並且強調可重用性和"不要重複自己"（DRY）原則。

## 主要特色

1. **快速開發**: Django 提供了許多內建功能，讓開發者能夠快速建立 Web 應用程式
2. **安全性**: Django 內建了許多安全功能，幫助開發者避免常見的安全問題
3. **可擴展性**: Django 可以處理高流量的網站
4. **豐富的生態系統**: 有大量的第三方套件可以使用

## 開始使用 Django

首先，你需要安裝 Django：

```bash
pip install django
```

然後建立一個新的專案：

```bash
django-admin startproject myproject
```

這就是 Django 開發的第一步！''',
                'excerpt': 'Django 是一個強大的 Python Web 框架，本文將帶你了解 Django 的基本概念和如何開始使用。'
            },
            {
                'title': 'Python 資料結構完整指南',
                'content': '''Python 提供了多種內建的資料結構，每種都有其特定的用途和優勢。

## 列表 (List)

列表是 Python 中最常用的資料結構之一：

```python
my_list = [1, 2, 3, 4, 5]
my_list.append(6)  # 新增元素
print(my_list[0])  # 存取元素
```

## 字典 (Dictionary)

字典用於儲存鍵值對：

```python
my_dict = {'name': 'John', 'age': 30}
print(my_dict['name'])  # 輸出: John
```

## 集合 (Set)

集合用於儲存唯一的元素：

```python
my_set = {1, 2, 3, 3, 4}
print(my_set)  # 輸出: {1, 2, 3, 4}
```

## 元組 (Tuple)

元組是不可變的序列：

```python
my_tuple = (1, 2, 3)
# my_tuple[0] = 5  # 這會產生錯誤
```

選擇正確的資料結構對於程式的效能和可讀性非常重要。''',
                'excerpt': '深入了解 Python 的內建資料結構：列表、字典、集合和元組的使用方法和最佳實踐。'
            },
            {
                'title': '響應式網頁設計的核心概念',
                'content': '''響應式網頁設計（Responsive Web Design）是現代網頁開發的重要技能。

## 什麼是響應式設計？

響應式設計是一種網頁設計方法，讓網頁能夠在不同的裝置和螢幕尺寸上都能良好顯示。

## 核心技術

### 1. 彈性網格系統

使用相對單位而非固定像素：

```css
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

.column {
    width: 50%;
    float: left;
}
```

### 2. 彈性圖片

讓圖片能夠自動調整大小：

```css
img {
    max-width: 100%;
    height: auto;
}
```

### 3. 媒體查詢

針對不同螢幕尺寸套用不同的樣式：

```css
@media screen and (max-width: 768px) {
    .column {
        width: 100%;
    }
}
```

## Bootstrap 框架

Bootstrap 是一個流行的 CSS 框架，提供了完整的響應式網格系統和元件。

響應式設計不僅是技術要求，更是提升使用者體驗的關鍵。''',
                'excerpt': '學習響應式網頁設計的基本概念，包括彈性網格、媒體查詢和 Bootstrap 框架的使用。'
            }
        ]
        
        # 建立範例文章
        for i, post_data in enumerate(sample_posts):
            if i >= count:
                break
                
            author = random.choice(users[:3])  # 只讓前三個使用者當作者
            category = random.choice(categories)
            
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'slug': slugify(post_data['title']),
                    'author': author,
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'category': category,
                    'status': 'published',
                    'published_at': timezone.now(),
                }
            )
            
            if created:
                # 隨機新增標籤
                post_tags = random.sample(tags, random.randint(2, 5))
                post.tags.set(post_tags)
                self.stdout.write(f'建立文章: {post.title}')
                posts.append(post)
        
        # 如果需要更多文章，建立簡單的範例文章
        for i in range(len(sample_posts), count):
            title = f'範例文章 {i + 1}'
            content = f'''這是第 {i + 1} 篇範例文章的內容。

## 文章簡介

這篇文章展示了部落格系統的基本功能，包括：

- 文章發布
- 分類管理
- 標籤系統
- 評論功能

## 內容段落

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

### 子標題

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

這是一個完整的部落格範例專案，展示了 Django 的各種功能。'''
            
            author = random.choice(users[:3])
            category = random.choice(categories)
            
            post, created = Post.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'author': author,
                    'content': content,
                    'excerpt': f'這是第 {i + 1} 篇範例文章的摘要，展示部落格系統的基本功能。',
                    'category': category,
                    'status': 'published',
                    'published_at': timezone.now(),
                }
            )
            
            if created:
                # 隨機新增標籤
                post_tags = random.sample(tags, random.randint(1, 4))
                post.tags.set(post_tags)
                posts.append(post)
        
        return posts

    def create_comments(self, users, posts, count):
        """建立範例評論"""
        sample_comments = [
            '這篇文章寫得很好，對我很有幫助！',
            '感謝分享，學到了很多新知識。',
            '內容很詳細，適合初學者閱讀。',
            '希望能看到更多類似的教學文章。',
            '程式碼範例很實用，謝謝作者。',
            '這個主題很有趣，期待後續文章。',
            '解釋得很清楚，容易理解。',
            '實作部分很棒，跟著做了一遍。',
            '有沒有相關的進階教學？',
            '文章結構很好，邏輯清晰。',
        ]
        
        for i in range(count):
            post = random.choice(posts)
            author = random.choice(users)
            content = random.choice(sample_comments)
            
            Comment.objects.create(
                post=post,
                author=author,
                content=content,
                is_approved=True,
            )
