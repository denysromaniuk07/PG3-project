"""
Resume processing tasks.
Handles async resume analysis and skill extraction.
"""

import logging
from celery import shared_task
from api.models import Resume, User
from services import ResumeService, AchievementService, NotificationService
from tasks.email_tasks import send_achievement_email

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def analyze_resume_async(self, resume_id):
    """
    Analyze resume asynchronously.
    
    Args:
        resume_id: Resume ID to analyze
    """
    try:
        resume = Resume.objects.get(id=resume_id)
        
        logger.info(f"Starting resume analysis for resume {resume_id}")
        
        # Perform ML analysis
        ResumeService._sync_identified_skills(
            resume.user,
            resume.extracted_skills
        )
        
        # Check for achievements
        AchievementService.check_and_unlock_achievements(resume.user)
        
        # Notify user
        NotificationService.create_notification(
            user=resume.user,
            notification_type='system',
            title='Resume Analyzed',
            message=f'Your resume has been analyzed. Score: {resume.total_score}/100'
        )
        
        logger.info(f"Resume analysis completed for resume {resume_id}")
    
    except Resume.DoesNotExist:
        logger.warning(f"Resume {resume_id} not found")
    except Exception as exc:
        logger.error(f"Error analyzing resume {resume_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task(bind=True, max_retries=3)
def extract_resume_text_async(self, resume_id):
    """
    Extract text from resume file.
    
    Args:
        resume_id: Resume ID
    """
    try:
        resume = Resume.objects.get(id=resume_id)
        
        # Extract text
        from api.ml_utils import extract_text_from_resume
        extracted_text = extract_text_from_resume(resume.file, resume.file_type)
        
        resume.extracted_text = extracted_text
        resume.save()
        
        logger.info(f"Text extracted from resume {resume_id}")
    
    except Exception as exc:
        logger.error(f"Error extracting text from resume {resume_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task
def batch_analyze_resumes():
    """
    Analyze all pending resumes in batch.
    Useful for background processing.
    """
    try:
        pending_resumes = Resume.objects.filter(
            extracted_text='',
            analyzed_at__isnull=True
        )
        
        for resume in pending_resumes:
            analyze_resume_async.delay(resume.id)
        
        logger.info(f"Queued {pending_resumes.count()} resumes for analysis")
    
    except Exception as exc:
        logger.error(f"Error in batch analyze resumes: {str(exc)}")


@shared_task
def cleanup_old_resumes(days=90):
    """
    Delete resumes older than specified days.
    
    Args:
        days: Days to keep
    """
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        old_resumes = Resume.objects.filter(
            created_at__lt=cutoff_date,
            is_deleted=True
        )
        
        deleted_count = old_resumes.count()
        old_resumes.delete()
        
        logger.info(f"Deleted {deleted_count} old resumes")
    
    except Exception as exc:
        logger.error(f"Error cleaning up old resumes: {str(exc)}")
