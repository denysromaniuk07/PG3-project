from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class URLValidator:
    """Custom URL validator with specific protocol support"""
    
    def __init__(self, protocols=None, message=None):
        self.protocols = protocols or ['http', 'https']
        self.message = message or _('Enter a valid URL.')

    def __call__(self, value):
        if not value:
            return
        
        url_pattern = r'^(' + '|'.join(self.protocols) + r')://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, value, re.IGNORECASE):
            raise ValidationError(self.message)


class SkillNameValidator:
    """Validator for skill names - alphanumeric and spaces only"""
    
    def __init__(self, message=None):
        self.message = message or _('Skill names can only contain letters, numbers, and spaces.')

    def __call__(self, value):
        if not re.match(r'^[a-zA-Z0-9\s\-\.]+$', value):
            raise ValidationError(self.message)


class UsernameValidator:
    """Strict username validator"""
    
    def __init__(self, message=None):
        self.message = message or _('Username can only contain letters, numbers, underscores, and hyphens.')

    def __call__(self, value):
        if len(value) < 3:
            raise ValidationError(_('Username must be at least 3 characters long.'))
        if len(value) > 30:
            raise ValidationError(_('Username must not exceed 30 characters.'))
        if not re.match(r'^[a-zA-Z0-9_\-]+$', value):
            raise ValidationError(self.message)


class ProficiencyLevelValidator:
    """Validator for skill proficiency levels"""
    VALID_LEVELS = ['beginner', 'intermediate', 'advanced', 'expert']
    
    def __init__(self, message=None):
        self.message = message or _(f'Proficiency level must be one of: {", ".join(self.VALID_LEVELS)}')

    def __call__(self, value):
        if value.lower() not in self.VALID_LEVELS:
            raise ValidationError(self.message)


class MinimumScoreValidator:
    """Validator to ensure a score meets minimum requirement"""
    
    def __init__(self, min_score, message=None):
        self.min_score = min_score
        self.message = message or _(f'Score must be at least {min_score}.')

    def __call__(self, value):
        if value < self.min_score:
            raise ValidationError(self.message)


class MaximumScoreValidator:
    """Validator to ensure a score doesn't exceed maximum"""
    
    def __init__(self, max_score, message=None):
        self.max_score = max_score
        self.message = message or _(f'Score cannot exceed {max_score}.')

    def __call__(self, value):
        if value > self.max_score:
            raise ValidationError(self.message)


class FileTypeValidator:
    """Validator for allowed file types"""
    
    def __init__(self, allowed_types, message=None):
        self.allowed_types = allowed_types
        self.message = message or _(f'File type must be one of: {", ".join(allowed_types)}')

    def __call__(self, file):
        if not file:
            return
        
        file_ext = file.name.split('.')[-1].lower()
        if file_ext not in self.allowed_types:
            raise ValidationError(self.message)


class FileSizeValidator:
    """Validator for file size limits"""
    
    def __init__(self, max_size_mb, message=None):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.message = message or _(f'File size must not exceed {max_size_mb}MB.')

    def __call__(self, file):
        if not file:
            return
        
        if file.size > self.max_size_bytes:
            raise ValidationError(self.message)


class DateRangeValidator:
    """Validator to ensure date ranges are valid"""
    
    def __init__(self, message=None):
        self.message = message or _('End date must be after start date.')

    def __call__(self, value):
        """Expects value to be a dict with 'start_date' and 'end_date'"""
        if isinstance(value, dict):
            start = value.get('start_date')
            end = value.get('end_date')
            if start and end and start >= end:
                raise ValidationError(self.message)


class BioLengthValidator:
    """Validator for biography/bio text length"""
    
    def __init__(self, min_length=10, max_length=500, message=None):
        self.min_length = min_length
        self.max_length = max_length
        self.message = message

    def __call__(self, value):
        if not value:
            return
        
        if len(value) < self.min_length:
            raise ValidationError(
                self.message or _(f'Bio must be at least {self.min_length} characters long.')
            )
        if len(value) > self.max_length:
            raise ValidationError(
                self.message or _(f'Bio cannot exceed {self.max_length} characters.')
            )


class EmailDomainValidator:
    """Validator to restrict email domains"""
    
    def __init__(self, allowed_domains=None, blocked_domains=None, message=None):
        self.allowed_domains = allowed_domains
        self.blocked_domains = blocked_domains or []
        self.message = message or _('Email domain is not allowed.')

    def __call__(self, value):
        if not value or '@' not in value:
            return
        
        domain = value.split('@')[1].lower()
        
        if self.allowed_domains and domain not in self.allowed_domains:
            raise ValidationError(self.message)
        
        if domain in self.blocked_domains:
            raise ValidationError(self.message)


class SlugValidator:
    """Validator for slug fields (URL-friendly strings)"""
    
    def __init__(self, message=None):
        self.message = message or _('Slug can only contain letters, numbers, hyphens, and underscores.')

    def __call__(self, value):
        if not re.match(r'^[a-zA-Z0-9_\-]+$', value):
            raise ValidationError(self.message)


class JSONValidator:
    """Validator for JSON field content"""
    
    def __init__(self, schema=None, message=None):
        self.schema = schema
        self.message = message or _('Invalid JSON format.')

    def __call__(self, value):
        if not isinstance(value, dict):
            raise ValidationError(self.message)
        
        # Optional schema validation
        if self.schema:
            self._validate_schema(value, self.schema)

    def _validate_schema(self, value, schema):
        """Validate value against schema"""
        # Implement simple schema validation
        for key, expected_type in schema.items():
            if key in value:
                if not isinstance(value[key], expected_type):
                    raise ValidationError(
                        _(f'Field "{key}" must be of type {expected_type.__name__}.')
                    )
