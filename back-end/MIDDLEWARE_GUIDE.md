# Middleware Documentation

## Overview

The backend implements a comprehensive middleware stack for authentication, error handling, analytics, and rate limiting. All middleware is located in the `middleware/` directory.

---

## Middleware Components

### 1. Authentication Middleware (`auth_middleware.py`)

#### JWTAuthenticationMiddleware

Validates JWT tokens from the Authorization header and sets authenticated user on request.

**Features:**

- JWT token extraction from `Authorization: Bearer <token>` header
- Token validation and user lookup
- Automatic user assignment to request object
- Logging of authentication attempts

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.auth_middleware.JWTAuthenticationMiddleware',
]
```

**How it works:**

1. Extracts token from request header
2. Validates token signature and expiration
3. Retrieves user from database
4. Sets `request.user` to authenticated user or AnonymousUser

#### UserContextMiddleware

Enriches request with user context data (permissions, profile info, stats).

**Features:**

- User context data in `request.user_context`
- Includes: is_authenticated, user_id, username, is_staff, is_superuser
- Additional user profile fields: points, is_mentor, is_premium, location, title

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.auth_middleware.UserContextMiddleware',
]
```

**Usage in views:**

```python
def my_view(request):
    context = request.user_context
    print(context['user_id'])
    print(context['is_mentor'])
```

#### TokenBlacklistMiddleware

Prevents use of revoked tokens (e.g., after logout).

**Features:**

- Checks token against blacklist database
- Automatically revokes tokens on logout
- Prevents token reuse after revocation

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.auth_middleware.TokenBlacklistMiddleware',
]
```

---

### 2. Error Handling Middleware (`error_handler.py`)

#### ExceptionHandlerMiddleware

Catches unhandled exceptions and returns proper JSON error responses.

**Features:**

- Handles all exception types (404, 403, validation errors, API exceptions, generic)
- Logs exceptions with full traceback for debugging
- Returns standardized error response format
- Exposes traceback only in debug mode

**Handled Exception Types:**

- `Http404` → 404 Not Found
- `PermissionDenied` → 403 Forbidden
- `ValidationError` → 400 Bad Request
- `APIException` → Uses exception's status code
- Generic exceptions → 500 Internal Server Error

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.error_handler.ExceptionHandlerMiddleware',
]
```

**Error Response Format:**

```json
{
  "error": "Internal Server Error",
  "detail": "Detailed error message",
  "status": 500,
  "field_errors": {
    "field_name": ["Error for this field"]
  }
}
```

#### SecurityHeadersMiddleware

Adds security headers to all responses to protect against web vulnerabilities.

**Security Headers Added:**

- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Referrer-Policy: strict-origin-when-cross-origin` - Referrer control
- `Permissions-Policy: geolocation=(), microphone=(), camera=()` - Feature permissions
- `Content-Security-Policy` - Basic CSP policy
- `Strict-Transport-Security` - HTTPS enforcement (production only)

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.error_handler.SecurityHeadersMiddleware',
]
```

#### RequestResponseLoggingMiddleware

Logs all HTTP requests and responses with duration and metadata.

**Logged Information:**

- Request method, path, timestamp
- Response status code
- Request duration (in milliseconds)
- Client IP address
- User information

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.error_handler.RequestResponseLoggingMiddleware',
]
```

**Log Example:**

```
INFO: Request: GET /api/users/
INFO: Response: GET /api/users/ - 200 (25.43ms)
```

---

### 3. Analytics Middleware (`analytics_middleware.py`)

#### AnalyticsMiddleware

Tracks API usage and generates analytics data.

**Features:**

- Tracks API endpoint usage (count per endpoint)
- Measures response times per endpoint
- Monitors error rates
- Caches data for dashboard visualization

**Tracked Metrics:**

- API call count per endpoint per hour
- Response time statistics (average, min, max)
- Error count per status code and endpoint

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.analytics_middleware.AnalyticsMiddleware',
]
```

**Accessing Analytics:**

```python
from django.core.cache import cache

# Get usage count
usage = cache.get('api_usage:GET:/api/users/')

# Get response times
times = cache.get('response_time:GET:/api/users/')
avg_time = sum(times) / len(times) if times else 0
```

#### UserActivityMiddleware

Tracks user activity for profile stats and achievements.

**Features:**

