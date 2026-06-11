# Simplified News Website Project

This project has been simplified to match the knowledge of students learning programming (C, C++, Java, Python, JavaScript).

## What Was Simplified

### 1. **Models (Django ORM)**
- Removed complex fields (image uploads, icons, colors, timestamps)
- Kept only essential fields: title, content, author, category, views, status
- Removed custom methods and properties
- Simplified to basic field types

### 2. **Views (Django Views)**
- Changed from Generic Views to simple function-based views
- Removed complex Q() queries for search
- Removed pagination
- Removed AJAX/JSON API endpoints
- Simple database queries only

### 3. **Settings**
- Removed unnecessary middleware
- Removed complex configuration
- Kept only essential Django apps

### 4. **Requirements**
- Removed extra packages
- Now only: Django==4.2.0, Pillow==10.0.0

### 5. **Templates**
- Removed Font Awesome icons
- Removed complex JavaScript
- Removed inline CSS styling
- Simple HTML structure
- Responsive design with basic CSS

### 6. **CSS**
- One simple CSS file instead of complex framework
- Grid layout for news items
- Mobile responsive with media queries
- No animations or complex styling

### 7. **Database Models**
- Category: name, slug
- Author: name, email
- News: title, slug, category, author, description, content, status, views, published_at

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Make migrations
```bash
python manage.py makemigrations
```

### 3. Migrate database
```bash
python manage.py migrate
```

### 4. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 5. Run server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

### 6. Admin Panel
Go to: http://127.0.0.1:8000/admin

Login with superuser credentials

## Project Structure

```
project/
├── config/           # Django configuration
│   ├── settings.py  # Simplified settings
│   ├── urls.py
│   ├── wsgi.py
├── Webtintuc/        # Main app
│   ├── models.py     # 3 simple models
│   ├── views.py      # 6 function-based views
│   ├── urls.py
│   ├── templates/    # Simple HTML templates
│   │   ├── base.html
│   │   ├── trang_chu.html (homepage)
│   │   ├── chi-tiet-tin.html (detail)
│   │   ├── search_results.html
│   │   ├── category_news.html
│   │   ├── author_news.html
│   ├── static/
│   │   └── css/
│   │       └── style.css  # One simple CSS file
├── db.sqlite3        # Database
├── manage.py
├── requirements.txt
```

## Code Examples

### Simple Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
```

### Simple View
```python
def index(request):
    featured_news = News.objects.filter(is_featured=True, status='published').first()
    latest_news = News.objects.filter(status='published')[:8]
    context = {'featured_news': featured_news, 'latest_news': latest_news}
    return render(request, 'trang_chu.html', context)
```

### Simple Template
```html
{% for news in latest_news %}
    <div class="news-card">
        <h3><a href="{% url 'webtintuc:news_detail' news.slug %}">{{ news.title }}</a></h3>
        <p>{{ news.description }}</p>
    </div>
{% endfor %}
```

## Learning Path

This project matches your learning schedule:
- **06/2026**: C/C++ basics - understand code structure
- **07/2026**: Java/Python - apply OOP concepts here
- **07-08/2026**: Python - project uses Python/Django
- **08/2026**: JavaScript - minimal, can be added later
- **09/2026**: C#/PHP - concepts are similar

## Next Steps

1. Add more features as you learn
2. Try adding user authentication
3. Add comments on articles
4. Create an API with Django REST Framework
5. Build a React frontend

---

All code is written simply for learning purposes. No complex patterns or advanced techniques.
