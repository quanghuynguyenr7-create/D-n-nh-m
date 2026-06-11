from django.urls import path
from . import views

app_name = 'webtintuc'

urlpatterns = [
    path('', views.index, name='index'),
    path('tin/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tim-kiem/', views.search_posts, name='search'),
    path('danh-muc/<slug:slug>/', views.category_posts, name='category'),
    path('category/<slug:slug>/posts/', views.category_news, name='category_news'),

    # Reaction
    path('tin/<slug:slug>/react/', views.react_post, name='react_post'),

    # Follow category
    path('danh-muc/<slug:slug>/follow/', views.follow_category, name='follow_category'),

    # Notifications
    path('thong-bao/', views.notifications, name='notifications'),
    path('api/thong-bao/', views.notifications_api, name='notifications_api'),

    # Profile
    path('nguoi-dung/<str:username>/', views.user_profile, name='user_profile'),
    path('chinh-sua-profile/', views.edit_profile, name='edit_profile'),

    # Admin: posts
    path('tao-bai-viet/', views.create_post, name='create_post'),
    path('chinh-sua/<slug:slug>/', views.edit_post, name='edit_post'),
    path('upload-anh/', views.upload_image, name='upload_image'),
    path('bai-viet-cua-toi/', views.my_posts, name='my_posts'),

    # Auth
    path('dang-ky/', views.register_view, name='register'),
    path('dang-nhap/', views.login_view, name='login'),
    path('dang-xuat/', views.logout_view, name='logout'),
    path('chinh-sach/', views.chinh_sach, name='chinh_sach'),
    path('quang-cao/', views.quang_cao, name='quang_cao'),
    path('huong-dan/', views.huong_dan, name='huong_dan'),
    path('faq/', views.faq, name='faq'),
]
