from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .models import OnboardingProfile
from .serializers import OnboardingProfileSerializer


ALLOWED_CV_EXTENSIONS = ['pdf', 'doc', 'docx']
MAX_CV_SIZE = 5 * 1024 * 1024  # 5MB


class CVUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if 'cv' not in request.FILES:
            return Response(
                {"error": "No CV file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cv_file = request.FILES['cv']

        if cv_file.size > MAX_CV_SIZE:
            return Response(
                {"error": f"File size exceeds 5MB limit"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_extension = cv_file.name.split('.')[-1].lower()
        if file_extension not in ALLOWED_CV_EXTENSIONS:
            return Response(
                {"error": f"Only {', '.join(ALLOWED_CV_EXTENSIONS)} files are allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            profile, created = OnboardingProfile.objects.get_or_create(user=request.user)
            profile.cv = cv_file
            profile.save()

            serializer = OnboardingProfileSerializer(profile)
            return Response(
                {
                    "message": "CV uploaded successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """Retrieve user's CV and onboarding profile"""
        try:
            profile = OnboardingProfile.objects.get(user=request.user)
            serializer = OnboardingProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OnboardingProfile.DoesNotExist:
            return Response(
                {"error": "Onboarding profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        """Delete user's CV"""
        try:
            profile = OnboardingProfile.objects.get(user=request.user)
            if profile.cv:
                profile.cv.delete()
                profile.save()
            return Response(
                {"message": "CV deleted successfully"},
                status=status.HTTP_200_OK
            )
        except OnboardingProfile.DoesNotExist:
            return Response(
                {"error": "Onboarding profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
