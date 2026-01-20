from rest_framework import serializers
from .models import OnboardingProfile


class OnboardingProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    cv_url = serializers.SerializerMethodField()

    class Meta:
        model = OnboardingProfile
        fields = ['id', 'user', 'cv', 'cv_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_cv_url(self, obj):
        if obj.cv:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cv.url)
        return None