- Records user actions (API calls)
- Updates last activity timestamp
- Maintains activity log per user
- Keeps last 50 actions per user

**Tracked Activities:**

- All user API requests
- Timestamp and endpoint
- Request method (GET, POST, PUT, DELETE)

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.analytics_middleware.UserActivityMiddleware',
]
```

**Accessing User Activity:**

```python
from django.core.cache import cache

# Get user's recent actions
actions = cache.get(f'user_actions:{user_id}')

# Get last activity time
last_activity = cache.get(f'user_last_activity:{user_id}')
```

#### PerformanceMonitoringMiddleware

Monitors application performance and alerts on slow requests.

**Features:**

- Detects slow requests (default: > 1 second)
- Logs slow request details for analysis
- Adds response time header to all responses
- Helps identify performance bottlenecks

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.analytics_middleware.PerformanceMonitoringMiddleware',
]

# Customize slow request threshold
SLOW_REQUEST_THRESHOLD = 1.5  # seconds
```

**Response Header:**

```
X-Response-Time: 0.156s
```

**Slow Request Log Example:**

```
WARNING: Slow request detected: GET /api/courses/ took 1.25s
```

---

### 4. Rate Limiting Middleware (`rate_limiting_middleware.py`)

#### RateLimitMiddleware

Implements rate limiting per user and per IP to prevent API abuse.

**Features:**

- Hourly rate limits (authenticated and anonymous users)
- Burst limits (requests per minute)
- Configurable limits per user type
- Rate limit headers in responses

**Default Limits:**

- Authenticated users: 1000 requests/hour
- Anonymous users: 100 requests/hour
- Burst: 20 requests/minute

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.rate_limiting_middleware.RateLimitMiddleware',
]

# In settings.py
RATE_LIMIT_SETTINGS = {
    'AUTHENTICATED_REQUESTS_PER_HOUR': 1000,
    'ANONYMOUS_REQUESTS_PER_HOUR': 100,
    'BURST_SIZE': 20,
    'BURST_WINDOW': 60,
}
```

**Response Headers:**

```
X-RateLimit-Limit-Hourly: 1000
X-RateLimit-Remaining-Hourly: 987
X-RateLimit-Reset-Hourly: 1641234567

X-RateLimit-Limit-Burst: 20
X-RateLimit-Remaining-Burst: 18
X-RateLimit-Reset-Burst: 1641234560
```

**Rate Limit Exceeded Response:**

```json
{
  "error": "Rate Limit Exceeded",
  "detail": "Too many requests. Please try again later.",
  "limit_type": "hour",
  "status": 429
}
```

#### IPWhitelistMiddleware

Allows bypassing rate limits for whitelisted IPs.

**Features:**

- Whelist specific IPs for unlimited access
- Marks whitelisted requests for special handling
- Useful for internal services and monitoring

**Configuration:**

```python
MIDDLEWARE = [
    'middleware.rate_limiting_middleware.IPWhitelistMiddleware',
]

# In settings.py
RATE_LIMIT_WHITELIST = [
    '127.0.0.1',
    '::1',
    '192.168.1.100',
]
```

---

## Complete Middleware Stack

### Recommended Configuration

Add to `settings.py` MIDDLEWARE list:

```python
MIDDLEWARE = [
    # Security & CORS
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    # Standard Django middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom authentication middleware
    'middleware.auth_middleware.JWTAuthenticationMiddleware',
    'middleware.auth_middleware.UserContextMiddleware',
    'middleware.auth_middleware.TokenBlacklistMiddleware',

    # Custom error handling & security
    'middleware.error_handler.ExceptionHandlerMiddleware',
    'middleware.error_handler.SecurityHeadersMiddleware',
    'middleware.error_handler.RequestResponseLoggingMiddleware',

    # Analytics & monitoring
    'middleware.analytics_middleware.AnalyticsMiddleware',
    'middleware.analytics_middleware.UserActivityMiddleware',
    'middleware.analytics_middleware.PerformanceMonitoringMiddleware',

    # Rate limiting
    'middleware.rate_limiting_middleware.IPWhitelistMiddleware',
    'middleware.rate_limiting_middleware.RateLimitMiddleware',
]
```

### Middleware Execution Order

1. **Django built-in middleware** - Security, sessions, CSRF
2. **Authentication middleware** - JWT validation, user context
3. **Error handling & logging** - Exception catching, security headers
4. **Analytics middleware** - Activity tracking, performance monitoring
5. **Rate limiting middleware** - Request throttling

---

## Configuration Examples

### Development Settings

```python
# settings.py

DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

RATE_LIMIT_SETTINGS = {
    'AUTHENTICATED_REQUESTS_PER_HOUR': 5000,  # Higher for testing
    'ANONYMOUS_REQUESTS_PER_HOUR': 1000,
    'BURST_SIZE': 100,
    'BURST_WINDOW': 60,
}

RATE_LIMIT_WHITELIST = [
    '127.0.0.1',
    '::1',
]
```

### Production Settings

```python
# settings.py

DEBUG = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/errors.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
        },
    },
}

RATE_LIMIT_SETTINGS = {
    'AUTHENTICATED_REQUESTS_PER_HOUR': 1000,
    'ANONYMOUS_REQUESTS_PER_HOUR': 100,
    'BURST_SIZE': 20,
    'BURST_WINDOW': 60,
}

RATE_LIMIT_WHITELIST = [
    '10.0.0.0/8',  # Internal network
]
```

---

## Logging

### Log Directory

Create a `logs/` directory in the project root:

```bash
mkdir -p back-end/logs
touch back-end/logs/django.log
touch back-end/logs/errors.log
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages about potential issues
- **ERROR**: Error messages
- **CRITICAL**: Critical errors that may crash the application

### Monitoring Logs

```bash
# Watch Django logs
tail -f back-end/logs/django.log

# Watch error logs
tail -f back-end/logs/errors.log

# Search for specific errors
grep "Rate Limit Exceeded" back-end/logs/django.log
```

---

## Testing Middleware

### Unit Tests

Create tests in `api/tests.py`:

```python
from django.test import TestCase, RequestFactory
from middleware.auth_middleware import JWTAuthenticationMiddleware
from middleware.error_handler import ExceptionHandlerMiddleware
from middleware.rate_limiting_middleware import RateLimitMiddleware

class MiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = JWTAuthenticationMiddleware(lambda x: None)

    def test_jwt_authentication(self):
        # Test valid token
        request = self.factory.get('/api/users/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer valid_token'
        self.middleware.process_request(request)
        # Assert user is set

    def test_rate_limiting(self):
        # Test rate limit exceeded
        request = self.factory.get('/api/users/')
        middleware = RateLimitMiddleware(lambda x: None)
        # Simulate multiple requests
        # Assert rate limit response
```

### Manual Testing

```bash
# Test JWT authentication
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/users/

# Test rate limiting
for i in {1..101}; do curl http://localhost:8000/api/users/; done

# Check rate limit headers
curl -i http://localhost:8000/api/users/
```

---

## Performance Considerations

### Caching

- Rate limits cached for 1 hour (hourly) and 1 minute (burst)
- Analytics data cached for 1 hour
- User activity cached for 24 hours

### Database Queries

- JWT middleware performs 1 database query per request
- Minimize queries by using select_related/prefetch_related

### Cache Backend

Configure Redis for better performance in production:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## Troubleshooting

### Middleware Not Working

1. Check middleware is added to `MIDDLEWARE` list in `settings.py`
2. Verify import paths are correct
3. Check middleware order (authentication before rate limiting)
4. Review logs for error messages

### Rate Limit Too Restrictive

Adjust in `settings.py`:

```python
RATE_LIMIT_SETTINGS = {
    'AUTHENTICATED_REQUESTS_PER_HOUR': 2000,  # Increase limit
}
```

### High Response Times

Check with PerformanceMonitoringMiddleware logs for slow endpoints. Profile with Django Debug Toolbar or similar tools.

### Token Authentication Not Working

1. Verify JWT token is valid
2. Check Authorization header format: `Authorization: Bearer <token>`
3. Review token expiration time
4. Check JWTAuthenticationMiddleware is enabled

---

## Best Practices

1. **Always use HTTPS in production** - Set `SECURE_SSL_REDIRECT = True`
2. **Monitor rate limits** - Set up alerts for abuse patterns
3. **Log important events** - Use structured logging for analysis
4. **Test middleware** - Create unit tests for custom middleware
5. **Document rate limits** - Communicate limits to API users
6. **Regular log review** - Check logs for security issues
7. **Use Redis caching** - Better performance than database caching
8. **Whitelist internal IPs** - Exempt internal services from rate limits
