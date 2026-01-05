# AI Career Platform - Docker Setup Guide

## Overview

This guide covers the complete Docker setup for the AI Career Platform, including all services needed for development and production.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User Request (Port 80/443)             │
└──────────────────────────┬──────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │    Nginx    │
                    │  (Reverse   │
                    │   Proxy)    │
                    └──────┬──────┘
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐        ┌────▼────┐       ┌────▼────┐
    │ Frontend │        │   API   │       │  Static │
    │  (React) │        │ (Django)│       │  Files  │
    │ Port 3000│        │Port 8000│       │         │
    └─────────┘        └────┬────┘       └─────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
       ┌────▼──────┐   ┌────▼────┐    ┌─────▼────┐
       │ PostgreSQL │   │  Redis  │    │  Celery  │
       │ (Database) │   │ (Cache) │    │ (Workers)│
       │  Port 5432 │   │Port 6379│    │          │
       └───────────┘   └─────────┘    └──────────┘
```

## Services

### 1. **Nginx** (Reverse Proxy)

- Handles SSL/TLS termination
- Routes requests to frontend and backend
- Serves static files
- Implements rate limiting
- Adds security headers
- Port: 80 (HTTP), 443 (HTTPS)

### 2. **PostgreSQL** (Database)

- Primary data storage
- Version: 16-alpine
- Port: 5432
- Volume: `postgres_data`

### 3. **Redis** (Cache & Message Broker)

- Caches API responses
- Celery message broker
- Session storage
- Version: 7-alpine
- Port: 6379
- Volume: `redis_data`

### 4. **Django Backend** (REST API)

- Main application server
- Handles business logic
- Serves API endpoints
- Port: 8000
- Volumes: `static_volume`, `media_volume`, `logs_volume`

### 5. **Celery Worker** (Async Tasks)

- Processes background jobs
- Email sending
- Resume analysis
- Recommendations generation
- Achievement checking
- Concurrency: 4 workers

### 6. **Celery Beat** (Task Scheduler)

- Schedules periodic tasks
- Hourly analytics caching
- Daily recommendation generation
- Daily email digests

### 7. **Flower** (Celery Monitoring)

- Web UI for Celery monitoring
- Task tracking
- Performance metrics
- Port: 5555

### 8. **React Frontend** (Web Application)

- User interface
- Port: 3000
- Built and served via Node.js

## Quick Start

### Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 1.29+)
- 4GB RAM minimum
- 20GB disk space

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd PG3-project
```

2. **Create environment file**

```bash
cp .env.example .env
```

3. **Edit `.env` file**

```bash
nano .env
# Update:
# - SECRET_KEY (generate a random key)
# - DB_PASSWORD
# - REDIS_PASSWORD
# - EMAIL credentials (if using real email)
```

4. **Build and start services**

```bash
docker-compose build
docker-compose up -d
```

5. **Check service status**

```bash
docker-compose ps
```

6. **View logs**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

## Common Commands

### Starting Services

```bash
# Start all services in background
docker-compose up -d

# Start specific service
docker-compose up -d backend

# Start and see logs
docker-compose up backend
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop without removing volumes
docker-compose stop

# Stop and remove volumes (CAUTION: loses data)
docker-compose down -v
```

### Database Operations

```bash
# Create migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access database shell
docker-compose exec db psql -U postgres -d career_platform

# Backup database
docker-compose exec db pg_dump -U postgres career_platform > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres career_platform < backup.sql
```

### Django Operations

```bash
# Run Django shell
docker-compose exec backend python manage.py shell

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Check Django health
docker-compose exec backend python manage.py check
```

### Celery Operations

```bash
# View Celery logs
docker-compose logs -f celery_worker

# Monitor with Flower (http://localhost:5555)
# Already running in the setup

# Inspect active tasks
docker-compose exec celery_worker celery -A tasks inspect active

# Purge all tasks
docker-compose exec celery_worker celery -A tasks purge
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f db

# View last 100 lines
docker-compose logs --tail=100

# Follow specific pattern
docker-compose logs -f | grep ERROR
```

## Development Workflow

### 1. **Code Changes**

```bash
# Edit files in your editor
# Changes are reflected immediately due to volumes

# For backend: restart if settings.py changed
docker-compose restart backend

# For frontend: automatic hot reload
# (changes in src/ are reflected instantly)
```

### 2. **Database Migrations**

```bash
# Create migration
docker-compose exec backend python manage.py makemigrations

# Apply migration
docker-compose exec backend python manage.py migrate
```

### 3. **Testing**

```bash
# Run tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_views.py

# Run with coverage
docker-compose exec backend pytest --cov=api tests/
```

### 4. **Shell Access**

```bash
# Access Django shell
docker-compose exec backend python manage.py shell

# Python code in shell
from api.models import User
User.objects.all().count()
```

## Accessing Services

| Service      | URL                         | Purpose           |
| ------------ | --------------------------- | ----------------- |
| Frontend     | http://localhost:3000       | Web UI            |
| API          | http://localhost:8000/api   | REST API          |
| Admin        | http://localhost:8000/admin | Django Admin      |
| Flower       | http://localhost:5555       | Celery Monitoring |
| Health Check | http://localhost/health     | Service Health    |

## Default Credentials

**Django Admin**:

- Username: `admin`
- Password: `admin123`

(Created automatically on first run)

## Production Deployment

### 1. **Environment Setup**

