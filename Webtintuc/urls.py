from django.urls import path
from . import views

app_name = 'webtintuc'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('tin/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tim-kiem/', views.search_posts, name='search'),
    path('danh-muc/<slug:slug>/', views.category_posts, name='category'),
    path('bai-viet-cua-toi/', views.my_posts, name='my_posts'),
    
    # Authentication
    path('dang-ky/', views.register_view, name='register'),
    path('dang-nhap/', views.login_view, name='login'),
    path('dang-xuat/', views.logout_view, name='logout'),
]
