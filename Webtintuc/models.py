from django.db import models
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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title
