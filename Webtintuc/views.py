from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Category, Comment, Reaction, UserProfile, CategoryFollow, Notification
from .forms import RegisterForm, LoginForm, CommentForm, PostForm, ProfileForm
import os, uuid


# ==================== AUTO-CREATE PROFILE ====================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


# ==================== CONTEXT HELPER ====================
def get_base_context(request=None):
    ctx = {'categories': Category.objects.filter(category_type='news')}
    if request and request.user.is_authenticated:
        ctx['unread_count'] = Notification.objects.filter(user=request.user, is_read=False).count()
    return ctx


# ==================== AUTH VIEWS ====================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Tách họ và tên thành first_name / last_name
            full_name = form.cleaned_data.get('full_name', '').strip()
            parts = full_name.rsplit(' ', 1)
            if len(parts) == 2:
                user.first_name, user.last_name = parts[0], parts[1]
            else:
                user.first_name = full_name
            user.save()
            # Lưu thêm thông tin vào UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.birth_date = form.cleaned_data.get('birth_date')
            profile.gender = form.cleaned_data.get('gender')
            profile.save()
            login(request, user)
            return redirect('webtintuc:index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {**get_base_context(request), 'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'webtintuc:index'))
            form.add_error(None, 'Tên đăng nhập hoặc mật khẩu không đúng')
    else:
        form = LoginForm()
    return render(request, 'login.html', {**get_base_context(request), 'form': form})


def logout_view(request):
    logout(request)
    return redirect('webtintuc:index')


