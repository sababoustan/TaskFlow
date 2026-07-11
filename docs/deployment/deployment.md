# Deployment

This document describes the deployment architecture and infrastructure of the TaskFlow backend.

---

# Deployment Goal

Deploy the application in a production-ready environment with scalability, security, maintainability, and containerized infrastructure.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django + Django REST Framework |
| Database | PostgreSQL |
| Cache | Redis |
| Background Jobs | Celery |
| WSGI Server | Gunicorn |
| Reverse Proxy | Nginx |
| Containerization | Docker |
| Container Management | Docker Compose |
| Continuous Integration | GitHub Actions |

---

# Deployment Architecture

```text
                    Client
                       │
                       ▼
                    Nginx
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
      Gunicorn                 Static Files
          │
          ▼
      Django API
          │
 ┌────────┼─────────────┐
 ▼        ▼             ▼
PostgreSQL Redis      Celery Worker
                      │
                      ▼
                 Background Jobs
```

---

# Docker Containers

The application consists of the following containers:

- nginx
- backend
- postgres
- redis
- celery
- celery-beat

---

# Docker Compose Services

## Backend

Runs the Django application using Gunicorn.

Responsibilities:

- REST API
- JWT Authentication
- User Management
- Password Management
- Business Logic
- Database Access

---

## PostgreSQL

Stores all application data.

Responsibilities:

- Users
- Workspaces
- Memberships
- Projects
- Sprints
- Tasks
- Labels
- Comments
- Attachments
- Notifications

---

## Redis

Acts as both the cache layer and the Celery message broker.

Responsibilities:

- Caching
- Celery Message Broker
- Celery Result Backend
- Rate Limiting (Future)

---

## Celery

Executes asynchronous background jobs.

Example jobs:

- Send workspace invitation emails
- Send task notifications
- Process background tasks

---

## Celery Beat

Runs scheduled background tasks.

Example tasks:

- Remove expired invitations
- Send task deadline reminders
- Cleanup temporary data

---

## Nginx

Acts as the reverse proxy.

Responsibilities:

- HTTPS
- Reverse Proxy
- Static Files
- Media Files
- Request Routing

---

# Environment Variables

Sensitive configuration must never be committed to Git.

Example:

```env
SECRET_KEY=

DEBUG=

ACCESS_TOKEN_LIFETIME=

REFRESH_TOKEN_LIFETIME=

ALLOWED_HOSTS=

POSTGRES_DB=

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_HOST=

POSTGRES_PORT=

REDIS_HOST=

REDIS_PORT=

EMAIL_HOST=

EMAIL_PORT=

EMAIL_HOST_USER=

EMAIL_HOST_PASSWORD=

```

---

# Static Files

Collect static files before deployment.

```bash
python manage.py collectstatic
```

Served by:

- Nginx

---

# Media Files

Uploaded files are stored inside:

```text
/media/
```

Served by:

- Nginx

---

# Database Migration

Before starting the application:

```bash
python manage.py migrate
```

---

# Create Superuser

```bash
python manage.py createsuperuser
```

---

# Celery Commands

Worker

```bash
celery -A config worker -l info
```

Beat

```bash
celery -A config beat -l info
```

---

# Gunicorn

Gunicorn is used as the WSGI server in the production environment.

Example:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

The number of worker processes should be configured based on the available CPU cores and production server resources.

# Reverse Proxy

```text
Client
    │
    ▼
Nginx
    │
    ▼
Gunicorn
    │
    ▼
Django REST API
```

---

# Security

Production deployment should include:

- HTTPS
- SSL Certificates
- JWT Authentication
- Refresh Token Blacklisting
- Secure Cookies
- HttpOnly Cookies
- CSRF Protection
- CORS Configuration
- Environment Variables
- Hidden Secret Keys
- Strong Password Policy

---

# Logging

Application logs include:

- Authentication Events
- Login Attempts
- Password Changes
- API Requests
- Exceptions
- Celery Tasks
- Database Errors

Logs can be written to:

- Console
- File System

---

# Monitoring

Possible future monitoring tools:

- Prometheus
- Grafana

Metrics:

- CPU Usage
- Memory Usage
- Response Time
- Error Rate
- Queue Size
- Authentication Failures
- API Throughput

---

# Backup Strategy

Regular database backups should be scheduled.

Suggested strategy:

- Daily Backup
- Weekly Full Backup

Uploaded files should also be backed up.

---

# Continuous Integration (CI)

The project uses GitHub Actions for Continuous Integration.

The CI pipeline performs:

- Install Dependencies
- Run Code Formatter
- Run Linter
- Run Unit Tests
- Build Docker Image

---

# CI Workflow

```text
Developer
      │
      ▼
Git Push
      │
      ▼
GitHub
      │
      ▼
GitHub Actions
      │
      ▼
Install Dependencies
      │
      ▼
Run Formatter
      │
      ▼
Run Linter
      │
      ▼
Run Tests
      │
      ▼
Build Docker Image
      │
      ▼
Pipeline Passed
```

---

# Deployment Checklist

Before deployment:

- Environment Variables Configured
- JWT Configuration Verified
- Authentication Endpoints Tested
- DEBUG=False
- Database Migrated
- Static Files Collected
- Docker Containers Running
- PostgreSQL Running
- Redis Running
- Celery Worker Running
- Celery Beat Running
- Gunicorn Running
- Nginx Running
- HTTPS Enabled

---

# Future Improvements

- Continuous Deployment (CD)
- Kubernetes
- Horizontal Scaling
- Load Balancer
- Object Storage (AWS S3 / MinIO)
- Monitoring Dashboard
- Distributed Caching
- GitHub Container Registry
- Email Verification
- Password Reset via Email
- Login Rate Limiting
- Distributed Session Management

---

# Deployment Status

| Component | Status |
|-----------|--------|
| Django REST API | Planned |
| PostgreSQL | Planned |
| Redis | Planned |
| Celery | Planned |
| Celery Beat | Planned |
| Gunicorn | Planned |
| Nginx | Planned |
| Docker | Planned |
| Docker Compose | Planned |
| GitHub Actions (CI) | Planned |
| Continuous Deployment (CD) | Not Implemented |
| Kubernetes | Future |

---

# Deployment Philosophy

The deployment architecture follows a production-ready approach.

The primary goals are:

- Scalability
- Security
- Reliability
- Maintainability
- High Availability
- Containerized Infrastructure
- Cloud Readiness