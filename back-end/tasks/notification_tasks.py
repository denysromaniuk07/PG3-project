"""
Notification tasks.
Manages notification delivery, scheduling, and cleanup.
"""

import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from api.models import User
from services import NotificationService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2)
def send_notification_async(self, user_id, notification_type, title, message, related_user_id=None):
    """
    Send a notification asynchronously.
    
    Args:
        user_id: Recipient user ID
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        related_user_id: Optional related user ID
    """
    try:
        user = User.objects.get(id=user_id)
        related_user = User.objects.get(id=related_user_id) if related_user_id else None
        
        NotificationService.create_notification(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            related_user=related_user
        )
        
        logger.info(f"Notification sent to user {user_id}: {notification_type}")
    
    except User.DoesNotExist:
        logger.warning(f"User {user_id} not found for notification")
    except Exception as exc:
        logger.error(f"Error sending notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=2)


@shared_task
def cleanup_old_notifications(days=30):
    """
    Delete notifications older than specified days.
    
    Args:
        days: Days to keep
    """
    try:
        from api.models import Notification
        
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count, _ = Notification.objects.filter(
            created_at__lt=cutoff_date,
            is_read=True
        ).delete()
        
        logger.info(f"Deleted {deleted_count} old notifications")
    
    except Exception as exc:
        logger.error(f"Error cleaning up notifications: {str(exc)}")


@shared_task
def send_mention_notifications(user_ids, mention_type, content_id):
    """
    Send mention notifications to multiple users.
    
    Args:
        user_ids: List of user IDs to notify
        mention_type: Type of mention (post, comment, etc.)
        content_id: ID of content mentioning user
    """
    try:
        for user_id in user_ids:
            send_notification_async.delay(
                user_id=user_id,
                notification_type='mention',
                title='You were mentioned',
                message=f'Someone mentioned you in a {mention_type}',
                related_user_id=None
            )
        
        logger.info(f"Sent mention notifications to {len(user_ids)} users")
    
    except Exception as exc:
        logger.error(f"Error sending mention notifications: {str(exc)}")


@shared_task
def send_like_notifications(user_id, liker_id, content_type):
    """
    Send notification when user's content is liked.
    
    Args:
        user_id: Content owner user ID
        liker_id: User who liked the content
        content_type: Type of content (post, comment, etc.)
    """
    try:
        liker = User.objects.get(id=liker_id)
        
        send_notification_async.delay(
            user_id=user_id,
            notification_type='like',
            title=f'{liker.get_full_name()} liked your {content_type}',
            message='Check out the engagement on your content',
            related_user_id=liker_id
        )
        
        logger.info(f"Like notification sent to user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error sending like notification: {str(exc)}")


@shared_task
def send_comment_notifications(user_id, commenter_id, content_type):
    """
    Send notification when content receives a comment.
    
    Args:
        user_id: Content owner user ID
        commenter_id: User who commented
        content_type: Type of content
    """
    try:
        commenter = User.objects.get(id=commenter_id)
        
        send_notification_async.delay(
            user_id=user_id,
            notification_type='comment',
            title=f'{commenter.get_full_name()} commented on your {content_type}',
            message='See what they said',
            related_user_id=commenter_id
        )
        
        logger.info(f"Comment notification sent to user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error sending comment notification: {str(exc)}")


@shared_task
def mark_notifications_read_batch(user_id):
    """
    Mark all notifications as read for a user.
    Used when user opens notification center.
    
    Args:
        user_id: User ID
    """
    try:
        from api.models import Notification
        
        updated_count = Notification.objects.filter(
            user_id=user_id,
            is_read=False
        ).update(is_read=True)
        
        logger.info(f"Marked {updated_count} notifications as read for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error marking notifications as read: {str(exc)}")


@shared_task
def send_batch_notifications(notifications_data):
    """
    Send multiple notifications in batch.
    
    Args:
        notifications_data: List of dicts with notification info
        
    Example:
        [
            {
                'user_id': 1,
                'notification_type': 'achievement',
                'title': '...',
                'message': '...'
            }
        ]
    """
    try:
        for notif_data in notifications_data:
            send_notification_async.delay(
                user_id=notif_data['user_id'],
                notification_type=notif_data['notification_type'],
                title=notif_data['title'],
                message=notif_data['message'],
                related_user_id=notif_data.get('related_user_id')
            )
        
        logger.info(f"Queued {len(notifications_data)} notifications for sending")
    
    except Exception as exc:
        logger.error(f"Error sending batch notifications: {str(exc)}")
