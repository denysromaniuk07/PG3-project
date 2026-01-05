"""
Django middleware components.

This package provides middleware for authentication, error handling,
analytics, and rate limiting.

Usage in settings.py:
MIDDLEWARE = [
    # ... standard Django middleware ...
    'middleware.auth_middleware.JWTAuthenticationMiddleware',
    'middleware.auth_middleware.UserContextMiddleware',
    'middleware.error_handler.ExceptionHandlerMiddleware',
    'middleware.error_handler.SecurityHeadersMiddleware',
    'middleware.error_handler.RequestResponseLoggingMiddleware',
    'middleware.analytics_middleware.AnalyticsMiddleware',
    'middleware.analytics_middleware.UserActivityMiddleware',
    'middleware.analytics_middleware.PerformanceMonitoringMiddleware',
    'middleware.rate_limiting_middleware.RateLimitMiddleware',
    'middleware.rate_limiting_middleware.IPWhitelistMiddleware',
]
"""

# Import all middleware components
from .auth_middleware import (
    JWTAuthenticationMiddleware,
    UserContextMiddleware,
    TokenBlacklistMiddleware,
)

from .error_handler import (
    ExceptionHandlerMiddleware,
    SecurityHeadersMiddleware,
    RequestResponseLoggingMiddleware,
)

from .analytics_middleware import (
    AnalyticsMiddleware,
    UserActivityMiddleware,
    PerformanceMonitoringMiddleware,
)

from .rate_limiting_middleware import (
    RateLimitMiddleware,
    IPWhitelistMiddleware,
)

__all__ = [
    # Authentication
    'JWTAuthenticationMiddleware',
    'UserContextMiddleware',
    'TokenBlacklistMiddleware',
    # Error Handling
    'ExceptionHandlerMiddleware',
    'SecurityHeadersMiddleware',
    'RequestResponseLoggingMiddleware',
    # Analytics
    'AnalyticsMiddleware',
    'UserActivityMiddleware',
    'PerformanceMonitoringMiddleware',
    # Rate Limiting
    'RateLimitMiddleware',
    'IPWhitelistMiddleware',
]
