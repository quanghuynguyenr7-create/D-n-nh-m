from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


# ==================== CATEGORY MODEL ====================
class Category(models.Model):
    """Danh mục tin tức hoặc blog"""
    CATEGORY_TYPES = (
        ('news', 'Tin Tức'),
        ('blog', 'Blog'),
    )
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPES,
        default='news'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==================== TAG MODEL ====================
class Tag(models.Model):
    """Thẻ từ khóa gắn với bài viết"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==================== POST MODEL ====================
class Post(models.Model):
    """Bài viết (tin tức hoặc blog)"""
    STATUS_CHOICES = (
        ('draft', 'Nháp'),
        ('published', 'Đã đăng'),
    )
    POST_TYPES = (
        ('news', 'Tin Tức'),
        ('blog', 'Blog'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    summary = models.TextField(help_text="Tóm tắt ngắn gọn bài viết")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    views_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES,
        default='news'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Bài Viết"
        verbose_name_plural = "Bài Viết"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


# ==================== COMMENT MODEL ====================
class Comment(models.Model):
    """Bình luận trên bài viết"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bình Luận"
        verbose_name_plural = "Bình Luận"

    def __str__(self):
        return f"Bình luận của {self.user.username} trên {self.post.title}"


# ==================== ADVERTISEMENT MODEL ====================
class Advertisement(models.Model):
    """Quảng cáo / Banner"""
    POSITION_CHOICES = (
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
    )
    
    title = models.CharField(max_length=100)
    banner_url = models.URLField()
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