```bash
# Create production .env
cp .env.example .env.production

# Update with production values
nano .env.production

# Critical settings:
DEBUG=False
SECRET_KEY=<generate-random-256-char-string>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<strong-database-password>
REDIS_PASSWORD=<strong-redis-password>
EMAIL_HOST_PASSWORD=<your-email-app-password>
```

### 2. **SSL Certificates**

```bash
# Using Let's Encrypt with Certbot
mkdir -p ssl
certbot certonly --webroot -w . -d yourdomain.com -d www.yourdomain.com

# Copy certificates to ssl/ directory
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
```

### 3. **Deploy**

```bash
# Pull latest code
git pull origin main

# Build with production env
docker-compose -f docker-compose.yml --env-file .env.production build

# Start services
docker-compose -f docker-compose.yml --env-file .env.production up -d

# Check health
docker-compose ps
curl https://yourdomain.com/health/
```

### 4. **Database Backup**

```bash
# Automated daily backup
0 2 * * * docker-compose exec -T db pg_dump -U postgres career_platform > /backups/db-$(date +\%Y\%m\%d).sql
```

### 5. **Monitoring**

```bash
# Check services
docker-compose ps

# View resource usage
docker stats

# Check logs for errors
docker-compose logs | grep ERROR
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs <service>

# Restart service
docker-compose restart <service>

# Check health
docker-compose ps
```

### Database Connection Failed

```bash
# Wait for database to start
docker-compose logs db

# Test connection
docker-compose exec backend python manage.py dbshell

# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose up -d backend
```

### Redis Connection Failed

```bash
# Check Redis logs
docker-compose logs redis

# Test connection
docker-compose exec redis redis-cli ping

# Should return: PONG
```

### Celery Tasks Not Running

```bash
# Check worker logs
docker-compose logs celery_worker

# Check beat logs
docker-compose logs celery_beat

# Inspect active tasks
docker-compose exec celery_worker celery -A tasks inspect active

# Purge and restart
docker-compose exec celery_worker celery -A tasks purge
docker-compose restart celery_worker
```

### Out of Disk Space

```bash
# Clean up unused images
docker image prune -a

# Clean up unused volumes
docker volume prune

# Check disk usage
docker system df
```

### Memory Issues

```bash
# Increase available memory in Docker Desktop settings

# Or limit service memory
# In docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

## Security Best Practices

1. **Environment Variables**

   - Never commit `.env` file
   - Use strong random passwords
   - Rotate secrets regularly

2. **SSL/TLS**

   - Always use HTTPS in production
   - Renew certificates before expiration
   - Use strong cipher suites

3. **Database**

   - Backup regularly
   - Use strong passwords
   - Restrict access to port 5432

4. **Docker Registry**

   - Use private registry for production images
   - Sign images
   - Scan for vulnerabilities

5. **Updates**
   - Keep Docker and dependencies updated
   - Monitor security advisories
   - Update base images regularly

## Performance Tuning

### 1. **Gunicorn Workers**

```
Recommended: CPU cores * 2 + 1
For 4 cores: 9 workers

In docker-compose.yml:
command: gunicorn backend.wsgi:application --workers 9
```

### 2. **Celery Workers**

```
Recommended: same as Gunicorn
concurrency: 9

In docker-compose.yml:
command: celery -A tasks worker -l info --concurrency=9
```

### 3. **Database Connections**

```
Max connections in PostgreSQL:
Max = (RAM in GB) * 3

For 8GB RAM: 24 connections
```

### 4. **Redis Memory**

```
Set max memory policy:
maxmemory 512mb
maxmemory-policy allkeys-lru
```

### 5. **Nginx Caching**

```
Already configured in nginx.conf:
- Static files cached 30 days
- Media files cached 7 days
- API responses not cached (dynamic)
```

## Monitoring

### 1. **Container Health**

```bash
docker-compose ps
docker stats
```

### 2. **Application Logs**

```bash
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

### 3. **Celery Tasks** (Flower)

```
http://localhost:5555
- Active tasks
- Completed tasks
- Failed tasks
- Task history
```

### 4. **Database**

```bash
# Connection count
SELECT count(*) FROM pg_stat_activity;

# Slow queries
SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC;
```

## Maintenance

### Daily

- Monitor logs for errors
- Check disk space
- Monitor task queue

### Weekly

- Review Celery task metrics
- Check database size
- Update dependencies if needed

### Monthly

- Database maintenance (VACUUM, ANALYZE)
- SSL certificate renewal check
- Security updates

### Quarterly

- Database backup restoration test
- Disaster recovery drill
- Performance review

## File Structure

```
PG3-project/
├── docker-compose.yml          # Service orchestration
├── nginx.conf                  # Nginx configuration
├── .env.example                # Environment template
├── back-end/
│   ├── Dockerfile             # Django image
│   ├── docker-entrypoint.sh    # Startup script
│   ├── .dockerignore           # Docker build exclusions
│   └── [Django files]
├── front-end/
│   ├── Dockerfile             # React image
│   ├── .dockerignore           # Docker build exclusions
│   └── [React files]
└── ssl/                        # SSL certificates (create for HTTPS)
    ├── cert.pem
    └── key.pem
```

## Support

For Docker-related issues, refer to:

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)

For application-specific issues, see:

- [README.md](back-end/README.md) - Backend overview
- [API_REFERENCE.md](back-end/API_REFERENCE.md) - API documentation
- [TASKS_GUIDE.md](back-end/TASKS_GUIDE.md) - Celery documentation
