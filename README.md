# TaskFlow

TaskFlow is a backend task management system inspired by Jira and Trello, built with Django REST Framework.

The project follows a layered architecture and separates business logic from API views using a Service Layer pattern. It provides secure authentication, workspace management, invitation workflows, and role-based permissions.

---

## Features

### Authentication

- Custom User Model (Email Authentication)
- JWT Authentication (Login / Logout)
- Change Password with Token Blacklisting
- User Profile API
- Delete Account API
- Workspace CRUD
- Workspace Invitation System
- Accept / Reject / Cancel Invitations
- Automatic Membership Creation
- Role-Based Access Control (RBAC)
- Unique Workspace Slugs
- Service Layer Pattern
- OpenAPI Documentation (Swagger & ReDoc)
- Comprehensive API Tests with Pytest

---

### Workspace Management

- Create Workspace
- List User Workspaces
- Update Workspace
- Delete Workspace
- Automatic Unique Slug Generation
- Search Workspaces

---

### Workspace Invitations

- Invite users by email
- Assign role while inviting
- List workspace invitations
- Accept invitation
- Reject invitation
- Cancel invitation

Invitation validation includes:

- Prevent inviting existing members
- Prevent duplicate pending invitations
- Permission validation
- Invitation status managementInvitation validation includes:

- Prevent inviting existing members
- Prevent duplicate pending invitations
- Permission validation
- Invitation status management

---

### Membership

- Automatic membership creation after accepting an invitation
- Workspace role assignment
- Unique membership per workspace

---

### Permission System

Role-based access control.

Supported roles:

- Admin
- Manager
- Member
- Viewer

Workspace owner automatically has full access.

---

### Security

- JWT Authentication
- Refresh Token Blacklisting
- Password Validation
- Permission Checks
- Service Layer Validation
- Transaction support for sensitive operations

---

### Testing

## Testing

The project includes a comprehensive automated API test suite covering:

- Authentication and authorization
- User APIs
- Workspace APIs
- Membership APIs
- Invitation APIs
- Project APIs
- Workflow APIs
- Status APIs
- Sprint APIs
- Positive and negative test cases
- Role-based access control
- API validation
- Database state verification

Implemented using:

- pytest
- pytest-django
- Django REST Framework APIClient
- Fixtures
- Parametrization
- `conftest.py`

### Test Results

✅ 221 tests passed

For detailed testing documentation, see [`docs/testing.md`](docs/testing.md).

---

## Tech Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- drf-spectacular
- PostgreSQL
- pytest
- pytest-django

---

## Project Structure

```
TaskFlow/

├── apps/
│   ├── users/
│   ├── workspaces/
│   ├── projects/
│   └── tasks/
│
├── config/
├── docs/
├── requirements.txt
├── manage.py
└── README.md
```

The project follows Layered Architecture:

```
Views
    ↓
Serializers
    ↓
Services
    ↓
Models
```

Business logic is implemented inside Service Layer instead of Views.

---

## API Documentation

Swagger

```
/api/docs/
```

ReDoc

```
/api/redoc/
```

OpenAPI Schema

```
/api/schema/
```

---

## Authentication Endpoints

| Method | Endpoint |
|----------|-----------------------------|
| POST | /api/v1/auth/register/ |
| POST | /api/v1/auth/login/ |
| POST | /api/v1/auth/logout/ |
| GET | /api/v1/auth/profile/ |
| PUT | /api/v1/auth/change-password/ |
| DELETE | /api/v1/auth/delete-account/ |

---

## Workspace Endpoints

| Method | Endpoint |
|----------|-------------------------------------------|
| POST | /api/v1/workspaces/ |
| GET | /api/v1/workspaces/ |
| PATCH | /api/v1/workspaces/{id}/ |
| DELETE | /api/v1/workspaces/{id}/ |

---

## Invitation Endpoints

| Method | Endpoint |
|----------|------------------------------------------------|
| POST | /api/v1/workspaces/{workspace_id}/invitations/ |
| GET | /api/v1/workspaces/{workspace_id}/invitations/ |
| POST | /api/v1/workspaces/invitations/{id}/accept/ |
| POST | /api/v1/workspaces/invitations/{id}/reject/ |
| POST | /api/v1/workspaces/invitations/{id}/cancel/ |

---

## Installation

Clone the repository

```bash
git clone https://github.com/sababoustan/TaskFlow
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Run server

```bash
python manage.py runserver
```

---

## Run Tests

```bash
pytest
```

---

## Architecture Principles

- Layered Architecture
- Service Layer Pattern
- RESTful API Design
- Role Based Authorization
- Separation of Concerns
- Clean Code

---

## Current Progress

✅ Authentication Module

✅ Workspace Module

✅ Membership Module

✅ Invitation Module

⬜ Projects

⬜ Tasks

⬜ Comments

⬜ Notifications

⬜ Activity Logs

---

## License

This project is for educational and portfolio purposes.