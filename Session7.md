```markdown
# SESSION 6 (4H) – FINAL PLAN  
**"API Development & Integration – DRF Basics + Postman"**

> **Continue from Session 5**  
> Students have:  
> - Custom `Author` (AbstractUser)  
> - Full auth: signup/login/logout  
> - Secure settings + roles  
> - Bootstrap UI  
> - Git workflow  

---

## 0. Warm-up & Git Pull (5 min)

```bash
git pull
python manage.py runserver
```
→ Open blog → “Today: **Your blog gets a simple API** — learn DRF basics with just 2 endpoints.”

---

## 1. Introduction to Django REST Framework (DRF) (20 min)

### Install & Setup
```bash
pip install djangorestframework
```

### `settings.py`
```python
INSTALLED_APPS += [
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

### Project `urls.py`
```python
from django.urls import path, include

urlpatterns += [
    path('api/', include('api.urls')),
]
```

> **Explain**:
> - `DRF` → turns models into **JSON APIs**
> - `SessionAuthentication` → uses Django login sessions
> - `IsAuthenticatedOrReadOnly` → GET open, POST needs login

---

## 2. Create `api` Folder & Serializers – Model ↔ JSON (25 min)

### Create folder:
```bash
mkdir api
touch api/__init__.py api/serializers.py api/views.py api/urls.py
```

### `api/serializers.py`
```python
from rest_framework import serializers
from blog.models import Post, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'published', 'author']
        read_only_fields = ['author', 'created_at']
```

> **Explain**:
> - `Serializer` = **Form for APIs**
> - `read_only=True` → can't change author
> - Nested serializer → `author` shows full user data

---

## 3. Function-Based Views (FBV) for APIs – List & Create (30 min)

### `api/views.py`
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.models import Post
from .serializers import PostSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

> **Explain**:
> - `@api_view` → handles JSON + HTTP methods
> - `Response` → returns JSON
> - `many=True` → serialize list
> - `author=request.user` → auto-set from logged-in user

---

## 4. API URLs – Simple Paths (15 min)

### `api/urls.py`
```python
from django.urls import path
from .views import post_list, post_create

urlpatterns = [
    path('posts/', post_list, name='api_post_list'),
    path('posts/create/', post_create, name='api_post_create'),
]
```

**Endpoints**:
| Method | URL | Action |
|-------|-----|--------|
| GET | `/api/posts/` | List published posts |
| POST | `/api/posts/create/` | Create new post |

---

## 5. Authentication – Use Sessions (20 min)

> **Explain**:
> - DRF uses **Django sessions** → login on web, API works
> - No JWT today → keep simple
> - For mobile: send cookies or use token later

### Test with `curl`
```bash
# 1. GET list (no auth needed)
curl http://127.0.0.1:8000/api/posts/
```

```bash
# 2. POST create (needs session – use browser or simulate)
# First, login on /login/ to get session
curl -X POST http://127.0.0.1:8000/api/posts/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "API Post", "content": "From curl", "published": true}' \
  --cookie "sessionid=your_session_id_here"
```

---

## 6. API Testing with Postman (30 min)

### Live Demo:
1. **New collection**: AMIT Blog API
2. **GET /api/posts/** → see JSON list
3. **POST /api/posts/create/** → add auth (session cookie from browser)
4. **Invalid data** → 400 error
5. **No auth** → 403 for POST

### Postman Tips:
- Save session cookie as variable
- Tests: `pm.response.to.have.status(200)`

---

## 7. Secure API Settings (15 min)

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

> **Say**:
> - `IsAuthenticatedOrReadOnly` → read open, write protected
> - Pagination → limit results

---

## 8. Final Demo + Git Branch (20 min)

### Full Flow:
1. Browser login → Postman GET → list posts
2. Postman POST → create post → see in blog
3. No login → POST fails

### Git
```bash
git checkout -b feature/simple-drf-api
git add .
git commit -m "Simple DRF API with FBV: list + create posts"
git push origin feature/simple-drf-api
```

---

## 9. Merge to `main` (10 min)

→ Open PR → Merge → `git pull`

---

# END OF SESSION 6

**Students now have:**
- Basic **DRF API** with FBV
- Serializers for Post + Author
- 2 endpoints: GET list, POST create
- Session auth (simple)
- Postman testing
- Secure + paginated

---

# HOMEWORK
1. Add **GET single post** endpoint  
2. Add **validation** in serializer  
3. Test errors in Postman  
4. Push to `feature/single-post-api`

---

# NEXT SESSION (Session 7)
> **DRF Advanced: ViewSets**  
> **JWT Auth**  
> **API Docs**  
> **Integration Testing**

---

**You’re golden!**  
Paste into `session6_plan.md` → **ready to teach, simple DRF intro**.
```