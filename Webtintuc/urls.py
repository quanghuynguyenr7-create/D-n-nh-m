from django.urls import path
from . import views

app_name = 'webtintuc'

urlpatterns = [
    # Trang chủ
    path('', views.index, name='index'),
    
    # Chi tiết tin tức
    path('tin/<slug:slug>/', views.news_detail, name='news_detail'),
    
    # Tìm kiếm
    path('tim-kiem/', views.search_news, name='search'),
    
    # Danh mục
    path('danh-muc/<slug:slug>/', views.category_news, name='category'),
    
    # Tác giả
    path('tac-gia/<int:pk>/', views.author_news, name='author'),
    
    # API - Đăng ký newsletter
    path('api/subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # List view (tuỳ chọn)
    path('news-list/', views.NewsListView.as_view(), name='news_list'),
]
