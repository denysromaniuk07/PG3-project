from django.db import models
from django.contrib.auth.models import User


class OnboardingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding Profile - {self.user.username}"
