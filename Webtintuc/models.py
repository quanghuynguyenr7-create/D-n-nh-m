from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.utils.text import slugify
=======
>>>>>>> 2f11f31631ed977934cecef8646749be5bff50b9
from django.utils import timezone


class User(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Editor', 'Editor'),
        ('User', 'User'),
    ]
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'USER'

    def __str__(self):
        return self.username


class Category(models.Model):
<<<<<<< HEAD
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
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    
=======
    TYPE_CHOICES = [
        ('News', 'News'),
        ('Blog', 'Blog'),
    ]
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    category_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='News')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'CATEGORY'

>>>>>>> 2f11f31631ed977934cecef8646749be5bff50b9
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


<<<<<<< HEAD
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
=======
class Tag(models.Model):
    tag_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'TAG'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]
    TYPE_CHOICES = [
        ('News', 'News'),
        ('Blog', 'Blog'),
    ]
    post_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.CharField(max_length=500)
    content = models.TextField()
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    post_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='News')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, db_column='category_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_id')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='PostTag', blank=True)

    class Meta:
        db_table = 'POST'
>>>>>>> 2f11f31631ed977934cecef8646749be5bff50b9

    def __str__(self):
        return self.title


<<<<<<< HEAD

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
    
=======
class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tag_id')

    class Meta:
        db_table = 'POST_TAG'
        unique_together = ('post', 'tag')


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    content = models.TextField()
    parent_id = models.BigIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'COMMENT'

    def __str__(self):
        return f"Comment {self.comment_id} by {self.user}"


class Advertisement(models.Model):
    POSITION_CHOICES = [
        ('Sidebar', 'Sidebar'),
        ('Header_Banner', 'Header Banner'),
        ('Footer_Banner', 'Footer Banner'),
    ]
    ad_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    banner_url = models.CharField(max_length=255)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'ADVERTISEMENT'

>>>>>>> 2f11f31631ed977934cecef8646749be5bff50b9
    def __str__(self):
        return self.title
