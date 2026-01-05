"""
Rate limiting and throttling middleware.
Prevents abuse by limiting request rates per user/IP.
"""

import logging
import time
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone

logger = logging.getLogger(__name__)


class RateLimitMiddleware(MiddlewareMixin):
    """
    Implements rate limiting per user and per IP.
    Prevents API abuse and ensures fair resource usage.
    
    Usage: Add 'middleware.rate_limiting_middleware.RateLimitMiddleware' to MIDDLEWARE
    
    Configuration in settings.py:
    RATE_LIMIT_SETTINGS = {
        'AUTHENTICATED_REQUESTS_PER_HOUR': 1000,
        'ANONYMOUS_REQUESTS_PER_HOUR': 100,
        'BURST_SIZE': 20,  # Allow 20 requests per minute
        'BURST_WINDOW': 60,  # Per minute
    }
    """

    # Default rate limits
    AUTHENTICATED_REQUESTS_PER_HOUR = 1000
    ANONYMOUS_REQUESTS_PER_HOUR = 100
    BURST_SIZE = 20  # Requests per burst window
    BURST_WINDOW = 60  # Seconds

    def process_request(self, request):
        """Check rate limits before processing request."""
        
        # Skip rate limiting for static files and admin
        if self._should_skip_rate_limit(request):
            return None
        
        # Get identifier (user ID or IP)
        identifier = self._get_identifier(request)
        
        # Check hourly rate limit
        if not self._check_hourly_limit(request, identifier):
            return self._rate_limit_exceeded_response(request, 'hour')
        
        # Check burst limit
        if not self._check_burst_limit(identifier):
            return self._rate_limit_exceeded_response(request, 'minute')
        
        # Track request
        self._track_request(identifier)
        
        return None

    def process_response(self, request, response):
        """Add rate limit headers to response."""
        identifier = self._get_identifier(request)
        
        # Get current counts
        hourly_key = f"rate_limit:hourly:{identifier}"
        burst_key = f"rate_limit:burst:{identifier}"
        
        hourly_count = cache.get(hourly_key, 0)
        burst_count = cache.get(burst_key, 0)
        
        # Calculate limits
        if request.user.is_authenticated:
            hourly_limit = self.AUTHENTICATED_REQUESTS_PER_HOUR
        else:
            hourly_limit = self.ANONYMOUS_REQUESTS_PER_HOUR
        
        # Add rate limit headers
        response['X-RateLimit-Limit-Hourly'] = str(hourly_limit)
        response['X-RateLimit-Remaining-Hourly'] = str(max(0, hourly_limit - hourly_count))
        response['X-RateLimit-Reset-Hourly'] = str(int(time.time()) + 3600)
        
        response['X-RateLimit-Limit-Burst'] = str(self.BURST_SIZE)
        response['X-RateLimit-Remaining-Burst'] = str(max(0, self.BURST_SIZE - burst_count))
        response['X-RateLimit-Reset-Burst'] = str(int(time.time()) + self.BURST_WINDOW)
        
        return response

    @staticmethod
    def _should_skip_rate_limit(request):
        """Check if request should skip rate limiting."""
        skip_paths = ['/static/', '/media/', '/admin/']
        return any(request.path.startswith(path) for path in skip_paths)

    @staticmethod
    def _get_identifier(request):
        """Get unique identifier for rate limiting."""
        if request.user.is_authenticated:
            return f"user:{request.user.id}"
        else:
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            return f"ip:{ip}"

    def _check_hourly_limit(self, request, identifier):
        """Check if hourly limit is exceeded."""
        cache_key = f"rate_limit:hourly:{identifier}"
        current_count = cache.get(cache_key, 0)
        
        if request.user.is_authenticated:
            limit = self.AUTHENTICATED_REQUESTS_PER_HOUR
        else:
            limit = self.ANONYMOUS_REQUESTS_PER_HOUR
        
        return current_count < limit

    def _check_burst_limit(self, identifier):
        """Check if burst limit is exceeded."""
        cache_key = f"rate_limit:burst:{identifier}"
        current_count = cache.get(cache_key, 0)
        return current_count < self.BURST_SIZE

    @staticmethod
    def _track_request(identifier):
        """Track request for rate limiting."""
        # Track hourly
        hourly_key = f"rate_limit:hourly:{identifier}"
        hourly_count = cache.get(hourly_key, 0)
        cache.set(hourly_key, hourly_count + 1, timeout=3600)
        
        # Track burst
        burst_key = f"rate_limit:burst:{identifier}"
        burst_count = cache.get(burst_key, 0)
        cache.set(burst_key, burst_count + 1, timeout=60)

    @staticmethod
    def _rate_limit_exceeded_response(request, limit_type):
        """Return rate limit exceeded response."""
        identifier = RateLimitMiddleware._get_identifier(request)
        
        logger.warning(
            f"Rate limit exceeded ({limit_type}): {identifier}",
            extra={
                'identifier': identifier,
                'limit_type': limit_type,
                'path': request.path,
                'user': request.user.username if request.user.is_authenticated else 'Anonymous',
            }
        )
        
        return JsonResponse({
            'error': 'Rate Limit Exceeded',
            'detail': f'Too many requests. Please try again later.',
            'limit_type': limit_type,
            'status': 429,
        }, status=429)


class IPWhitelistMiddleware(MiddlewareMixin):
    """
    Allows bypassing rate limits for whitelisted IPs.
    Useful for internal services, monitoring, etc.
    
    Usage: Add 'middleware.rate_limiting_middleware.IPWhitelistMiddleware' to MIDDLEWARE
    
    Configuration in settings.py:
    RATE_LIMIT_WHITELIST = [
        '127.0.0.1',
        '::1',
        '192.168.1.100',
    ]
    """

    def process_request(self, request):
        """Check if IP is whitelisted."""
        from django.conf import settings
        
        whitelist = getattr(settings, 'RATE_LIMIT_WHITELIST', [])
        client_ip = self._get_client_ip(request)
        
        if client_ip in whitelist:
            # Mark request as whitelisted
            request._rate_limit_whitelisted = True
        
        return None

    @staticmethod
    def _get_client_ip(request):
        """Extract client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
