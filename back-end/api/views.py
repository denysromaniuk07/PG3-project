from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resume
from .serializers import ResumeSerializer
from .ml_utils import analyze_resume
import json


@api_view(['POST'])
def upload_resume(request):
    """Handle resume file uploads and initiate analysis"""
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        return Response(
            {'error': 'File is too large (max 5MB)'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    file_ext = '.' + file.name.split('.')[-1].lower()
    if file_ext not in allowed_extensions:
        return Response(
            {'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create resume record
        resume = Resume.objects.create(
            file=file,
            original_filename=file.name,
            file_size=file.size,
            analysis_status='analyzing'
        )
        
        # Perform ML analysis
        analysis_result = analyze_resume(file)
        
        # Map experience level
        exp_level = analysis_result['experience_level'].lower()
        if exp_level == 'entry-level':
            exp_level = 'entry-level'
        elif exp_level == 'junior':
            exp_level = 'junior'
        elif exp_level == 'mid-level':
            exp_level = 'mid-level'
        else:
            exp_level = 'senior'
        
        # Update resume with analysis results
        resume.extracted_text = analysis_result['extracted_text']
        resume.skills = analysis_result['skills']
        resume.skill_gaps = analysis_result['skill_gaps']
        resume.experience_level = exp_level
        resume.skill_score = analysis_result['skill_score']
        resume.total_score = float(analysis_result['total_score'])
        resume.analysis_status = 'completed'
        resume.save()
        
        serializer = ResumeSerializer(resume, context={'request': request})
        return Response(
            {
                'message': 'File uploaded and analyzed successfully',
                'resume': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        # Update resume status to failed
        if 'resume' in locals():
            resume.analysis_status = 'failed'
            resume.save()
        
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_resume_analysis(request, resume_id):
    """Get detailed resume analysis"""
    try:
        resume = Resume.objects.get(id=resume_id)
        serializer = ResumeSerializer(resume, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Resume.DoesNotExist:
        return Response(
            {'error': 'Resume not found'},
            status=status.HTTP_404_NOT_FOUND
        )