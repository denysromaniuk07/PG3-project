from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Base model with created_at and updated_at timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Model with soft delete capability"""
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark object as deleted without removing from database"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    @classmethod
    def active_objects(cls):
        """Get only non-deleted objects"""
        return cls.objects.filter(is_deleted=False)


class StatusModel(models.Model):
    """Base model with status field"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    class Meta:
        abstract = True


class RatableModel(models.Model):
    """Base model for rateable content"""
    rating = models.FloatField(
        default=0,
        help_text="Average rating score"
    )
    total_ratings = models.IntegerField(
        default=0,
        help_text="Total number of ratings"
    )

    class Meta:
        abstract = True

    def update_rating(self, new_rating):
        """Update rating with new vote"""
        self.total_ratings += 1
        self.rating = (self.rating * (self.total_ratings - 1) + new_rating) / self.total_ratings
        self.save()


class CountableModel(models.Model):
    """Base model for countable metrics (likes, views, etc.)"""
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_likes(self):
        """Increment like count"""
        self.likes_count += 1
        self.save(update_fields=['likes_count'])

    def decrement_likes(self):
        """Decrement like count"""
        if self.likes_count > 0:
            self.likes_count -= 1
            self.save(update_fields=['likes_count'])
