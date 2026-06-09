from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import News, Category, Author, NewsletterSubscriber


# ==================== HOME VIEW ====================
def index(request):
    """Trang chủ - Hiển thị tin nổi bật và tin mới nhất"""
    # Tin nổi bật
    featured_news = News.objects.filter(
        is_featured=True,
        status='published'
    ).order_by('-published_at').first()

    # Tin mới nhất
    latest_news = News.objects.filter(
        status='published'
    ).order_by('-published_at')[:8]

    # Tin nóng (top trending)
    trending_news = News.objects.filter(
        status='published'
    ).order_by('-views')[:4]

    # Danh mục
    categories = Category.objects.all()

    context = {
        'featured_news': featured_news,
        'latest_news': latest_news,
        'trending_news': trending_news,
        'categories': categories,
    }
    return render(request, 'trang_chu.html', context)


# ==================== NEWS DETAIL VIEW ====================
def news_detail(request, slug):
    """Trang chi tiết tin tức"""
    news = get_object_or_404(News, slug=slug, status='published')
    
    # Tăng lượt xem
    news.increment_views()

    # Tin tức liên quan
    related_news = news.get_related_news(limit=4)

    # Tin cùng danh mục
    same_category = News.objects.filter(
        category=news.category,
        status='published'
    ).exclude(id=news.id)[:3]

    context = {
        'news': news,
        'related_news': related_news,
        'same_category': same_category,
        'categories': Category.objects.all(),
    }
    return render(request, 'chi-tiet-tin.html', context)


# ==================== SEARCH VIEW ====================
def search_news(request):
    """Tìm kiếm tin tức"""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')

    # Base queryset
    news_list = News.objects.filter(status='published')

    # Tìm kiếm
    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query) |
            Q(author__name__icontains=query)
        )

    # Lọc theo danh mục
    if category:
        news_list = news_list.filter(category__slug=category)

    # Sắp xếp
    news_list = news_list.order_by('-published_at')

    # Phân trang
    paginator = Paginator(news_list, 12)  # 12 tin mỗi trang
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'query': query,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'search_results.html', context)


# ==================== CATEGORY VIEW ====================
def category_news(request, slug):
    """Hiển thị tin tức theo danh mục"""
    category = get_object_or_404(Category, slug=slug)
    
    news_list = News.objects.filter(
        category=category,
        status='published'
    ).order_by('-published_at')

    # Phân trang
    paginator = Paginator(news_list, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'category_news.html', context)


# ==================== AUTHOR VIEW ====================
def author_news(request, pk):
    """Hiển thị tin tức theo tác giả"""
    author = get_object_or_404(Author, pk=pk)
    
    news_list = author.news_articles.filter(
        status='published'
    ).order_by('-published_at')

    # Phân trang
    paginator = Paginator(news_list, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'author': author,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'author_news.html', context)


# ==================== NEWSLETTER API ====================
@require_POST
def subscribe_newsletter(request):
    """API để đăng ký nhận tin (AJAX)"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email không được để trống'
            }, status=400)

        # Kiểm tra email hợp lệ
        from django.core.validators import validate_email
        try:
            validate_email(email)
        except:
            return JsonResponse({
                'success': False,
                'message': 'Email không hợp lệ'
            }, status=400)

        # Kiểm tra đã đăng ký chưa
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )

        if created:
            message = f'Cảm ơn! Bạn đã đăng ký nhận tin tức từ TinTức.News'
        else:
            if subscriber.is_active:
                message = 'Email này đã được đăng ký trước đó'
            else:
                subscriber.is_active = True
                subscriber.save()
                message = 'Bạn đã được kích hoạt lại'

        return JsonResponse({
            'success': True,
            'message': message
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu không hợp lệ'
        }, status=400)


# ==================== NEWS LIST CLASS VIEW ====================
class NewsListView(ListView):
    """Class-based view để liệt kê tin tức (có thể mở rộng)"""
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 12

    def get_queryset(self):
        return News.objects.filter(
            status='published'
        ).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# ==================== NEWS DETAIL CLASS VIEW ====================
class NewsDetailView(DetailView):
    """Class-based view cho chi tiết tin tức"""
    model = News
    template_name = 'chi-tiet-tin.html'
    slug_field = 'slug'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        
        # Tăng lượt xem
        news.increment_views()
        
        context['related_news'] = news.get_related_news()
        context['categories'] = Category.objects.all()
        return context