# ==================== MAIN VIEWS ====================
def index(request):
    featured_post = Post.objects.filter(status='published').order_by('-views_count').first()
    latest_posts = Post.objects.filter(status='published').order_by('-published_at')[:8]
    trending_posts = Post.objects.filter(status='published').order_by('-views_count')[:4]
    return render(request, 'trang_chu.html', {
        **get_base_context(request),
        'featured_post': featured_post,
        'latest_posts': latest_posts,
        'trending_posts': trending_posts,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.views_count += 1
    post.save(update_fields=['views_count'])

    related_posts = Post.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]
    comments = Comment.objects.filter(post=post, is_approved=True).order_by('created_at')

    # Reaction của user hiện tại
    user_reaction = None
    if request.user.is_authenticated:
        try:
            user_reaction = Reaction.objects.get(user=request.user, post=post).reaction_type
        except Reaction.DoesNotExist:
            pass

    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST' and 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                c = comment_form.save(commit=False)
                c.post = post
                c.user = request.user
                c.save()
                return redirect('webtintuc:post_detail', slug=post.slug)
        else:
            comment_form = CommentForm()

    return render(request, 'chi-tiet-tin.html', {
        **get_base_context(request),
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
        'user_reaction': user_reaction,
        'like_count': post.like_count(),
        'dislike_count': post.dislike_count(),
    })


def search_posts(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.filter(status='published', title__icontains=query).order_by('-published_at') if query else []
    return render(request, 'search_results.html', {**get_base_context(request), 'query': query, 'posts': posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_at')
    is_following = False
    if request.user.is_authenticated:
        is_following = CategoryFollow.objects.filter(user=request.user, category=category).exists()
    return render(request, 'category_news.html', {
        **get_base_context(request),
        'category': category,
        'posts': posts,
        'is_following': is_following,
    })


def category_news(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_at')
    data = [{'title': p.title, 'slug': p.slug, 'published_at': p.published_at.strftime('%Y-%m-%d %H:%M'), 'views_count': p.views_count} for p in posts]
    return JsonResponse({'posts': data})


def chinh_sach(request):
    return render(request, 'chinh_sach.html', get_base_context(request))

def quang_cao(request):
    return render(request, 'quang_cao.html', get_base_context(request))

def huong_dan(request):
    return render(request, 'huong_dan.html', get_base_context(request))

def faq(request):
    return render(request, 'faq.html', get_base_context(request))


# ==================== REACTION (LIKE/DISLIKE) ====================
@login_required(login_url='webtintuc:login')
def react_post(request, slug):
    """AJAX: Like hoặc Dislike bài viết"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    post = get_object_or_404(Post, slug=slug)
    reaction_type = request.POST.get('type')  # 'like' hoặc 'dislike'
    if reaction_type not in ('like', 'dislike'):
        return JsonResponse({'error': 'Invalid type'}, status=400)

    existing = Reaction.objects.filter(user=request.user, post=post).first()
    if existing:
        if existing.reaction_type == reaction_type:
            existing.delete()   # bấm lại → bỏ react
            user_reaction = None
        else:
            existing.reaction_type = reaction_type  # đổi từ like → dislike hoặc ngược lại
            existing.save()
            user_reaction = reaction_type
    else:
        Reaction.objects.create(user=request.user, post=post, reaction_type=reaction_type)
        user_reaction = reaction_type

    return JsonResponse({
        'like_count': post.like_count(),
        'dislike_count': post.dislike_count(),
        'user_reaction': user_reaction,
    })


# ==================== FOLLOW CATEGORY ====================
@login_required(login_url='webtintuc:login')
def follow_category(request, slug):
    """AJAX: Follow/Unfollow danh mục"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    category = get_object_or_404(Category, slug=slug)
    obj, created = CategoryFollow.objects.get_or_create(user=request.user, category=category)
    if not created:
        obj.delete()
        return JsonResponse({'following': False, 'message': f'Đã bỏ theo dõi "{category.name}"'})
    return JsonResponse({'following': True, 'message': f'Đang theo dõi "{category.name}"'})


# ==================== NOTIFICATIONS ====================
@login_required(login_url='webtintuc:login')
def notifications(request):
    """Trang xem tất cả thông báo"""
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    # Đánh dấu tất cả là đã đọc
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {**get_base_context(request), 'notifications': notifs})


@login_required(login_url='webtintuc:login')
def notifications_api(request):
    """AJAX polling: trả về số thông báo chưa đọc + 5 cái mới nhất"""
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    unread = Notification.objects.filter(user=request.user, is_read=False).count()
    data = [{'message': n.message, 'post_slug': n.post.slug if n.post else '', 'is_read': n.is_read, 'created_at': n.created_at.strftime('%d/%m %H:%M')} for n in notifs]
    return JsonResponse({'unread': unread, 'notifications': data})


# ==================== USER PROFILE ====================
def user_profile(request, username):
    """Trang thông tin công khai của một user"""
    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    comments = Comment.objects.filter(user=profile_user, is_approved=True).select_related('post').order_by('-created_at')[:20]
    follows = CategoryFollow.objects.filter(user=profile_user).select_related('category')
    return render(request, 'user_profile.html', {
        **get_base_context(request),
        'profile_user': profile_user,
        'profile': profile,
        'comments': comments,
        'follows': follows,
    })


@login_required(login_url='webtintuc:login')
def edit_profile(request):
    """Trang chỉnh sửa profile của chính mình"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('webtintuc:user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {**get_base_context(request), 'form': form})


# ==================== ADMIN-ONLY: CREATE/EDIT POST ====================
@login_required(login_url='webtintuc:login')
def create_post(request):
    if not request.user.is_staff:
        return redirect('webtintuc:index')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('webtintuc:my_posts')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {**get_base_context(request), 'form': form})


@login_required(login_url='webtintuc:login')
def edit_post(request, slug):
    if not request.user.is_staff:
        return redirect('webtintuc:index')
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('webtintuc:my_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'create_post.html', {**get_base_context(request), 'form': form, 'post': post})


@login_required(login_url='webtintuc:login')
def upload_image(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if request.method == 'POST' and request.FILES.get('file'):
        image = request.FILES['file']
        ext = os.path.splitext(image.name)[1].lower()
        filename = f"{uuid.uuid4().hex}{ext}"
        save_dir = os.path.join(settings.MEDIA_ROOT, 'content')
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, filename), 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        return JsonResponse({'location': f"{settings.MEDIA_URL}content/{filename}"})
    return JsonResponse({'error': 'Không có file'}, status=400)

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
    if not request.user.is_staff:
        return redirect('webtintuc:index')
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'my_posts.html', {**get_base_context(request), 'posts': posts})
