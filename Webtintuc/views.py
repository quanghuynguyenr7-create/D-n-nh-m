from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Post, Category, Comment
from .forms import RegisterForm, LoginForm, CommentForm
from .forms import RegisterForm, LoginForm, CommentForm, PostForm 

# ==================== CONTEXT HELPER ====================

@login_required(login_url='webtintuc:login')
def create_post(request):
    """Tạo bài viết mới"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # request.FILES là bắt buộc để nhận ảnh
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('webtintuc:my_posts')
    else:
        form = PostForm()
    
    context = {
        **get_base_context(),
        'form': form,
    }
    return render(request, 'create_post.html', context)
def get_base_context():
    """Trả về context chung cho tất cả templates"""
    return {
        'categories': Category.objects.filter(category_type='news'),
    }


# ==================== AUTHENTICATION VIEWS ====================
def register_view(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('webtintuc:index')
    else:
        form = RegisterForm()
    
    context = {
        **get_base_context(),
        'form': form,
    }
    return render(request, 'register.html', context)


def login_view(request):
    """Đăng nhập"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'webtintuc:index'))
            else:
                form.add_error(None, 'Tên đăng nhập hoặc mật khẩu không đúng')
    else:
        form = LoginForm()
    
    context = {
        **get_base_context(),
        'form': form,
    }
    return render(request, 'login.html', context)


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    return redirect('webtintuc:index')


# ==================== MAIN VIEWS ====================
def index(request):
    """Trang chủ - Hiển thị bài nổi bật, mới nhất, trending"""
    # Bài viết nổi bật
    featured_posts = Post.objects.filter(
        status='published'
    ).order_by('-views_count')[:1]
    
    featured_post = featured_posts.first() if featured_posts else None

    # Bài mới nhất
    latest_posts = Post.objects.filter(
        status='published'
    ).order_by('-published_at')[:8]

    # Bài trending (top views)
    trending_posts = Post.objects.filter(
        status='published'
    ).order_by('-views_count')[:4]

    context = {
        **get_base_context(),
        'featured_post': featured_post,
        'latest_posts': latest_posts,
        'trending_posts': trending_posts,
    }
    return render(request, 'trang_chu.html', context)


def post_detail(request, slug):
    """Chi tiết bài viết"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Tăng lượt xem
    post.views_count += 1
    post.save(update_fields=['views_count'])

    # Bài viết cùng danh mục
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]

    # Bình luận
    comments = Comment.objects.filter(post=post, is_approved=True).order_by('-created_at')
    
    # Form bình luận
    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST' and 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('webtintuc:post_detail', slug=post.slug)
        else:
            comment_form = CommentForm()

    context = {
        **get_base_context(),
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'chi-tiet-tin.html', context)


def search_posts(request):
    """Tìm kiếm bài viết"""
    query = request.GET.get('q', '').strip()
    
    if query:
        posts = Post.objects.filter(
            status='published',
            title__icontains=query
        ).order_by('-published_at')
    else:
        posts = []

    context = {
        **get_base_context(),
        'query': query,
        'posts': posts,
    }
    return render(request, 'search_results.html', context)


def category_posts(request, slug):
    """Hiển thị bài theo danh mục"""
    category = get_object_or_404(Category, slug=slug, category_type='news')
    
    posts = Post.objects.filter(
        category=category,
        status='published'
    ).order_by('-published_at')

    context = {
        **get_base_context(),
        'category': category,
        'posts': posts,
    }
    return render(request, 'category_news.html', context)

def chinh_sach(request):
    """Trang chính sách"""
    context = {
        **get_base_context(),
    }
    return render(request, 'chinh_sach.html', context)
def quang_cao(request):
    """Trang quảng cáo"""
    context = {
        **get_base_context(),
    }
    return render(request, 'quang_cao.html', context)
def huong_dan(request):
    """Trang hướng dẫn"""
    context = {
        **get_base_context(),
    }
    return render(request, 'huong_dan.html', context)
def faq(request):
    """Trang FAQ"""
    context = {
        **get_base_context(),
    }
    return render(request, 'faq.html', context)
def category_news(request, slug):
    """Hiển thị bài viết theo danh mục (API)"""
    category = get_object_or_404(Category, slug=slug, category_type='news')
    
    posts = Post.objects.filter(
        category=category,
        status='published'
    ).order_by('-published_at')

    data = [
        {
            'title': post.title,
            'slug': post.slug,
            'published_at': post.published_at.strftime('%Y-%m-%d %H:%M'),
            'views_count': post.views_count,
        }
        for post in posts
    ]
    return JsonResponse({'posts': data})
@login_required(login_url='webtintuc:login')
def my_posts(request):
    """Bài viết của tôi"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        **get_base_context(),
        'posts': posts,
    }
    return render(request, 'my_posts.html', context)

