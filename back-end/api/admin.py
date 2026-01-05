from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Skill, UserSkill, Resume, Course, CourseModule, UserCourseProgress,
    Project, UserProjectProgress, JobOpportunity, JobApplication,
    CommunityPost, Comment, Mentor, MentorSession, Achievement, UserAchievement
)


# ==================== USER ADMIN ====================
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Career Profile', {
            'fields': ('title', 'location', 'bio', 'profile_picture', 'website', 
                      'github_url', 'linkedin_url', 'twitter_url')
        }),
        ('Settings', {
            'fields': ('points', 'is_mentor', 'is_premium')
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'title', 'points', 'is_mentor']
    list_filter = BaseUserAdmin.list_filter + ('is_mentor', 'is_premium', 'created_at')
    search_fields = ['username', 'email', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)


# ==================== SKILLS ====================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'endorsements_count']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['user__username', 'skill__name']


# ==================== RESUME ====================
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'file_type', 'uploaded_at', 'analyzed_at', 'total_score']
    list_filter = ['file_type', 'uploaded_at', 'experience_level']
    search_fields = ['user__username']
    readonly_fields = ['extracted_text', 'extracted_skills', 'skill_gaps', 'total_score']


# ==================== COURSES ====================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'category', 'total_students', 'rating']
    list_filter = ['difficulty', 'category', 'created_at']
    search_fields = ['title', 'description']


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'duration_minutes']
    list_filter = ['content_type', 'course']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'progress_percentage', 'completed_at']
    list_filter = ['status', 'started_at', 'completed_at']
    search_fields = ['user__username', 'course__title']


# ==================== PROJECTS ====================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'estimated_hours', 'total_submissions', 'average_rating']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['title', 'description']


@admin.register(UserProjectProgress)
class UserProjectProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'status', 'rating', 'submitted_at']
    list_filter = ['status', 'started_at', 'submitted_at']
    search_fields = ['user__username', 'project__title']


# ==================== JOBS ====================
@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'job_type', 'experience_level', 'posted_at']
    list_filter = ['job_type', 'experience_level', 'posted_at', 'deadline']
    search_fields = ['title', 'company_name', 'location']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'applied_at', 'updated_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__username', 'job__title']


# ==================== COMMUNITY ====================
@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['created_at', 'likes_count']
    search_fields = ['title', 'content', 'author__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'likes_count']
    list_filter = ['created_at', 'likes_count']
    search_fields = ['content', 'author__username']


# ==================== MENTORSHIP ====================
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_mentees', 'rating', 'hourly_rate', 'created_at']
    list_filter = ['rating', 'years_of_experience']
    search_fields = ['user__username', 'user__first_name', 'specializations']


@admin.register(MentorSession)
class MentorSessionAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentee', 'status', 'scheduled_date', 'completed_at']
    list_filter = ['status', 'requested_at', 'completed_at']
    search_fields = ['mentor__user__username', 'mentee__username']


# ==================== ACHIEVEMENTS ====================
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'rarity', 'points_awarded', 'created_at']
    list_filter = ['rarity', 'created_at']
    search_fields = ['name', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['earned_at', 'achievement__rarity']
    search_fields = ['user__username', 'achievement__name']
