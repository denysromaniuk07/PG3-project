"""
Email notification tasks.
Sends emails asynchronously for notifications, digests, and alerts.
"""

import logging
from celery import shared_task
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from api.models import User
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id):
    """
    Send welcome email to new user.
    
    Args:
        user_id: ID of new user
    """
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user,
            'site_name': 'AI Career Platform',
            'activation_url': f"{settings.FRONTEND_URL}/activate/{user.id}/",
        }
        
        html_message = render_to_string('emails/welcome.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Welcome to AI Career Platform!',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent to {user.email}")
        
    except User.DoesNotExist:
        logger.warning(f"User {user_id} not found for welcome email")
    except Exception as exc:
        logger.error(f"Error sending welcome email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_achievement_email(self, user_id, achievement_name, points):
    """
    Send achievement unlocked email.
    
    Args:
        user_id: User ID
        achievement_name: Achievement name
        points: Points awarded
    """
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user,
            'achievement_name': achievement_name,
            'points': points,
            'profile_url': f"{settings.FRONTEND_URL}/profile/{user.id}/",
        }
        
        html_message = render_to_string('emails/achievement.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f'🎉 Achievement Unlocked: {achievement_name}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Achievement email sent to {user.email}: {achievement_name}")
        
    except Exception as exc:
        logger.error(f"Error sending achievement email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_job_match_email(self, user_id, job_id):
    """
    Send job match notification email.
    
    Args:
        user_id: User ID
        job_id: Job ID
    """
    try:
        user = User.objects.get(id=user_id)
        from api.models import JobOpportunity
        job = JobOpportunity.objects.get(id=job_id)
        
        context = {
            'user': user,
            'job': job,
            'job_url': f"{settings.FRONTEND_URL}/jobs/{job.id}/",
        }
        
        html_message = render_to_string('emails/job_match.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f'Job Match: {job.title} at {job.company_name}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Job match email sent to {user.email}")
        
    except Exception as exc:
        logger.error(f"Error sending job match email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_mentor_request_email(self, mentor_id, session_id):
    """
    Send mentor request notification email.
    
    Args:
        mentor_id: Mentor user ID
        session_id: Mentor session ID
    """
    try:
        mentor = User.objects.get(id=mentor_id)
        from api.models import MentorSession
        session = MentorSession.objects.get(id=session_id)
        
        context = {
            'mentor': mentor,
            'mentee': session.mentee,
            'session': session,
            'respond_url': f"{settings.FRONTEND_URL}/mentoring/{session.id}/",
        }
        
        html_message = render_to_string('emails/mentor_request.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f'New Mentoring Request from {session.mentee.get_full_name()}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mentor.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Mentor request email sent to {mentor.email}")
        
    except Exception as exc:
        logger.error(f"Error sending mentor request email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_course_enrollment_email(self, user_id, course_id):
    """
    Send course enrollment confirmation email.
    
    Args:
        user_id: User ID
        course_id: Course ID
    """
    try:
        user = User.objects.get(id=user_id)
        from api.models import Course
        course = Course.objects.get(id=course_id)
        
        context = {
            'user': user,
            'course': course,
            'course_url': f"{settings.FRONTEND_URL}/courses/{course.id}/",
        }
        
        html_message = render_to_string('emails/course_enrollment.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=f'Enrollment Confirmed: {course.title}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Course enrollment email sent to {user.email}")
        
    except Exception as exc:
        logger.error(f"Error sending course enrollment email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_daily_digest():
    """
    Send daily digest email to active users.
    Contains: new recommendations, achievements, community highlights.
    """
    try:
        from services import RecommendationService, AnalyticsService
        
        # Get active users from last 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        users = User.objects.filter(
            last_login__gte=seven_days_ago,
            is_active=True
        )
        
        email_list = []
        
        for user in users:
            try:
                # Get personalized data
                recommendations = RecommendationService.get_personalized_dashboard(user)
                stats = AnalyticsService.get_user_stats(user)
                
                context = {
                    'user': user,
                    'recommendations': recommendations,
                    'stats': stats,
                    'dashboard_url': f"{settings.FRONTEND_URL}/dashboard/",
                }
                
                html_message = render_to_string('emails/daily_digest.html', context)
                plain_message = strip_tags(html_message)
                
                email_list.append((
                    f'Your Daily Digest - {timezone.now().strftime("%B %d, %Y")}',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message
                ))
            
            except Exception as e:
                logger.warning(f"Error preparing digest for user {user.id}: {str(e)}")
                continue
        
        # Send all emails in batch
        if email_list:
            send_mass_mail(email_list, fail_silently=False)
            logger.info(f"Daily digest emails sent to {len(email_list)} users")
    
    except Exception as exc:
        logger.error(f"Error sending daily digests: {str(exc)}")


@shared_task
def send_weekly_report():
    """
    Send weekly activity report to all users.
    """
    try:
        from services import AnalyticsService
        
        users = User.objects.filter(is_active=True)
        email_list = []
        
        for user in users:
            try:
                stats = AnalyticsService.get_user_stats(user)
                
                context = {
                    'user': user,
                    'stats': stats,
                    'report_url': f"{settings.FRONTEND_URL}/analytics/",
                }
                
                html_message = render_to_string('emails/weekly_report.html', context)
                plain_message = strip_tags(html_message)
                
                email_list.append((
                    f'Your Weekly Report - {timezone.now().strftime("%B %d, %Y")}',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message
                ))
            
            except Exception as e:
                logger.warning(f"Error preparing report for user {user.id}: {str(e)}")
                continue
        
        if email_list:
            send_mass_mail(email_list, fail_silently=False)
            logger.info(f"Weekly reports sent to {len(email_list)} users")
    
    except Exception as exc:
        logger.error(f"Error sending weekly reports: {str(exc)}")


@shared_task
def send_password_reset_email(user_id, reset_token):
    """
    Send password reset email.
    
    Args:
        user_id: User ID
        reset_token: Reset token
    """
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user,
            'reset_url': f"{settings.FRONTEND_URL}/reset-password/{reset_token}/",
            'expiry_hours': 24,
        }
        
        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Reset Your Password',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Password reset email sent to {user.email}")
    
    except Exception as exc:
        logger.error(f"Error sending password reset email: {str(exc)}")
