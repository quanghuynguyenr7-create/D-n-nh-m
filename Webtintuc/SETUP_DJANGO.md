# 📚 Hướng Dẫn Setup Django cho Webtintuc

## 🚀 Bước 1: Cài đặt Dependencies

```bash
pip install django pillow django-extensions
```

## 🛠️ Bước 2: Cấu hình Settings.py

Thêm vào `settings.py` của dự án Django:

```python
# INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'Webtintuc.apps.WebtintucConfig',  # Thêm dòng này
]

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'Webtintuc' / 'templates',  # Thêm đường dẫn templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'Webtintuc' / 'static',  # Thêm đường dẫn static
]

# MEDIA FILES (cho hình ảnh)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Internationalization
LANGUAGE_CODE = 'vi-vn'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Django Admin
ADMIN_URL = 'admin/'
```

## 📝 Bước 3: Cấu hình URLs.py

Thêm vào `urls.py` của dự án chính:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Webtintuc.urls')),  # Thêm dòng này
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## 🗄️ Bước 4: Tạo Migration

```bash
python manage.py makemigrations Webtintuc
python manage.py migrate
```

## 👤 Bước 5: Tạo Superuser

```bash
python manage.py createsuperuser
```

Nhập thông tin:
- Username: `admin`
- Email: `admin@example.com`
- Password: `your_password`

## 🌐 Bước 6: Chạy Server

```bash
python manage.py runserver
```

Truy cập:
- Trang chủ: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`

## 📋 Bước 7: Thêm Dữ Liệu Mẫu

1. Vào Admin: `http://localhost:8000/admin/`
2. Đăng nhập bằng superuser
3. Tạo Categories (Danh mục)
4. Tạo Authors (Tác giả)
5. Tạo News (Tin tức)

### Ví dụ Danh Mục:
- Công Nghệ (Technology)
- AI & Machine Learning
- Fintech
- Chứng Khoán (Stock Market)
- Tài Chính (Finance)
- Startups
- Blog

### Ví dụ Tác Giả:
- Nguyễn Bảo (nguyenbao@example.com)
- Lê Minh (leminh@example.com)
- Đỗ Anh (doanh@example.com)

### Ví dụ Tin Tức:
- Tạo một số tin tức với thông tin từ files gốc

## 🎨 Static Files

Chạy lệnh để collect static files:

```bash
python manage.py collectstatic --noinput
```

## 📸 Upload Hình Ảnh

- Hình ảnh tin tức sẽ được lưu tại: `media/news_images/`
- Hình ảnh tác giả sẽ được lưu tại: `media/avatars/`

## 🔍 API Endpoints

| URL | Mô Tả |
|-----|-------|
| `/` | Trang chủ |
| `/tin/<slug>/` | Chi tiết tin tức |
| `/tim-kiem/?q=keyword` | Tìm kiếm |
| `/danh-muc/<slug>/` | Danh mục |
| `/tac-gia/<pk>/` | Tác giả |
| `/api/subscribe-newsletter/` | Đăng ký newsletter (POST) |

## ⚙️ Cấu hình Nâng Cao

### Pagination
Số lượng tin trên mỗi trang: `12` (có thể sửa trong `views.py`)

### Cache
Để thêm cache, cài đặt:
```bash
pip install django-caching
```

### Database
Mặc định sử dụng SQLite. Để dùng PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webtintuc_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

### Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### VPS/Server
```bash
pip install gunicorn whitenoise
# Cấu hình nginx/apache
# Thiết lập SSL certificate
```

## 🐛 Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Migration Error
```bash
python manage.py migrate --fake-initial
```

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Error
```bash
python manage.py flush  # Xóa tất cả dữ liệu
python manage.py migrate
```

## 📚 Tài Liệu Tham Khảo

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)

## ✅ Checklist

- [ ] Cài đặt dependencies
- [ ] Cấu hình settings.py
- [ ] Cấu hình urls.py
- [ ] Tạo migrations
- [ ] Chạy migrations
- [ ] Tạo superuser
- [ ] Chạy server
- [ ] Thêm dữ liệu mẫu
- [ ] Test các chức năng
- [ ] Deploy

## 💡 Tips

1. Dùng `python manage.py shell` để test code
2. Dùng `django-debug-toolbar` để debug
3. Dùng `django-extensions` cho commands hữu ích
4. Dùng `pytest-django` để viết tests
5. Dùng `black` để format code
6. Dùng `flake8` để lint code

## 🤝 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra Django version: `python -m django --version`
2. Kiểm tra migrations: `python manage.py showmigrations`
3. Xem logs: `python manage.py runserver --verbosity 2`
4. Kiểm tra database: `python manage.py dbshell`

---

**Chúc bạn thành công! 🎉**
