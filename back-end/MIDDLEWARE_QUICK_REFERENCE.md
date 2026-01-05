# Middleware Quick Reference

## All Middleware Components

### Authentication

```
middleware.auth_middleware.JWTAuthenticationMiddleware      # JWT token validation
middleware.auth_middleware.UserContextMiddleware           # User context enrichment
middleware.auth_middleware.TokenBlacklistMiddleware        # Token revocation checking
```

### Error Handling & Security

```
middleware.error_handler.ExceptionHandlerMiddleware        # Exception catching
middleware.error_handler.SecurityHeadersMiddleware         # Security headers
middleware.error_handler.RequestResponseLoggingMiddleware  # Request/response logging
```

### Analytics

```
middleware.analytics_middleware.AnalyticsMiddleware         # API usage tracking
middleware.analytics_middleware.UserActivityMiddleware      # User activity tracking
middleware.analytics_middleware.PerformanceMonitoringMiddleware  # Slow request detection
```

### Rate Limiting

```
middleware.rate_limiting_middleware.IPWhitelistMiddleware   # IP whitelist
middleware.rate_limiting_middleware.RateLimitMiddleware     # Rate limiting
```

---

## Installation in settings.py

```python
MIDDLEWARE = [
    # Django built-in
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware
    'middleware.auth_middleware.JWTAuthenticationMiddleware',
    'middleware.auth_middleware.UserContextMiddleware',
    'middleware.auth_middleware.TokenBlacklistMiddleware',
    'middleware.error_handler.ExceptionHandlerMiddleware',
    'middleware.error_handler.SecurityHeadersMiddleware',
    'middleware.error_handler.RequestResponseLoggingMiddleware',
    'middleware.analytics_middleware.AnalyticsMiddleware',
    'middleware.analytics_middleware.UserActivityMiddleware',
    'middleware.analytics_middleware.PerformanceMonitoringMiddleware',
    'middleware.rate_limiting_middleware.IPWhitelistMiddleware',
    'middleware.rate_limiting_middleware.RateLimitMiddleware',
]
```

---

## Configuration

### Rate Limiting

```python
RATE_LIMIT_SETTINGS = {
    'AUTHENTICATED_REQUESTS_PER_HOUR': 1000,
    'ANONYMOUS_REQUESTS_PER_HOUR': 100,
    'BURST_SIZE': 20,
    'BURST_WINDOW': 60,
}

RATE_LIMIT_WHITELIST = [
    '127.0.0.1',
    '::1',
    'localhost',
]
```

### Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
    },
    'loggers': {
        'middleware': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

---

## Key Features

### Authentication

- ✅ JWT token validation
- ✅ User context enrichment
- ✅ Token blacklisting

### Error Handling

- ✅ Exception catching (404, 403, 400, 500, etc.)
- ✅ Security headers (XSS, clickjacking, MIME sniffing)
- ✅ Request/response logging

### Analytics

- ✅ API usage tracking per endpoint
- ✅ User activity recording
- ✅ Slow request detection (> 1 second)

### Rate Limiting

- ✅ Hourly rate limits (1000 auth, 100 anon)
- ✅ Burst limits (20/minute)
- ✅ IP whitelist bypass

---

## Common Use Cases

### Check if User is Authenticated

```python
def my_view(request):
    if request.user.is_authenticated:
        user_id = request.user_context['user_id']
```

### Get User Context

```python
def my_view(request):
    context = request.user_context
    is_mentor = context.get('is_mentor', False)
    points = context.get('points', 0)
```

### Check Analytics

```python
from django.core.cache import cache

# API usage
usage = cache.get('api_usage:GET:/api/users/')

# Response times
times = cache.get('response_time:GET:/api/users/')
avg = sum(times) / len(times) if times else 0
```

### Handle Rate Limiting

```python
# Client checks headers
X-RateLimit-Remaining-Hourly: 950
X-RateLimit-Reset-Hourly: 1641234567

# When limit exceeded: HTTP 429
{
  "error": "Rate Limit Exceeded",
  "detail": "Too many requests. Please try again later."
}
```

---

## Monitoring

### Watch Logs

```bash
tail -f logs/django.log
tail -f logs/errors.log
```

### Monitor Performance

```bash
grep "Slow request" logs/django.log
```

### Check Rate Limits

```bash
grep "Rate Limit Exceeded" logs/django.log
```

### User Activity

```bash
grep "user_actions" logs/django.log
```

---

## Security

- ✅ XSS Protection
- ✅ Clickjacking Prevention
- ✅ MIME Sniffing Protection
- ✅ CSRF Protection
- ✅ Referrer Policy
- ✅ Feature Policy
- ✅ Content Security Policy

---

## File Structure

```
middleware/
├── __init__.py                      # Package exports
├── auth_middleware.py               # Authentication (JWT, context, blacklist)
├── error_handler.py                 # Error handling & security
├── analytics_middleware.py           # Analytics & monitoring
└── rate_limiting_middleware.py       # Rate limiting & IP whitelist
```

---

## Testing

### Test Rate Limiting

```bash
# Simulate 101 requests (exceeds 100/hour limit for anon)
for i in {1..101}; do curl http://localhost:8000/api/users/; done
```

### Test JWT Auth

```bash
# Get token
curl -X POST http://localhost:8000/token/ \
  -d "username=user&password=pass"

# Use token
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/users/
```

### Check Headers

```bash
curl -i http://localhost:8000/api/users/
# See X-RateLimit-* and X-Response-Time headers
```

---

## Troubleshooting

| Issue                  | Solution                                   |
| ---------------------- | ------------------------------------------ |
| Middleware not loading | Check MIDDLEWARE order in settings.py      |
| Rate limit not working | Verify RATE_LIMIT_SETTINGS configured      |
| JWT not validating     | Check Authorization header format          |
| Slow request alerts    | Review SLOW_REQUEST_THRESHOLD              |
| Logs not appearing     | Create logs/ directory and set permissions |
