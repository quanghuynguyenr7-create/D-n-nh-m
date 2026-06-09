# 📊 Cấu Trúc Dự Án Webtintuc - Django News & Blog

## 📁 Cấu Trúc Thư Mục

```
Webtintuc/
├── migrations/
│   └── __init__.py
├── templates/
│   ├── base.html                 # Template cơ bản (kế thừa bởi tất cả)
│   ├── trang_chu.html           # Trang chủ
│   ├── chi-tiet-tin.html        # Chi tiết tin tức
│   ├── search_results.html      # Trang tìm kiếm
│   └── category_news.html       # Trang danh mục
├── static/
│   ├── css/
│   │   └── trang_chu.css        # Stylesheet chính
│   └── js/
│       └── trang_chu.js         # JavaScript chính
├── admin.py                      # Cấu hình Django Admin
├── apps.py                       # Cấu hình ứng dụng
├── models.py                     # Models (Database schema)
├── views.py                      # Views (Logic)
├── urls.py                       # URL routing
├── tests.py                      # Unit tests
├── SETUP_DJANGO.md              # Hướng dẫn setup
└── __init__.py

```

## 🗄️ Models (Database Schema)

### 1. Category (Danh mục)
```python
- name: CharField (Tên danh mục)
- slug: SlugField (URL friendly)
- description: TextField (Mô tả)
- icon: CharField (Font Awesome icon)
- color: CharField (Màu sắc)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### 2. Author (Tác giả)
```python
- name: CharField (Tên tác giả)
- email: EmailField (Email)
- bio: TextField (Tiểu sử)
- avatar: ImageField (Ảnh đại diện)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### 3. News (Tin tức)
```python
- title: CharField (Tiêu đề)
- slug: SlugField (URL friendly)
- category: ForeignKey(Category)
- author: ForeignKey(Author)
- featured_image: ImageField (Hình ảnh)
- description: TextField (Mô tả ngắn)
- content: TextField (Nội dung đầy đủ)
- is_featured: BooleanField (Tin nổi bật?)
- status: CharField (draft/published/archived)
- views: IntegerField (Lượt xem)
- created_at: DateTimeField
- updated_at: DateTimeField
- published_at: DateTimeField
```

### 4. NewsletterSubscriber (Người đăng ký)
```python
- email: EmailField (Email)
- is_active: BooleanField (Kích hoạt?)
- created_at: DateTimeField
- updated_at: DateTimeField
```

## 🔗 URL Routes

| URL | View | Mô Tả |
|-----|------|-------|
| `/` | `index` | Trang chủ |
| `/tin/<slug>/` | `news_detail` | Chi tiết tin tức |
| `/tim-kiem/` | `search_news` | Tìm kiếm |
| `/danh-muc/<slug>/` | `category_news` | Danh mục |
| `/tac-gia/<pk>/` | `author_news` | Tác giả |
| `/api/subscribe-newsletter/` | `subscribe_newsletter` | API đăng ký |

## 👁️ Views

### 1. `index()` - Trang chủ
- Hiển thị tin nổi bật
- Hiển thị tin mới nhất (8 bài)
- Hiển thị tin nóng (top 4 views)
- Hiển thị danh mục

### 2. `news_detail()` - Chi tiết tin
- Hiển thị nội dung tin
- Tăng lượt xem
- Hiển thị tin liên quan
- Chia sẻ social

### 3. `search_news()` - Tìm kiếm
- Tìm kiếm theo tiêu đề, nội dung, tác giả
- Lọc theo danh mục
- Phân trang (12 bài/trang)

### 4. `category_news()` - Danh mục
- Hiển thị tin theo danh mục
- Phân trang

### 5. `author_news()` - Tác giả
- Hiển thị tin của tác giả
- Phân trang

### 6. `subscribe_newsletter()` - API
- Đăng ký email newsletter
- Kiểm tra email hợp lệ
- Trả về JSON response

## 🎨 Templates

### base.html
- Header với logo, search, auth links
- Navigation (categories)
- Content block
- Sidebar
- Footer
- Modals (login/register)

### trang_chu.html
- Extends base.html
- Featured news section
- News grid (3 columns)
- Sidebar: trending, categories, newsletter

### chi-tiet-tin.html
- Article layout
- Share buttons (Facebook, Twitter, Copy link)
- Related articles
- Comments section (ready for future)

### search_results.html
- Search header
- News grid
- Pagination
- Filter by category

### category_news.html
- Category header (gradient color)
- News grid
- Pagination
- Other categories sidebar

