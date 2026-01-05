"""
Analytics and tracking middleware.
Tracks user activity, API usage, and performance metrics.
"""

import logging
import time
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class AnalyticsMiddleware(MiddlewareMixin):
    """
    Tracks user activity and generates analytics data.
    Records: page views, API calls, user behavior.
    
    Usage: Add 'middleware.analytics_middleware.AnalyticsMiddleware' to MIDDLEWARE
    """

    def process_request(self, request):
        """Track incoming request."""
        request._analytics_start_time = time.time()
        request._analytics_path = request.path
        request._analytics_method = request.method
        
        # Track API usage
        if request.path.startswith('/api/'):
            self._track_api_usage(request)
        
        return None

    def process_response(self, request, response):
        """Track response and record analytics."""
        
        if hasattr(request, '_analytics_start_time'):
            duration = time.time() - request._analytics_start_time
            
            # Track response time
            if request.path.startswith('/api/'):
                self._track_response_time(request, duration)
            
            # Track errors
            if response.status_code >= 400:
                self._track_error(request, response.status_code)
        
        return response

    @staticmethod
    def _track_api_usage(request):
        """Track API endpoint usage."""
        cache_key = f"api_usage:{request.method}:{request.path}"
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1, timeout=3600)  # 1 hour

    @staticmethod
    def _track_response_time(request, duration):
        """Track endpoint response times."""
        cache_key = f"response_time:{request.method}:{request.path}"
        durations = cache.get(cache_key, [])
        durations.append(duration)
        
        # Keep only last 100 measurements
        if len(durations) > 100:
            durations = durations[-100:]
        
        cache.set(cache_key, durations, timeout=3600)

    @staticmethod
    def _track_error(request, status_code):
        """Track API errors."""
        cache_key = f"api_errors:{status_code}:{request.path}"
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1, timeout=3600)


class UserActivityMiddleware(MiddlewareMixin):
    """
    Tracks user activity for profile stats and achievements.
    Records: logins, posts, comments, etc.
    
    Usage: Add 'middleware.analytics_middleware.UserActivityMiddleware' to MIDDLEWARE
    """

    def process_response(self, request, response):
        """Track user activity."""
        
        if not request.user.is_authenticated:
            return response
        
        # Track successful API calls
        if response.status_code < 400 and request.path.startswith('/api/'):
            self._track_user_action(request)
        
        # Track last activity time
        self._update_last_activity(request)
        
        return response

    @staticmethod
    def _track_user_action(request):
        """Track user actions for analytics."""
        action = {
            'user_id': request.user.id,
            'action_type': request.method,
            'endpoint': request.path,
            'timestamp': timezone.now().isoformat(),
        }
        
        cache_key = f"user_actions:{request.user.id}"
        actions = cache.get(cache_key, [])
        actions.append(action)
        
        # Keep only last 50 actions
        if len(actions) > 50:
            actions = actions[-50:]
        
        cache.set(cache_key, actions, timeout=86400)  # 24 hours

    @staticmethod
    def _update_last_activity(request):
        """Update user's last activity timestamp in cache."""
        cache_key = f"user_last_activity:{request.user.id}"
        cache.set(cache_key, timezone.now(), timeout=86400)


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """
    Monitors application performance and logs slow requests.
    Alerts on performance degradation.
    
    Usage: Add 'middleware.analytics_middleware.PerformanceMonitoringMiddleware' to MIDDLEWARE
    """

    # Threshold in seconds for slow requests
    SLOW_REQUEST_THRESHOLD = 1.0

    def process_request(self, request):
        """Start performance monitoring."""
        request._performance_start_time = time.time()
        return None

    def process_response(self, request, response):
        """Log performance metrics."""
        
        if hasattr(request, '_performance_start_time'):
            duration = time.time() - request._performance_start_time
            
            if duration > self.SLOW_REQUEST_THRESHOLD:
                logger.warning(
                    f"Slow request detected: {request.method} {request.path} took {duration:.2f}s",
                    extra={
                        'method': request.method,
                        'path': request.path,
                        'duration_seconds': duration,
                        'status_code': response.status_code,
                        'user': request.user.username if request.user.is_authenticated else 'Anonymous',
                    }
                )
            
            # Add performance headers
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response
