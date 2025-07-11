from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'tags', 'created_at', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['tags']
    inlines = [CommentInline]
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('內容', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('分類與標籤', {
            'fields': ('category', 'tags')
        }),
        ('時間資訊', {
            'fields': ('published_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建文章
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'已核准 {queryset.count()} 則評論')
    approve_comments.short_description = '核准選中的評論'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'已取消核准 {queryset.count()} 則評論')
    disapprove_comments.short_description = '取消核准選中的評論'
