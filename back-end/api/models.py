from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Extended User Model
class User(AbstractUser):
    """Extended user model with career platform fields"""
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


# Skill Model
class Skill(models.Model):
    """Skills that users can have"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('frontend', 'Frontend'),
            ('backend', 'Backend'),
            ('fullstack', 'Full Stack'),
            ('mobile', 'Mobile'),
            ('data', 'Data Science'),
            ('devops', 'DevOps'),
            ('soft', 'Soft Skills'),
        ],
        default='frontend'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# User Skill Proficiency
class UserSkill(models.Model):
    """Track user's skill proficiency"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    endorsed_by_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['-proficiency_level']

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


# Course Model
class Course(models.Model):
    """Learning courses"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    estimated_duration = models.IntegerField(help_text='Duration in hours')
    color_gradient = models.CharField(max_length=100, default='from-indigo-500 to-purple-500')
    thumbnail = models.ImageField(upload_to='courses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# Course Module Model
class CourseModule(models.Model):
    """Modules within courses"""
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('exercise', 'Exercise'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    order = models.IntegerField()
    duration = models.IntegerField(help_text='Duration in minutes')
    video_url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# User Course Progress
class UserCourseProgress(models.Model):
    """Track user progress in courses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    completed_modules = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


# Module Completion Tracking
class ModuleCompletion(models.Model):
    """Track individual module completions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_completions')
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"


# Project Model
class Project(models.Model):
    """Coding projects"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('locked', 'Locked'),
    ]
    
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('fullstack', 'Full Stack'),
        ('ml', 'Machine Learning'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    icon_emoji = models.CharField(max_length=10, default='📁')
    color_gradient = models.CharField(max_length=100, default='from-blue-500 to-cyan-500')
    thumbnail = models.ImageField(upload_to='projects/', null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    unlock_requirements = models.TextField(blank=True, help_text='JSON or text description of requirements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# User Project Progress
class UserProjectProgress(models.Model):
    """Track user progress in projects"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_progress')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='not_started'
    )
    progress = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    submission_url = models.URLField(blank=True, help_text='GitHub repo or demo link')

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"


# Achievement/Badge Model
class Achievement(models.Model):
    """Achievements and badges"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')
    points_value = models.IntegerField(default=10)
    unlock_condition = models.TextField(help_text='Condition to unlock this achievement')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-points_value']

    def __str__(self):
        return self.title


# User Achievement
class UserAchievement(models.Model):
    """Track user achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"


# Job Opportunity Model
class JobOpportunity(models.Model):
    """Job postings"""
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('contract', 'Contract'),
            ('freelance', 'Freelance'),
        ],
        default='full_time'
    )
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    required_skills = models.ManyToManyField(Skill, related_name='job_opportunities')
    job_url = models.URLField()
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


# User Job Application
class JobApplication(models.Model):
    """Track user job applications"""
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title}"


# Community Post Model
class CommunityPost(models.Model):
    """Community discussion posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    title = models.CharField(max_length=300)
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# Post Tag Model
class PostTag(models.Model):
    """Tags for community posts"""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Post-Tag Relationship
class CommunityPostTag(models.Model):
    """M2M relationship between posts and tags"""
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(PostTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')


# Post Like Model
class PostLike(models.Model):
    """Track post likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


# Comment Model
class Comment(models.Model):
    """Comments on community posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


# Mentor Model
class Mentor(models.Model):
    """User profile for mentors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField()
    specializations = models.ManyToManyField(Skill, related_name='mentors')
    hourly_rate = models.IntegerField(null=True, blank=True)
    availability = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField()
    verified = models.BooleanField(default=False)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=5.0
    )
    total_mentees = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentor: {self.user.username}"


# Resume Model
class Resume(models.Model):
    """User resume"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume - {self.user.username}"


# Resume Analysis Model
class ResumeAnalysis(models.Model):
    """Analysis of user resume"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume_analysis')
    extracted_skills = models.JSONField(default=list, blank=True)
    skill_gaps = models.JSONField(default=list, blank=True)
    recommendations = models.TextField(blank=True)
    overall_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    analyzed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume Analysis - {self.user.username}"


# Post Model (Original - kept for reference)
class Post(models.Model):
    """Generic posts (deprecated - use CommunityPost instead)"""
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title