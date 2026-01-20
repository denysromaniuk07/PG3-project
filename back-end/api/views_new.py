from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import timedelta

from .models import (
    User, Skill, UserSkill, Resume, Course, CourseModule, UserCourseProgress,
    Project, UserProjectProgress, JobOpportunity, JobApplication,
    CommunityPost, Comment, Mentor, Achievement, UserAchievement
)
from .serializers import (
    UserSerializer, SkillSerializer, UserSkillSerializer, ResumeSerializer,
    CourseSerializer, CourseModuleSerializer, UserCourseProgressSerializer,
    ProjectSerializer, UserProjectProgressSerializer, JobOpportunitySerializer,
    JobApplicationSerializer, CommunityPostSerializer, CommentSerializer,
    MentorSerializer, AchievementSerializer,
    UserAchievementSerializer
)
from .permissions import IsOwner, IsMentor, IsAuthorOrReadOnly
from .filters import JobOpportunityFilter, CourseFilter, MentorFilter
from .ml_utils import analyze_resume


# ==================== PAGINATION ====================
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ==================== USER MANAGEMENT ====================
class UserViewSet(viewsets.ModelViewSet):
    """
    User management endpoints:
    - List all users
    - Retrieve user profile
    - Update user profile
    - Get user skills, achievements, statistics
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'title', 'location']
    ordering_fields = ['points', 'created_at']
    ordering = ['-points']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def skills(self, request, pk=None):
        """Get user's skills"""
        user = self.get_object()
        skills = user.skills.all()
        serializer = UserSkillSerializer(skills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def achievements(self, request, pk=None):
        """Get user's achievements"""
        user = self.get_object()
        achievements = user.achievements.all()
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user statistics and analytics"""
        user = self.get_object()
        stats = {
            'total_points': user.points,
            'total_skills': user.skills.count(),
            'total_achievements': user.achievements.count(),
            'courses_completed': user.course_progress.filter(status='completed').count(),
            'projects_completed': user.project_progress.filter(status='completed').count(),
            'job_applications': user.job_applications.count(),
            'community_posts': user.community_posts.count(),
            'is_mentor': user.is_mentor,
        }
        return Response(stats)

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get top users by points"""
        top_users = User.objects.order_by('-points')[:100]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)


# ==================== SKILLS MANAGEMENT ====================
class SkillViewSet(viewsets.ModelViewSet):
    """Predefined skills database"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']


class UserSkillViewSet(viewsets.ModelViewSet):
    """
    User skill management:
    - Add/remove skills from user profile
    - Update skill proficiency levels
    - Endorse user skills
    """
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.skills.all()
        return UserSkill.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def endorse(self, request, pk=None):
        """Endorse a user's skill"""
        user_skill = self.get_object()
        user_skill.endorsements_count += 1
        user_skill.save()
        serializer = self.get_serializer(user_skill)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def gaps(self, request):
        """Get skill gaps analysis for user"""
        user = request.user
        user_skills = user.skills.values_list('skill__name', flat=True)
        # Find recommended skills not yet learned
        all_skills = Skill.objects.exclude(name__in=user_skills)
        serializer = SkillSerializer(all_skills[:10], many=True)
        return Response(serializer.data)


# ==================== RESUME MANAGEMENT ====================
class ResumeViewSet(viewsets.ModelViewSet):
    """
    Resume management with ML analysis:
    - Upload and analyze resumes
    - View analysis results
    - Track resume history
    """
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        # Trigger ML analysis
        try:
            analysis_result = analyze_resume(resume.file)
            resume.extracted_text = analysis_result.get('extracted_text')
            resume.extracted_skills = analysis_result.get('skills', {})
            resume.skill_gaps = analysis_result.get('skill_gaps', [])
            resume.experience_level = analysis_result.get('experience_level')
            resume.skill_score = analysis_result.get('skill_score', 0)
            resume.total_score = int(analysis_result.get('total_score', 0))
            resume.analyzed_at = timezone.now()
            resume.save()
        except Exception as e:
            # Log error but don't fail
            pass

    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        """Get detailed resume analysis"""
        resume = self.get_object()
        return Response({
            'skills': resume.extracted_skills,
            'skill_gaps': resume.skill_gaps,
            'experience_level': resume.experience_level,
            'skill_score': resume.skill_score,
            'total_score': resume.total_score,
            'analyzed_at': resume.analyzed_at,
        })


# ==================== LEARNING SYSTEM ====================
class CourseViewSet(viewsets.ModelViewSet):
    """Course management with filtering and progress tracking"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['created_at', 'estimated_duration']
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        """Get course modules"""
        course = self.get_object()
        modules = course.modules.all().order_by('order')
        serializer = CourseModuleSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll user in course"""
        course = self.get_object()
        progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'progress': 0}
        )
        serializer = UserCourseProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get user's progress in course"""
        course = self.get_object()
        progress = get_object_or_404(UserCourseProgress, user=request.user, course=course)
        serializer = UserCourseProgressSerializer(progress)
        return Response(serializer.data)


