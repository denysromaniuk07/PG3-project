from django_filters import rest_framework as filters
from .models import JobOpportunity, Course, Mentor


class JobOpportunityFilter(filters.FilterSet):
    """Filter for job opportunities"""
    location = filters.CharFilter(lookup_expr='icontains')
    job_type = filters.ChoiceFilter(
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('contract', 'Contract'),
            ('freelance', 'Freelance'),
        ]
    )
    salary_min = filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = filters.NumberFilter(field_name='salary_max', lookup_expr='lte')

    class Meta:
        model = JobOpportunity
        fields = ['location', 'job_type', 'salary_min', 'salary_max']


class CourseFilter(filters.FilterSet):
    """Filter for courses"""
    difficulty = filters.ChoiceFilter(field_name='difficulty_level', choices=Course.DIFFICULTY_CHOICES)
    category = filters.CharFilter(lookup_expr='icontains')
    duration_min = filters.NumberFilter(field_name='estimated_duration', lookup_expr='gte')
    duration_max = filters.NumberFilter(field_name='estimated_duration', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['difficulty_level', 'category']


class MentorFilter(filters.FilterSet):
    """Filter for mentors"""
    hourly_rate_min = filters.NumberFilter(field_name='hourly_rate', lookup_expr='gte')
    hourly_rate_max = filters.NumberFilter(field_name='hourly_rate', lookup_expr='lte')
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    years_min = filters.NumberFilter(field_name='years_of_experience', lookup_expr='gte')

    class Meta:
        model = Mentor
        fields = ['hourly_rate_min', 'hourly_rate_max', 'rating_min', 'years_min']
