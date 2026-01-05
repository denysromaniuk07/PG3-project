"""
Notification service.
Handles user notifications, alerts, and messaging.
"""

import logging
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from api.models import User
from datetime import timedelta
from django.db import models

logger = logging.getLogger(__name__)


class Notification(models.Model):
    """Model for storing notifications (add to api/models.py)"""
    NOTIFICATION_TYPES = [
        ('achievement', 'Achievement Unlocked'),
        ('mention', 'Mentioned'),
        ('like', 'Post Liked'),
        ('comment', 'Comment Added'),
        ('job_match', 'Job Match'),
        ('mentor_request', 'Mentor Request'),
        ('system', 'System Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


class NotificationService:
    """Service for managing user notifications."""

    @staticmethod
    def create_notification(user, notification_type, title, message, related_user=None):
        """
        Create a notification for a user.
        
        Args:
            user: User to receive notification
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            related_user: User who triggered the notification
        
        Returns:
            Notification object
        """
        from api.models import Notification
        
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            related_user=related_user
        )
        
        # Send email if user has email notifications enabled
        if hasattr(user, 'notification_preferences') and user.notification_preferences.get('email_enabled', True):
            NotificationService.send_email_notification(user, title, message)
        
        logger.info(f"Notification created for user {user.id}: {notification_type}")
        return notification

    @staticmethod
    def send_email_notification(user, subject, message):
        """
        Send email notification to user.
        
        Args:
            user: User object
            subject: Email subject
            message: Email message
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Email notification sent to {user.email}")
        except Exception as e:
            logger.error(f"Error sending email to {user.email}: {str(e)}")

    @staticmethod
    def notify_achievement_unlocked(user, achievement):
        """
        Notify user when they unlock an achievement.
        
        Args:
            user: User object
            achievement: Achievement object
        """
        NotificationService.create_notification(
            user=user,
            notification_type='achievement',
            title=f'Achievement Unlocked: {achievement.name}',
            message=f'You earned {achievement.points_awarded} points!',
        )

    @staticmethod
    def notify_job_match(user, job):
        """
        Notify user about a matching job.
        
        Args:
            user: User object
            job: JobOpportunity object
        """
        NotificationService.create_notification(
            user=user,
            notification_type='job_match',
            title=f'New Job Match: {job.title}',
            message=f'{job.company_name} is hiring for {job.title}. Check it out!',
        )

    @staticmethod
    def notify_mentor_request(mentor, mentee, session):
        """
        Notify mentor about a new session request.
        
        Args:
            mentor: Mentor user object
            mentee: Mentee user object
            session: MentorSession object
        """
        NotificationService.create_notification(
            user=mentor,
            notification_type='mentor_request',
            title=f'New Mentoring Request from {mentee.get_full_name()}',
            message=f'Topic: {session.title}. Review and respond to the request.',
            related_user=mentee
        )

    @staticmethod
    def notify_post_liked(post_author, liker):
        """
        Notify user when their post is liked.
        
        Args:
            post_author: User who created the post
            liker: User who liked the post
        """
        NotificationService.create_notification(
            user=post_author,
            notification_type='like',
            title=f'{liker.get_full_name()} liked your post',
            message='Check out the reactions to your post.',
            related_user=liker
        )

    @staticmethod
    def notify_post_comment(post_author, commenter):
        """
        Notify user when their post gets a comment.
        
        Args:
            post_author: User who created the post
            commenter: User who commented
        """
        NotificationService.create_notification(
            user=post_author,
            notification_type='comment',
            title=f'{commenter.get_full_name()} commented on your post',
            message='See what they said about your post.',
            related_user=commenter
        )

    @staticmethod
    def notify_user_mentioned(mentioned_user, mentioner, content_type):
        """
        Notify user when they are mentioned.
        
        Args:
            mentioned_user: User being mentioned
            mentioner: User doing the mentioning
            content_type: Type of content (post, comment, etc.)
        """
        NotificationService.create_notification(
            user=mentioned_user,
            notification_type='mention',
            title=f'{mentioner.get_full_name()} mentioned you',
            message=f'You were mentioned in a {content_type}.',
            related_user=mentioner
        )

    @staticmethod
    def get_user_notifications(user, unread_only=False, limit=20):
        """
        Get notifications for a user.
        
        Args:
            user: User object
            unread_only: Only get unread notifications
            limit: Maximum number to return
        
        Returns:
            QuerySet of notifications
        """
        from api.models import Notification
        
        query = Notification.objects.filter(user=user)
        
        if unread_only:
            query = query.filter(is_read=False)
        
        return query.order_by('-created_at')[:limit]

    @staticmethod
    def mark_notification_read(notification_id):
        """
        Mark a notification as read.
        
        Args:
            notification_id: Notification ID
        """
        from api.models import Notification
        
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        logger.info(f"Notification {notification_id} marked as read")

    @staticmethod
    def mark_all_read(user):
        """
        Mark all notifications as read for a user.
        
        Args:
            user: User object
        """
        from api.models import Notification
        
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)
        logger.info(f"All notifications marked as read for user {user.id}")

    @staticmethod
    def get_notification_count(user):
        """
        Get unread notification count for a user.
        
        Args:
            user: User object
        
        Returns:
            Unread notification count
        """
        from api.models import Notification
        
        return Notification.objects.filter(user=user, is_read=False).count()

    @staticmethod
    def delete_old_notifications(days=30):
        """
        Delete notifications older than specified days (cleanup task).
        
        Args:
            days: Number of days to keep
        """
        from api.models import Notification
        
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count, _ = Notification.objects.filter(created_at__lt=cutoff_date).delete()
        logger.info(f"Deleted {deleted_count} old notifications")
