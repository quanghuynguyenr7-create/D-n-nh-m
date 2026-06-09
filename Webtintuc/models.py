from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# ==================== CATEGORY MODEL ====================
class Category(models.Model):
    """Danh mục tin tức"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Tên danh mục"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="URL slug",
        help_text="Sẽ được tạo tự động từ tên"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Mô tả"
    )
    icon = models.CharField(
        max_length=50,
        default="fas fa-newspaper",
        verbose_name="Icon (Font Awesome class)"
    )
    color = models.CharField(
        max_length=7,
        default="#667eea",
        verbose_name="Màu sắc"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==================== AUTHOR MODEL ====================
class Author(models.Model):
    """Tác giả bài viết"""
    name = models.CharField(
        max_length=100,
        verbose_name="Tên tác giả"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Tiểu sử"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Ảnh đại diện"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Tác giả"
        verbose_name_plural = "Tác giả"
        ordering = ['name']

    def __str__(self):
        return self.name


# ==================== NEWS MODEL ====================
class News(models.Model):
    """Tin tức / Bài viết"""
    STATUS_CHOICES = (
        ('draft', 'Bản nháp'),
        ('published', 'Đã xuất bản'),
        ('archived', 'Đã lưu trữ'),
    )

    title = models.CharField(
        max_length=250,
        verbose_name="Tiêu đề"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="URL slug",
        help_text="Sẽ được tạo tự động từ tiêu đề"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_items',
        verbose_name="Danh mục"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_articles',
        verbose_name="Tác giả"
    )
    featured_image = models.ImageField(
        upload_to='news_images/',
        verbose_name="Hình ảnh nổi bật"
    )
    description = models.TextField(
        verbose_name="Mô tả ngắn",
        help_text="Mô tả ngắn gọn về bài viết (khoảng 200 từ)"
    )
    content = models.TextField(
        verbose_name="Nội dung bài viết"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Tin nổi bật"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Trạng thái"
    )
    views = models.IntegerField(
        default=0,
        verbose_name="Lượt xem"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Ngày xuất bản"
    )

    class Meta:
        verbose_name = "Tin tức"
        verbose_name_plural = "Tin tức"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['is_featured', '-published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def increment_views(self):
        """Tăng lượt xem"""
        self.views += 1
        self.save(update_fields=['views'])

    def get_related_news(self, limit=5):
        """Lấy các tin tức liên quan"""
        return News.objects.filter(
            category=self.category,
            status='published'
        ).exclude(id=self.id)[:limit]

    @property
    def time_since_published(self):
        """Thời gian từ lúc xuất bản"""
        if self.published_at:
            from django.utils.timesince import timesince
            return f"{timesince(self.published_at)} trước"
        return "Chưa xuất bản"


# ==================== NEWSLETTER MODEL ====================
class NewsletterSubscriber(models.Model):
    """Người đăng ký nhận tin tức"""
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Đã kích hoạt"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày đăng ký"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Người đăng ký"
        verbose_name_plural = "Người đăng ký"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
