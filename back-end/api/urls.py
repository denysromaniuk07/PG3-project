from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_new as views

# Create router and register viewsets
router = DefaultRouter()

# User Management
router.register(r'users', views.UserViewSet, basename='user')

# Skills Management
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'user-skills', views.UserSkillViewSet, basename='user-skill')

# Resume Management
router.register(r'resumes', views.ResumeViewSet, basename='resume')

# Learning System
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'course-modules', views.CourseModuleViewSet, basename='course-module')
router.register(r'course-progress', views.UserCourseProgressViewSet, basename='course-progress')

# Projects
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'project-progress', views.UserProjectProgressViewSet, basename='project-progress')

# Jobs
router.register(r'jobs', views.JobOpportunityViewSet, basename='job')
router.register(r'job-applications', views.JobApplicationViewSet, basename='job-application')

# Community
router.register(r'community/posts', views.CommunityPostViewSet, basename='community-post')
router.register(r'community/comments', views.CommentViewSet, basename='comment')

# Mentorship
router.register(r'mentors', views.MentorViewSet, basename='mentor')
router.register(r'mentor-sessions', views.MentorSessionViewSet, basename='mentor-session')

# Achievements
router.register(r'achievements', views.AchievementViewSet, basename='achievement')
router.register(r'user-achievements', views.UserAchievementViewSet, basename='user-achievement')

urlpatterns = [
    path('', include(router.urls)),
]
