```markdown
# SESSION 7 (4H) – FINAL PLAN  
**"API Completion + Debugging & Performance Optimization"**

> **Continue from Session 6**  
> Students have:  
> - `api/` folder with `serializers.py`, `views.py`, `urls.py`  
> - 2 FBV APIs: `GET /api/posts/`, `POST /api/posts/create/`  
> - Session auth + Postman  
> - Secure settings  

---

## 0. Warm-up & Git Pull (5 min)

```bash
git pull
python manage.py runserver
```
→ Open Postman → “Today: **Complete the API** + **make it fast & debuggable**.”

---

## PART 1: COMPLETE THE API (1H 30M)

---

### 1. Add `GET` Single Post – FBV (20 min)

**`api/views.py`**
```python
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk, published=True)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostSerializer(post)
    return Response(serializer.data)
```

**`api/urls.py`**
```python
path('posts/<int:pk>/', post_detail, name='api_post_detail'),
```

> **Explain**:
> - `pk` from URL → get single post
> - `404` if not found or not published

---

### 2. Add `PUT` Update Post – FBV (25 min)

**`api/views.py`**
```python
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    
    if post.author != request.user:
        return Response({'error': 'You can only edit your own posts'}, status=403)
    
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
```

**`api/urls.py`**
```python
path('posts/<int:pk>/update/', post_update, name='api_post_update'),
```

> **Explain**:
> - `partial=True` → allow partial updates
> - **Ownership check** → only author can edit

---

### 3. Add `DELETE` Post – FBV (15 min)

**`api/views.py`**
```python
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=404)
    
    if post.author != request.user:
        return Response({'error': 'Not authorized'}, status=403)
    
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```

**`api/urls.py`**
```python
path('posts/<int:pk>/delete/', post_delete, name='api_post_delete'),
```

---

### 4. Class-Based View (CBV) Example – `GET` All Posts (20 min)

**`api/views.py`**
```python
from rest_framework.views import APIView

class PostListCBV(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.filter(published=True).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
```

**`api/urls.py`**
```python
path('cbv/posts/', PostListCBV.as_view(), name='api_cbv_post_list'),
```

> **Explain**:
> - `APIView` → base for CBVs
> - `get()` method → handles GET
> - Same logic as FBV, but **class-based**

**Compare**:
| FBV | CBV |
|-----|-----|
| `@api_view` | `class X(APIView)` |
| `def func(request)` | `def get(self, request)` |
| Simple | Reusable with mixins |

---

### 5. Final API Endpoints (10 min)

| Method | URL | Action |
|-------|-----|--------|
| GET | `/api/posts/` | List (FBV) |
| GET | `/api/posts/1/` | Detail (FBV) |
| POST | `/api/posts/create/` | Create |
| PUT | `/api/posts/1/update/` | Update |
| DELETE | `/api/posts/1/delete/` | Delete |
| GET | `/api/cbv/posts/` | List (CBV) |

---

## PART 2: DEBUGGING & PERFORMANCE (2H)

---

### 6. Django Debug Toolbar (25 min)

```bash
pip install django-debug-toolbar
```

**`settings.py`**
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ...]

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}
```

**`urls.py`**
```python
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

> **Show**:
> - SQL queries
> - Template rendering time
> - Cache hits

---

### 7. Query Optimization – `select_related` & `prefetch_related` (25 min)

**Problem**: N+1 queries in `post_list`

**Fix in `api/views.py`**
```python
from django.db.models import Prefetch

def post_list(request):
    posts = Post.objects.filter(published=True)\
        .select_related('author')\
        .order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
```

> **Explain**:
> - `select_related('author')` → JOIN → 1 query instead of 100
> - Use for `ForeignKey`, `OneToOne`
> - `prefetch_related` → for `ManyToMany`, reverse FK

---

### 8. Logging & Error Tracking (20 min)

**`settings.py`**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

> **Show**:
> - 500 errors → saved to `errors.log`
> - Use `logger.error()` in views

---

### 9. Caching with Redis (30 min)

```bash
pip install redis django-redis
```

**`settings.py`**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**Cache API list**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
@api_view(['GET'])
def post_list(request):
    ...
```

> **Explain**:
> - Redis → in-memory cache
> - `cache_page` → cache entire view
> - Great for **read-heavy** APIs

---

### 10. Code Profiling – Find Slow Code (15 min)

```bash
pip install django-silk
```

**`settings.py`**
```python
INSTALLED_APPS += ['silk']
MIDDLEWARE = ['silk.middleware.SilkyMiddleware', ...]
```

→ Visit `/silk/` → see **slow queries**, **time per request**

> **Say**:
> “Use Silk in **dev only** — never in prod.”

---

## 11. Final Demo + Git Branch (15 min)

### Test Full Flow in Postman:
1. GET list → cached
2. Create → update → delete
3. CBV vs FBV → same result
4. Debug Toolbar → 1 query
5. Silk → response time

### Git
```bash
git checkout -b feature/api-complete-debug-perf
git add .
git commit -m "Complete API (CRUD), CBV example, Debug Toolbar, Query opt, Redis cache, Logging"
git push origin feature/api-complete-debug-perf
```

---

## 12. Merge to `main` (10 min)

→ PR → Merge → `git pull`

---

# END OF SESSION 7

**Students now have:**
- **Full CRUD API** (FBV + CBV example)
- **Ownership checks**
- **Debug Toolbar** → see queries
- **Query optimization**
- **Logging** → track errors
- **Redis caching**
- **Silk profiling**

---

# HOMEWORK
1. Add **PATCH** for partial update  
2. Add **API versioning** (`/api/v1/posts/`)  
3. Use **Sentry** for error tracking (optional)  
4. Push to `feature/api-v1`

---

# NEXT SESSION (Session 8)
> **Testing (Unit + Integration)**  
> **CI/CD with GitHub Actions**  
> **Docker & Deployment**  
> **Final Project**

---

**You’re golden!**  
Paste into `session7_plan.md` → **complete, optimized, debuggable**.
```

---

**Save as:** `session7_plan.md`  
**Open in:** Typora / Obsidian → **full color + code**  
**Export PDF:** Typora → perfect handout

**Ready for Session 8?** Say: **“Session 8 plan”**