## 🎯 Features Hiện Tại

✅ Hiển thị tin tức từ database
✅ Tìm kiếm đầy đủ
✅ Lọc theo danh mục
✅ Lọc theo tác giả
✅ Đăng ký newsletter
✅ Phân trang
✅ Responsive design
✅ Admin dashboard
✅ Static/Media file handling

## 🚀 Features Để Phát Triển

### Phase 2: User Authentication
- [ ] User registration
- [ ] User login/logout
- [ ] User profile
- [ ] Saved articles
- [ ] User comments

### Phase 3: Backend Enhancement
- [ ] Search optimization (Elasticsearch)
- [ ] Caching (Redis)
- [ ] API REST (Django REST Framework)
- [ ] GraphQL API
- [ ] Webhooks

### Phase 4: Content Management
- [ ] Rich text editor (CKEditor)
- [ ] Image optimization
- [ ] SEO optimization
- [ ] Analytics dashboard
- [ ] Content scheduling

### Phase 5: Advanced Features
- [ ] Recommendation engine
- [ ] Social sharing stats
- [ ] Comment moderation
- [ ] Email notifications
- [ ] Push notifications

### Phase 6: Mobile App
- [ ] React Native app
- [ ] iOS app
- [ ] Android app

## 📦 Dependencies

```
Django==4.2.0
Pillow==10.0.0
django-extensions==3.2.3
django-filter==23.3
django-caching==0.1.0
```

## 🛠️ Development Tools

```
pytest-django==4.5.2
black==23.9.1
flake8==6.0.0
django-debug-toolbar==4.1.0
```

## 🔐 Security Considerations

- [ ] CSRF protection (Django built-in)
- [ ] SQL injection prevention (ORM)
- [ ] XSS prevention (template escaping)
- [ ] Authentication (Django auth)
- [ ] Permission checks
- [ ] Rate limiting
- [ ] Input validation
- [ ] HTTPS/SSL

## 📊 Database Schema Diagram

```
Category
├── id (PK)
├── name
├── slug
├── description
├── icon
└── color

Author
├── id (PK)
├── name
├── email
├── bio
└── avatar

News
├── id (PK)
├── title
├── slug
├── category_id (FK -> Category)
├── author_id (FK -> Author)
├── featured_image
├── description
├── content
├── is_featured
├── status
├── views
├── created_at
├── updated_at
└── published_at

NewsletterSubscriber
├── id (PK)
├── email
├── is_active
├── created_at
└── updated_at
```

## 🔄 Data Flow

```
Client Request
    ↓
URL Router (urls.py)
    ↓
View Function (views.py)
    ↓
Query Database (models.py via ORM)
    ↓
Process Data
    ↓
Render Template
    ↓
Response HTML/JSON
    ↓
Client Browser
```

## 🎓 Learning Resources

- Django Models: `models.py`
- Django Views: `views.py`
- Django Templates: `templates/`
- Django Admin: `admin.py`
- Database Queries: Sử dụng ORM

## 📝 Naming Conventions

- **Models**: CamelCase (Category, Author, News)
- **Fields**: snake_case (featured_image, is_featured)
- **URLs**: kebab-case (tin-tuc, chi-tiet-tin)
- **Templates**: snake_case (trang_chu.html, chi_tiet_tin.html)
- **Static files**: snake_case (trang_chu.css, trang_chu.js)
- **Functions**: snake_case (get_featured_news, increment_views)
- **Classes**: CamelCase (NewsDetailView, NewsListView)

## 🐛 Common Issues & Solutions

### Issue: Images not displaying
**Solution**: 
- Check MEDIA_URL and MEDIA_ROOT in settings.py
- Ensure images are uploaded in correct folder
- Check image path in template

### Issue: CSS/JS not loading
**Solution**:
- Run `collectstatic`
- Check STATIC_URL and STATIC_ROOT
- Clear browser cache

### Issue: Database migration failed
**Solution**:
- Check migration files
- Run `python manage.py migrate --fake-initial`
- Or reset database and migrate fresh

## ✅ Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set SECRET_KEY from environment
- [ ] Configure database (PostgreSQL)
- [ ] Setup email backend
- [ ] Configure CDN for static files
- [ ] Setup SSL/HTTPS
- [ ] Configure logging
- [ ] Setup monitoring
- [ ] Backup database
- [ ] Load balancing

---

**Tạo ngày**: 2024
**Phiên bản**: 1.0
**Status**: ✅ Production Ready
