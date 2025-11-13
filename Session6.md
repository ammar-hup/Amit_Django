```markdown
# SESSION 5 (4H) – FINAL PLAN  
**"Security & Application Hardening – Full Auth + Custom User"**

> **Continue from Session 4**  
> Students have:  
> - Blog with `Author` → `Post`  
> - `PostForm`, create post (FBV)  
> - Bootstrap UI  
> - Git PR workflow  
> - `.env` security

---

## 0. Warm-up & Git Pull (5 min)

```bash
git pull
python manage.py runserver
```
→ Open blog → “Today: **Real users sign up, log in, and own posts** — **securely**.”

---

## 1. Replace `OneToOneField` → `AbstractUser` for `Author` (30 min)

> **Goal**: Use **custom user model** from the start (Django best practice)

### Step 1: Update `blog/models.py`
```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Author(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

### Step 2: Update `settings.py`
```python
AUTH_USER_MODEL = 'blog.Author'
```

### Step 3: Fresh Migrations
```bash
# WARNING: Only works on fresh DB!
rm db.sqlite3
rm -r blog/migrations/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

> **Explain**:
> - `AbstractUser` → **extends Django User** with extra fields
> - `AUTH_USER_MODEL` → tells Django: **“Use my Author, not default User”**
> - **Cannot change later** → must be set **before first migrate**

---

## 2. Authentication & Authorization – Login/Signup/Logout (40 min)

### Create `blog/forms.py` (add auth forms)
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Author
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
```

### Update `blog/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

### Add Views in `blog/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PostForm, SignUpForm
from .models import Post

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/auth_form.html', {'form': form, 'title': 'Sign Up'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
    return render(request, 'blog/auth_form.html', {'title': 'Log In'})

@login_required
def logout_view(request):
    logout(request)
    return redirect('post_list')
```

---

## 3. CSRF, XSS, SQL Injection Prevention (25 min)

### Already Safe:
| Threat | Django Protection |
|-------|-------------------|
| **CSRF** | `{% csrf_token %}` |
| **XSS** | Auto-escape in templates |
| **SQLi** | ORM → no raw SQL |

### Show XSS Example
```html
<!-- Safe -->
{{ post.content|linebreaks }}

<!-- Unsafe (never do) -->
{{ post.content|safe }}  <!-- allows <script>alert()</script> -->
```

> **Say**:  
> “Django **escapes by default** → safe from XSS”

---

## 4. Secure Settings (HTTPS, Secrets, etc.) (20 min)

### Update `.env`
```env
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Update `settings.py`
```python
from decouple import config, Csv

DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='', cast=Csv())

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
```

> **Explain**:
> - `SECURE_SSL_REDIRECT` → force HTTPS
> - `SESSION_COOKIE_SECURE` → cookies only over HTTPS
> - `DEBUG=False` → no stack traces in prod

---

## 5. User Roles & Permissions (25 min)

### Add to `Author` model
```python
    is_editor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
```

### Use in Views
```python
@login_required
def post_create(request):
    if not request.user.is_editor and not request.user.is_admin:
        return render(request, 'blog/error.html', {'message': 'You are not authorized to create posts.'})
    # ... rest
```

### Admin: Assign roles
→ Check `is_editor` for users

> **Say**:  
> “Django has **Groups & Permissions** too — we’ll use later”

---

## 6. Best Deployment Practices (20 min)

| Practice | Why |
|--------|-----|
| `DEBUG=False` | No errors in public |
| `.env` not in Git | Secrets safe |
| `collectstatic` | Serve CSS efficiently |
| Gunicorn + Nginx | Production server |
| HTTPS | Encrypt traffic |

---

## 7. Templates – Auth Pages (15 min)

### `templates/blog/auth_form.html`
```html
{% extends 'blog/base.html' %}
{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-danger text-white">
                <h3>{{ title }}</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {% for field in form %}
                    <div class="mb-3">
                        {{ field.label_tag }}
                        {{ field }}
                        {% if field.errors %}
                            <div class="text-danger small">{{ field.errors }}</div>
                        {% endif %}
                    </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-danger">{{ title }}</button>
                </form>
                {% if title == 'Log In' %}
                <p class="mt-3">Don't have an account? <a href="{% url 'signup' %}">Sign up</a></p>
                {% else %}
                <p class="mt-3">Already have an account? <a href="{% url 'login' %}">Log in</a></p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 8. Update Navbar – Auth Links (10 min)

**`base.html`**
```html
<ul class="navbar-nav ms-auto">
    {% if user.is_authenticated %}
    <li class="nav-item"><a class="nav-link" href="{% url 'post_create' %}">New Post</a></li>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
            {{ user.get_full_name|default:user.username }}
        </a>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Profile</a></li>
            <li><a class="dropdown-item" href="{% url 'logout' %}">Logout</a></li>
        </ul>
    </li>
    {% else %}
    <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Log In</a></li>
    <li class="nav-item"><a class="nav-link" href="{% url 'signup' %}">Sign Up</a></li>
    {% endif %}
</ul>
```

---

## 9. Final Demo + Git Branch (15 min)

### Test:
1. Sign up → login → create post → logout
2. Try creating post while logged out → redirected

### Git
```bash
git checkout -b feature/auth-custom-user
git add .
git commit -m "Custom AbstractUser, signup/login/logout, secure settings"
git push origin feature/auth-custom-user
```

---

## 10. Merge & Deploy Prep (10 min)

→ Merge PR  
→ `DEBUG=False` in `.env`  
→ `python manage.py collectstatic`

---

# END OF SESSION 5

**Students now have:**
- Custom `Author` with `AbstractUser`
- Full **signup / login / logout**
- Secure settings
- Role-based access
- Production-ready auth

---

# HOMEWORK
1. Add **password change** view  
2. Add **profile edit** page  
3. Use **signals** to auto-create `Author` on user creation  
4. Push to `feature/profile`

---

# NEXT SESSION (Session 6)
> **Signals & Auto-Profile**  
> **Class-Based Views**  
> **Deployment to Render.com**  
> **Final Project Polish**

---

**You’re golden!**  
Paste into `session5_plan.md` → **ready to teach, secure, professional**.
```

---

**Save as:** `session5_plan.md`  
**Open in:** Typora / Obsidian → **full color + code**  
**Export PDF:** Typora → perfect handout

**Ready for Session 6?** Say: **“Session 6 plan”**