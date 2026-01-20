from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Skill, UserSkill, Resume, Course, CourseModule, UserCourseProgress,
    Project, UserProjectProgress, JobOpportunity, JobApplication,
    CommunityPost, Comment, Mentor, Achievement, UserAchievement
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
    list_display = ['user', 'skill', 'proficiency_level', 'endorsed_by_count']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['user__username', 'skill__name']


# ==================== RESUME ====================
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'uploaded_at', 'updated_at']
    list_filter = ['uploaded_at']
    search_fields = ['user__username']
    readonly_fields = ['extracted_text']


# ==================== COURSES ====================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty_level', 'category', 'created_at']
    list_filter = ['difficulty_level', 'category', 'created_at']
    search_fields = ['title', 'description']


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'duration']
    list_filter = ['content_type', 'course']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress', 'completed_at']
    list_filter = ['started_at', 'completed_at']
    search_fields = ['user__username', 'course__title']


# ==================== PROJECTS ====================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty_level', 'category', 'created_at']
    list_filter = ['difficulty_level', 'category', 'created_at']
    search_fields = ['title', 'description']


@admin.register(UserProjectProgress)
class UserProjectProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'status', 'progress', 'started_at']
    list_filter = ['status', 'started_at', 'completed_at']
    search_fields = ['user__username', 'project__title']


# ==================== JOBS ====================
@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company_name', 'job_type', 'posted_date']
    list_filter = ['job_type', 'posted_date', 'expires_at']
    search_fields = ['job_title', 'company_name', 'location']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'applied_at', 'updated_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__username', 'job__job_title']


# ==================== COMMUNITY ====================
@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'content', 'user__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']


# ==================== MENTORSHIP ====================
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'hourly_rate', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'specializations']


# ==================== ACHIEVEMENTS ====================
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'points_value', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_date']
    list_filter = ['earned_date']
    search_fields = ['user__username', 'achievement__title']
