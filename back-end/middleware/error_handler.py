"""
Error handling and exception middleware.
Catches exceptions, logs them, and returns proper error responses.
"""

import logging
import traceback
import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(MiddlewareMixin):
    """
    Catches unhandled exceptions and returns proper error responses.
    Logs all exceptions for debugging and monitoring.
    
    Usage: Add 'middleware.error_handler.ExceptionHandlerMiddleware' to MIDDLEWARE
    """

    def process_exception(self, request, exception):
        """Handle exceptions and return JSON error responses."""
        
        # Log exception with traceback
        logger.error(
            f"Exception in {request.method} {request.path}",
            exc_info=True,
            extra={
                'user': request.user.username if request.user.is_authenticated else 'Anonymous',
                'ip_address': self.get_client_ip(request),
            }
        )
        
        # Determine response based on exception type
        if isinstance(exception, Http404):
            return self._handle_404(exception)
        elif isinstance(exception, PermissionDenied):
            return self._handle_permission_denied(exception)
        elif isinstance(exception, (ValidationError, DRFValidationError)):
            return self._handle_validation_error(exception)
        elif isinstance(exception, APIException):
            return self._handle_api_exception(exception)
        else:
            return self._handle_generic_exception(exception)

    @staticmethod
    def _handle_404(exception):
        """Handle 404 Not Found exceptions."""
        return JsonResponse({
            'error': 'Not Found',
            'detail': 'The requested resource was not found.',
            'status': 404,
        }, status=404)

    @staticmethod
    def _handle_permission_denied(exception):
        """Handle permission denied exceptions."""
        return JsonResponse({
            'error': 'Permission Denied',
            'detail': str(exception.message) if hasattr(exception, 'message') else 'You do not have permission to perform this action.',
            'status': 403,
        }, status=403)

    @staticmethod
    def _handle_validation_error(exception):
        """Handle validation error exceptions."""
        error_dict = {}
        
        if isinstance(exception, DRFValidationError):
            if isinstance(exception.detail, dict):
                error_dict = exception.detail
            else:
                error_dict = {'error': str(exception.detail)}
        else:
            error_dict = {'error': str(exception)}
        
        return JsonResponse({
            'error': 'Validation Error',
            'detail': 'One or more fields contain invalid values.',
            'field_errors': error_dict,
            'status': 400,
        }, status=400)

    @staticmethod
    def _handle_api_exception(exception):
        """Handle DRF API exceptions."""
        return JsonResponse({
            'error': exception.default_detail,
            'detail': str(exception.detail) if hasattr(exception, 'detail') else str(exception),
            'status': exception.status_code,
        }, status=exception.status_code)

    @staticmethod
    def _handle_generic_exception(exception):
        """Handle generic unhandled exceptions."""
        import os
        
        # Only expose detailed errors in debug mode
        if os.environ.get('DEBUG', 'True') == 'True':
            error_detail = f"{exception.__class__.__name__}: {str(exception)}"
            traceback_info = traceback.format_exc()
        else:
            error_detail = "An internal server error occurred."
            traceback_info = None
        
        response_data = {
            'error': 'Internal Server Error',
            'detail': error_detail,
            'status': 500,
        }
        
        if traceback_info:
            response_data['traceback'] = traceback_info
        
        return JsonResponse(response_data, status=500)

    @staticmethod
    def get_client_ip(request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Adds security headers to all responses.
    Helps protect against common web vulnerabilities.
    
    Usage: Add 'middleware.error_handler.SecurityHeadersMiddleware' to MIDDLEWARE
    """

    def process_response(self, request, response):
        """Add security headers to response."""
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions policy (formerly Feature-Policy)
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy (basic)
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        
        # Strict Transport Security (only in production)
        if not self._is_development():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

    @staticmethod
    def _is_development():
        """Check if running in development mode."""
        import os
        return os.environ.get('DEBUG', 'True') == 'True'


class RequestResponseLoggingMiddleware(MiddlewareMixin):
    """
    Logs all HTTP requests and responses.
    Useful for debugging, monitoring, and audit trails.
    
    Usage: Add 'middleware.error_handler.RequestResponseLoggingMiddleware' to MIDDLEWARE
    """

    def process_request(self, request):
        """Log incoming request."""
        request._start_time = self._get_time()
        
        logger.info(
            f"Request: {request.method} {request.path}",
            extra={
                'method': request.method,
                'path': request.path,
                'ip_address': ExceptionHandlerMiddleware.get_client_ip(request),
                'user': request.user.username if request.user.is_authenticated else 'Anonymous',
                'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
            }
        )
        
        return None

    def process_response(self, request, response):
        """Log response with duration."""
        
        if hasattr(request, '_start_time'):
            duration = (self._get_time() - request._start_time) * 1000  # Convert to ms
        else:
            duration = None
        
        logger.info(
            f"Response: {request.method} {request.path} - {response.status_code}",
            extra={
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': f"{duration:.2f}" if duration else "Unknown",
                'ip_address': ExceptionHandlerMiddleware.get_client_ip(request),
                'user': request.user.username if request.user.is_authenticated else 'Anonymous',
            }
        )
        
        return response

    @staticmethod
    def _get_time():
        """Get current time for performance measurement."""
        import time
        return time.time()
