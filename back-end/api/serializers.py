from rest_framework import serializers
from .models import (
    User, Skill, UserSkill, Resume, Course, CourseModule, UserCourseProgress,
    Project, UserProjectProgress, JobOpportunity, JobApplication,
    CommunityPost, Comment, Mentor, MentorSession, Achievement, UserAchievement
)


# ==================== USER SERIALIZERS ====================
class UserSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'title', 
            'location', 'bio', 'profile_picture', 'github_url', 'linkedin_url',
            'twitter_url', 'website', 'points', 'is_mentor', 'is_premium',
            'created_at', 'updated_at', 'skills', 'achievements'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'points']

    def get_skills(self, obj):
        skills = obj.skills.all()[:5]
        return UserSkillSerializer(skills, many=True).data

    def get_achievements(self, obj):
        achievements = obj.achievements.all()[:5]
        return UserAchievementSerializer(achievements, many=True).data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ==================== SKILL SERIALIZERS ====================
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description']


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserSkill
        fields = [
            'id', 'skill', 'skill_id', 'proficiency_level', 
            'years_of_experience', 'endorsements_count', 'last_updated'
        ]
        read_only_fields = ['id', 'endorsements_count', 'last_updated']


# ==================== RESUME SERIALIZERS ====================
class ResumeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id', 'user', 'file', 'file_type', 'extracted_text',
            'extracted_skills', 'skill_gaps', 'experience_level',
            'skill_score', 'total_score', 'uploaded_at', 'analyzed_at'
        ]
        read_only_fields = [
            'id', 'user', 'extracted_text', 'extracted_skills',
            'skill_gaps', 'experience_level', 'skill_score',
            'total_score', 'analyzed_at', 'uploaded_at'
        ]


# ==================== COURSE SERIALIZERS ====================
class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = [
            'id', 'course', 'title', 'description', 'content_type',
            'order', 'content', 'video_url', 'duration_minutes',
            'created_at', 'updated_at'
        ]


class CourseSerializer(serializers.ModelSerializer):
    modules = CourseModuleSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'difficulty', 'category',
            'duration_hours', 'instructor', 'instructor_name', 'thumbnail',
            'total_students', 'rating', 'modules', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_students', 'created_at', 'updated_at']


class UserCourseProgressSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserCourseProgress
        fields = [
            'id', 'course', 'course_id', 'status', 'progress_percentage',
            'modules_completed', 'started_at', 'completed_at'
        ]
        read_only_fields = ['id', 'started_at']


# ==================== PROJECT SERIALIZERS ====================
class ProjectSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    required_skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Skill.objects.all(), source='required_skills'
    )

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'requirements', 'difficulty',
            'required_skills', 'required_skill_ids', 'estimated_hours',
            'total_submissions', 'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_submissions', 'average_rating', 'created_at', 'updated_at']


class UserProjectProgressSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProjectProgress
        fields = [
            'id', 'user', 'project', 'project_id', 'status',
            'submission_url', 'submission_notes', 'rating', 'feedback',
            'started_at', 'submitted_at', 'completed_at'
        ]
        read_only_fields = ['id', 'user', 'started_at']


# ==================== JOB SERIALIZERS ====================
class JobOpportunitySerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    required_skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Skill.objects.all(), source='required_skills'
    )

    class Meta:
        model = JobOpportunity
        fields = [
            'id', 'title', 'description', 'company_name', 'company_logo',
            'location', 'job_type', 'experience_level', 'required_skills',
            'required_skill_ids', 'salary_min', 'salary_max', 'application_url',
            'total_applications', 'posted_at', 'deadline'
        ]
        read_only_fields = ['id', 'total_applications', 'posted_at']


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobOpportunitySerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company_name', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id', 'user', 'job', 'job_id', 'job_title', 'company_name',
            'status', 'cover_letter', 'applied_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'applied_at', 'updated_at']


# ==================== COMMUNITY SERIALIZERS ====================
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'likes_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'likes_count', 'created_at', 'updated_at']


class CommunityPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CommunityPost
        fields = [
            'id', 'author', 'title', 'content', 'tags', 'likes_count',
            'comments_count', 'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'likes_count', 'comments_count', 'created_at', 'updated_at']


# ==================== MENTOR SERIALIZERS ====================
class MentorSessionSerializer(serializers.ModelSerializer):
    mentor = serializers.SerializerMethodField()
    mentee = UserSerializer(read_only=True)

    class Meta:
        model = MentorSession
        fields = [
            'id', 'mentor', 'mentee', 'title', 'description', 'status',
            'scheduled_date', 'duration_minutes', 'rating', 'feedback',
            'requested_at', 'completed_at'
        ]
        read_only_fields = ['id', 'mentee', 'requested_at']

    def get_mentor(self, obj):
        return {
            'id': obj.mentor.user.id,
            'username': obj.mentor.user.username,
            'name': obj.mentor.user.get_full_name(),
            'hourly_rate': str(obj.mentor.hourly_rate)
        }


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    sessions = MentorSessionSerializer(many=True, read_only=True)

    class Meta:
        model = Mentor
        fields = [
            'id', 'user', 'specializations', 'hourly_rate', 'bio',
            'total_mentees', 'rating', 'reviews_count', 'years_of_experience',
            'availability_hours_per_week', 'sessions', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'total_mentees', 'rating', 'reviews_count',
            'created_at', 'updated_at'
        ]


# ==================== ACHIEVEMENT SERIALIZERS ====================
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'icon', 'rarity',
            'points_awarded', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'earned_at']
        read_only_fields = ['id', 'earned_at']


class ResumeSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = [
            'id',
            'original_filename',
            'file_url',
            'file_size',
            'uploaded_at',
            'extracted_text',
            'skills',
            'skill_gaps',
            'experience_level',
            'skill_score',
            'total_score',
            'analysis_status'
        ]
        read_only_fields = ['id', 'uploaded_at', 'extracted_text', 'skills', 'skill_gaps', 'experience_level', 'skill_score', 'total_score', 'analysis_status']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None