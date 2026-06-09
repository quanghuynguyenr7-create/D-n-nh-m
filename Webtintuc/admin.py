from django.contrib import admin
from .models import Category, Author, News, NewsletterSubscriber


# ==================== CATEGORY ADMIN ====================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Giao diện', {
            'fields': ('icon', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ==================== AUTHOR ADMIN ====================
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email', 'bio')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Thông tin tác giả', {
            'fields': ('name', 'email', 'bio')
        }),
        ('Ảnh đại diện', {
            'fields': ('avatar',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ==================== NEWS ADMIN ====================
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'views', 'published_at')
    list_filter = ('status', 'category', 'is_featured', 'published_at', 'created_at')
    search_fields = ('title', 'description', 'content', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'views', 'published_at')
    date_hierarchy = 'published_at'

    fieldsets = (
        ('Thông tin bài viết', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Nội dung', {
            'fields': ('description', 'content', 'featured_image')
        }),
        ('Hiển thị', {
            'fields': ('is_featured', 'status')
        }),
        ('Thống kê', {
            'fields': ('views', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_published', 'make_draft', 'make_featured']

    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} bài viết đã được xuất bản')
    make_published.short_description = "Xuất bản các bài viết được chọn"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} bài viết đã được đưa về bản nháp')
    make_draft.short_description = "Đưa về bản nháp các bài viết được chọn"

    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} bài viết đã được đánh dấu nổi bật')
    make_featured.short_description = "Đánh dấu nổi bật các bài viết được chọn"


# ==================== NEWSLETTER SUBSCRIBER ADMIN ====================
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Email', {
            'fields': ('email',)
        }),
        ('Trạng thái', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_subscribers', 'deactivate_subscribers']

    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} người đăng ký đã được kích hoạt')
    activate_subscribers.short_description = "Kích hoạt những người đăng ký được chọn"

    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} người đăng ký đã bị vô hiệu hóa')
    deactivate_subscribers.short_description = "Vô hiệu hóa những người đăng ký được chọn"