class CourseModuleViewSet(viewsets.ReadOnlyModelViewSet):
    """Course module content"""
    serializer_class = CourseModuleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        if course_id:
            return CourseModule.objects.filter(course_id=course_id).order_by('order')
        return CourseModule.objects.all()


class UserCourseProgressViewSet(viewsets.ModelViewSet):
    """User course progress tracking"""
    serializer_class = UserCourseProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCourseProgress.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_module_complete(self, request, pk=None):
        """Mark a module as completed"""
        progress = self.get_object()
        module_id = request.data.get('module_id')
        
        module = get_object_or_404(CourseModule, id=module_id, course=progress.course)
        progress.completed_modules += 1
        total_modules = progress.course.modules.count()
        progress.progress = int((progress.completed_modules / total_modules) * 100)
        
        if progress.progress >= 100:
            progress.completed_at = timezone.now()
        
        progress.save()
        serializer = self.get_serializer(progress)
        return Response(serializer.data)


# ==================== PROJECTS SYSTEM ====================
class ProjectViewSet(viewsets.ModelViewSet):
    """Coding projects management"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty_level']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start working on a project"""
        project = self.get_object()
        progress, created = UserProjectProgress.objects.get_or_create(
            user=request.user,
            project=project,
            defaults={'status': 'in_progress'}
        )
        serializer = UserProjectProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get project submissions leaderboard"""
        project = self.get_object()
        submissions = UserProjectProgress.objects.filter(
            project=project,
            status__in=['in_progress', 'completed']
        ).order_by('-progress')[:50]
        serializer = UserProjectProgressSerializer(submissions, many=True)
        return Response(serializer.data)


class UserProjectProgressViewSet(viewsets.ModelViewSet):
    """User project progress and submissions"""
    serializer_class = UserProjectProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProjectProgress.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit project for review"""
        progress = self.get_object()
        progress.status = 'completed'
        progress.completed_at = timezone.now()
        progress.submission_url = request.data.get('submission_url', progress.submission_url)
        progress.save()
        serializer = self.get_serializer(progress)
        return Response(serializer.data)


# ==================== JOB OPPORTUNITIES ====================
class JobOpportunityViewSet(viewsets.ModelViewSet):
    """Job listings with skill matching"""
    queryset = JobOpportunity.objects.filter(expires_at__gte=timezone.now()).order_by('-posted_date')
    serializer_class = JobOpportunitySerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobOpportunityFilter
    search_fields = ['job_title', 'company_name', 'description', 'location']
    ordering_fields = ['posted_date', 'salary_min', 'salary_max']

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Apply for a job"""
        job = self.get_object()
        application, created = JobApplication.objects.get_or_create(
            user=request.user,
            job=job,
            defaults={'cover_letter': request.data.get('cover_letter', '')}
        )
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def matching(self, request):
        """Get recommended jobs based on user skills"""
        user = request.user
        user_skill_ids = user.skills.values_list('skill_id', flat=True)
        matching_jobs = JobOpportunity.objects.filter(
            required_skills__in=user_skill_ids,
            expires_at__gte=timezone.now()
        ).distinct().order_by('-posted_date')[:20]
        serializer = self.get_serializer(matching_jobs, many=True)
        return Response(serializer.data)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """Job application tracking"""
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update application status"""
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
        serializer = self.get_serializer(application)
        return Response(serializer.data)


# ==================== COMMUNITY ====================
class CommunityPostViewSet(viewsets.ModelViewSet):
    """Community discussion posts"""
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        post.likes_count += 1
        post.save()
        return Response({'likes_count': post.likes_count})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get post comments"""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending posts"""
        week_ago = timezone.now() - timedelta(days=7)
        trending = CommunityPost.objects.filter(
            created_at__gte=week_ago
        ).order_by('-likes_count', '-comments_count')[:20]
        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """Post comments"""
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id).order_by('created_at')
        return Comment.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = get_object_or_404(CommunityPost, id=post_id)
        comment = serializer.save(user=self.request.user, post=post)
        post.comments_count += 1
        post.save()


# ==================== MENTORSHIP ====================
class MentorViewSet(viewsets.ModelViewSet):
    """Mentor profiles and management"""
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MentorFilter
    search_fields = ['user__first_name', 'user__last_name', 'specializations', 'bio']
    ordering_fields = ['rating', 'hourly_rate', 'years_of_experience']
    ordering = ['-rating']

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get mentor reviews"""
        # TODO: Implement mentor reviews once MentorSession is implemented
        return Response([])


# ==================== ACHIEVEMENTS ====================
class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """Available achievements and badges"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rarity']


class UserAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """User earned achievements"""
    serializer_class = UserAchievementSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id:
            return UserAchievement.objects.filter(user_id=user_id)
        return UserAchievement.objects.all()
