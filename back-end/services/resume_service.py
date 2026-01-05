"""
Resume analysis and processing service.
Handles resume file uploads, text extraction, ML analysis, and skill identification.
"""

import logging
from django.core.files.storage import default_storage
from api.models import Resume, Skill, UserSkill
from api.ml_utils import analyze_resume, extract_text_from_resume
from django.db import transaction

logger = logging.getLogger(__name__)


class ResumeService:
    """Service for resume processing and analysis."""

    @staticmethod
    def upload_and_analyze_resume(user, resume_file, file_type='pdf'):
        """
        Upload a resume file and perform ML analysis.
        
        Args:
            user: User object
            resume_file: File object
            file_type: 'pdf' or 'docx'
        
        Returns:
            Resume object with analysis results
        """
        try:
            # Create resume record
            resume = Resume.objects.create(
                user=user,
                file=resume_file,
                file_type=file_type
            )
            
            # Extract text from resume
            extracted_text = extract_text_from_resume(resume_file, file_type)
            resume.extracted_text = extracted_text
            resume.save()
            
            # Perform ML analysis
            analysis_results = analyze_resume(extracted_text)
            
            # Update resume with analysis results
            resume.extracted_skills = analysis_results.get('skills', {})
            resume.skill_gaps = analysis_results.get('gaps', [])
            resume.experience_level = analysis_results.get('experience_level', 'unknown')
            resume.skill_score = analysis_results.get('skill_score', 0)
            resume.total_score = analysis_results.get('total_score', 0)
            resume.save()
            
            # Sync identified skills with user's skill profile
            ResumeService._sync_identified_skills(user, analysis_results.get('skills', {}))
            
            logger.info(f"Resume analyzed for user {user.id}: score={resume.total_score}")
            return resume
        
        except Exception as e:
            logger.error(f"Error analyzing resume for user {user.id}: {str(e)}")
            raise

    @staticmethod
    def _sync_identified_skills(user, identified_skills):
        """
        Sync identified skills from resume to user's skill profile.
        
        Args:
            user: User object
            identified_skills: Dict of {skill_name: confidence_score}
        """
        for skill_name, confidence in identified_skills.items():
            try:
                # Find or create skill
                skill, created = Skill.objects.get_or_create(
                    name__iexact=skill_name,
                    defaults={'name': skill_name, 'category': 'other'}
                )
                
                # Add to user if not already present
                user_skill, created = UserSkill.objects.get_or_create(
                    user=user,
                    skill=skill,
                    defaults={
                        'proficiency_level': ResumeService._map_confidence_to_proficiency(confidence),
                        'years_of_experience': 0
                    }
                )
                
                # Update proficiency if from resume is higher
                if not created:
                    new_proficiency = ResumeService._map_confidence_to_proficiency(confidence)
                    proficiency_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
                    
                    if proficiency_levels.get(new_proficiency, 0) > proficiency_levels.get(user_skill.proficiency_level, 0):
                        user_skill.proficiency_level = new_proficiency
                        user_skill.save()
            
            except Exception as e:
                logger.warning(f"Error syncing skill {skill_name}: {str(e)}")

    @staticmethod
    def _map_confidence_to_proficiency(confidence):
        """Map ML confidence score to proficiency level."""
        if confidence >= 0.9:
            return 'expert'
        elif confidence >= 0.7:
            return 'advanced'
        elif confidence >= 0.5:
            return 'intermediate'
        else:
            return 'beginner'

    @staticmethod
    def get_resume_analysis(resume_id):
        """
        Get detailed analysis results for a resume.
        
        Args:
            resume_id: Resume ID
        
        Returns:
            Analysis results dict
        """
        resume = Resume.objects.get(id=resume_id)
        return {
            'resume_id': resume.id,
            'extracted_skills': resume.extracted_skills,
            'skill_gaps': resume.skill_gaps,
            'experience_level': resume.experience_level,
            'skill_score': resume.skill_score,
            'total_score': resume.total_score,
            'analyzed_at': resume.analyzed_at.isoformat() if resume.analyzed_at else None,
        }

    @staticmethod
    def compare_resumes(resume_id_1, resume_id_2):
        """
        Compare two resumes and return differences.
        
        Args:
            resume_id_1: First resume ID
            resume_id_2: Second resume ID
        
        Returns:
            Comparison results
        """
        resume1 = Resume.objects.get(id=resume_id_1)
        resume2 = Resume.objects.get(id=resume_id_2)
        
        skills1 = set(resume1.extracted_skills.keys())
        skills2 = set(resume2.extracted_skills.keys())
        
        return {
            'resume1_unique_skills': list(skills1 - skills2),
            'resume2_unique_skills': list(skills2 - skills1),
            'common_skills': list(skills1 & skills2),
            'resume1_score': resume1.total_score,
            'resume2_score': resume2.total_score,
            'score_difference': abs(resume1.total_score - resume2.total_score),
        }

    @staticmethod
    def delete_resume(resume_id):
        """Soft delete a resume."""
        resume = Resume.objects.get(id=resume_id)
        resume.file.delete()
        resume.delete()
        logger.info(f"Resume {resume_id} deleted")
