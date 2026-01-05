# Core Module Usage Guide

The `core/` module provides reusable components to speed up development and maintain consistency across your application.

## 🏗️ Base Models

### TimeStampedModel

Auto-adds `created_at` and `updated_at` fields to any model.

```python
from core import TimeStampedModel

class Article(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # created_at and updated_at are automatic
```

### SoftDeleteModel

Soft delete (mark as deleted without removing from DB).

```python
from core import SoftDeleteModel

class User(SoftDeleteModel):
    name = models.CharField(max_length=100)

    # Usage
    user = User.objects.get(id=1)
    user.soft_delete()  # Mark as deleted
    user.restore()      # Restore
    User.active_objects()  # Get only active
```

### StatusModel

Track status: active, inactive, archived.

```python
from core import StatusModel

class Course(StatusModel):
    title = models.CharField(max_length=200)
    # status field added automatically
    # Choices: 'active', 'inactive', 'archived'
```

### RatableModel

Rating system for content.

```python
from core import RatableModel

class Review(RatableModel):
    content = models.TextField()
    # rating and total_ratings fields automatic

    # Usage
    review = Review.objects.get(id=1)
    review.update_rating(5)  # Add a 5-star rating
```

### CountableModel

Track views and likes.

```python
from core import CountableModel

class Post(CountableModel):
    title = models.CharField(max_length=200)
    # views_count and likes_count automatic

    # Usage
    post = Post.objects.get(id=1)
    post.increment_views()
    post.increment_likes()
    post.decrement_likes()
```

---

## 🎯 ViewSet Mixins

### OwnerFilterMixin

Filter objects by owner (current user).

```python
from core import OwnerFilterMixin
from rest_framework import viewsets

class MyDataViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    queryset = MyData.objects.all()
    serializer_class = MyDataSerializer
    owner_field = 'user'  # Default: 'user'

    # Usage: GET /api/mydata/ returns only current user's data
```

### CreateUserMixin

Auto-set user when creating objects.

```python
from core import CreateUserMixin

class PostViewSet(CreateUserMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    user_field = 'author'  # Field to set user to

    # Usage: POST creates post with author=request.user
```

### LikeDislikeMixin

Add like/unlike actions to ViewSet.

```python
from core import LikeDislikeMixin

class CommentViewSet(LikeDislikeMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # Adds endpoints:
    # POST /api/comments/{id}/like/
    # POST /api/comments/{id}/unlike/
```

### BulkActionMixin

Bulk delete and status update.

```python
from core import BulkActionMixin

class TodoViewSet(BulkActionMixin, viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    # Adds endpoints:
    # POST /api/todos/bulk_delete/
    # Data: {"ids": [1, 2, 3]}
    # POST /api/todos/bulk_update_status/
    # Data: {"ids": [1, 2, 3], "status": "completed"}
```

### SearchFilterMixin

Add advanced search capability.

```python
from core import SearchFilterMixin

class ArticleViewSet(SearchFilterMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    search_fields = ['title', 'content', 'author__name']

    # Usage: GET /api/articles/?search=django
```

### ExportMixin

Export data as CSV or JSON.

```python
from core import ExportMixin

class ReportViewSet(ExportMixin, viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    # Endpoints:
    # GET /api/reports/export/?format=json
    # GET /api/reports/export/?format=csv
```

### SoftDeleteMixin

Soft delete actions for ViewSet.

```python
from core import SoftDeleteMixin

class DocumentViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    # Adds endpoints:
    # POST /api/documents/{id}/soft_delete/
    # POST /api/documents/{id}/restore/
```

---

## ✔️ Custom Validators

### URLValidator

Validate URLs with specific protocols.

```python
from core import URLValidator
from django.db import models

website_url = models.URLField(
    validators=[URLValidator(protocols=['https'])]
)
# Only accepts https:// URLs
```

### SkillNameValidator

Validate skill names.

```python
from core import SkillNameValidator

skill_name = models.CharField(
    max_length=100,
    validators=[SkillNameValidator()]
)
# Only letters, numbers, spaces, hyphens, periods
```

### UsernameValidator

Enforce username rules.

```python
from core import UsernameValidator

username = models.CharField(
    max_length=30,
    validators=[UsernameValidator()]
)
# 3-30 chars, alphanumeric, underscore, hyphen only
```

### FileTypeValidator

Restrict allowed file types.

```python
from core import FileTypeValidator

resume = models.FileField(
    upload_to='resumes/',
    validators=[FileTypeValidator(allowed_types=['pdf', 'docx', 'txt'])]
)
```

### FileSizeValidator

Limit file sizes.

```python
from core import FileSizeValidator

document = models.FileField(
    upload_to='docs/',
    validators=[FileSizeValidator(max_size_mb=10)]  # Max 10MB
)
```

### DateRangeValidator

Ensure valid date ranges.

```python
from core import DateRangeValidator

class Event(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        DateRangeValidator()({
            'start_date': self.start_date,
            'end_date': self.end_date
        })
```

### BioLengthValidator

Validate bio/description fields.

```python
from core import BioLengthValidator

bio = models.TextField(
    validators=[BioLengthValidator(min_length=10, max_length=500)]
)
```

### EmailDomainValidator

Restrict email domains.

```python
from core import EmailDomainValidator

# Only allow corporate emails
email = models.EmailField(
    validators=[EmailDomainValidator(
        allowed_domains=['company.com', 'company.org']
    )]
)

# Block temporary email services
email = models.EmailField(
    validators=[EmailDomainValidator(
        blocked_domains=['tempmail.com', 'throwaway.email']
    )]
)
```

### SlugValidator

Validate URL-friendly slugs.

```python
from core import SlugValidator

slug = models.SlugField(
    validators=[SlugValidator()]
)
# Only letters, numbers, hyphens, underscores
```

### JSONValidator

Validate JSON field content.

```python
from core import JSONValidator

metadata = models.JSONField(
    validators=[JSONValidator(
        schema={
            'title': str,
            'count': int,
            'active': bool
        }
    )]
)
```

---

## 📚 Complete Example

Here's a complete example using multiple core components:

```python
# models.py
from django.db import models
from core import TimeStampedModel, CountableModel, RatableModel
from core import SkillNameValidator, BioLengthValidator

class Article(TimeStampedModel, CountableModel, RatableModel):
    """Blog article with timestamps, view/like tracking, and ratings"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

# serializers.py
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'author_name',
                  'views_count', 'likes_count', 'rating', 'created_at', 'updated_at']

# views.py
from rest_framework import viewsets
from core import CreateUserMixin, LikeDislikeMixin, SearchFilterMixin

class ArticleViewSet(CreateUserMixin, LikeDislikeMixin, SearchFilterMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    user_field = 'author'
    search_fields = ['title', 'content', 'author__name']

    # Automatically gets:
    # - author set on create
    # - like/unlike actions
    # - search capability
    # - all standard CRUD operations
```

---

## 🎓 Best Practices

1. **Combine mixins wisely** - Don't use conflicting mixins
2. **Use validators** - Always validate user input
3. **Inherit base models** - Share common functionality
4. **Override methods** - Customize mixin behavior when needed
5. **Document custom logic** - Explain why you're customizing

---

## 🔗 Integration with API

The core module is fully integrated with the API:

- All ViewSets use appropriate mixins
- All models use base classes
- All serializers use validators
- All endpoints benefit from pagination, filtering, searching

---

For more examples, see the actual implementations in `api/views_new.py` and `api/models.py`.
