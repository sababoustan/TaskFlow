# API Design

This document describes the REST API design for the TaskFlow backend.

---

# Base URL

```
/api/v1/
```

---

# Authentication

Authentication is based on JWT (JSON Web Token).
Access tokens are short-lived, while refresh tokens are used to obtain new access tokens.

Every protected endpoint requires the following header:

```
Authorization: Bearer <access_token>
```

---

# Response Format

## Success Response

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

## Error Response

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": {}
}
```

---

# Authentication Endpoints

## Register

```
POST /auth/register/
```

Creates a new user account.

---

## Login

```
POST /auth/login/
```

Returns JWT access and refresh tokens.

---

## Refresh Token

```
POST /auth/token/refresh/
```

Returns a new access token using a valid refresh token.

---

## Logout

```
POST /auth/logout/
```

Deletes the authenticated user's account and invalidates all active refresh tokens.

---

## Profile

```
GET /auth/profile/

```

Returns the authenticated user's profile.

---

## Update Profile

```
PUT /auth/profile/
```

Updates the authenticated user's profile.

---

```
PATCH /auth/profile/
```

Partially updates the authenticated user's profile.

---

## Delete Account

```
DELETE /auth/account/
```

Deletes the authenticated user's account and invalidates all active refresh tokens.
---

## Change Password

```
PATCH /auth/change-password/
```

Changes the authenticated user's password.

---

# Workspace

## List Workspaces

```http
GET /api/v1/workspaces/
```

Returns all workspaces owned by or shared with the authenticated user.

---

## Create Workspace

```http
POST /api/v1/workspaces/
```

Creates a new workspace.

---

## Retrieve Workspace

```http
GET /api/v1/workspaces/{workspace_id}/
```

Returns workspace details.

---

## Update Workspace

```http
PATCH /api/v1/workspaces/{workspace_id}/
```

Updates workspace information.

---

## Delete Workspace

```http
DELETE /api/v1/workspaces/{workspace_id}/
```

Deletes a workspace.

---

# Workspace Invitations

## List Invitations

```http
GET /api/v1/workspaces/{workspace_id}/invitations/
```

Returns all invitations for the specified workspace.

Only workspace owners and admins can access this endpoint.

---

## Create Invitation

```http
POST /api/v1/workspaces/{workspace_id}/invitations/
```

Invites an existing user to the workspace and assigns a role.

Validation includes:

- User must exist.
- User must not already be a workspace member.
- User must not already have a pending invitation.
- Only workspace owner or admins can invite users.

---

## Accept Invitation

```http
POST /api/v1/workspaces/invitations/{invitation_id}/accept/
```

Accepts a pending invitation.

A Membership record is created automatically using the role assigned in the invitation.

---

## Reject Invitation

```http
POST /api/v1/workspaces/invitations/{invitation_id}/reject/
```

Rejects a pending invitation.

The invitation status becomes `REJECTED`.

---

## Cancel Invitation

```http
POST /api/v1/workspaces/invitations/{invitation_id}/cancel/
```

Cancels a pending invitation.

Only workspace owners and admins can perform this action.

The invitation status becomes `CANCELLED`.

# Project

## List Projects

```
GET /projects/
```

Returns all projects.

---

## Create Project

```
POST /projects/
```

Creates a project.

---

## Get Project

```
GET /projects/{project_id}/
```

Returns project details.

---

## Update Project

```
PUT /projects/{project_id}/
```

Updates a project.

---

## Archive Project

```
PATCH /projects/{project_id}/archive/
```

Archives a project.

---

## Delete Project

```
DELETE /projects/{project_id}/
```

Deletes a project.

---

# Sprint

## List Sprints

```
GET /projects/{project_id}/sprints/
```

---

## Create Sprint

```
POST /projects/{project_id}/sprints/
```

---

## Get Sprint

```
GET /sprints/{sprint_id}/
```

---

## Update Sprint

```
PUT /sprints/{sprint_id}/
```

---

## Start Sprint

```
PATCH /sprints/{sprint_id}/start/
```

---

## Complete Sprint

```
PATCH /sprints/{sprint_id}/complete/
```

---

## Delete Sprint

```
DELETE /sprints/{sprint_id}/
```

---

# Task

## List Tasks

```
GET /tasks/
```

---

## Create Task

```
POST /tasks/
```

---

## Get Task

```
GET /tasks/{task_id}/
```

---

## Update Task

```
PUT /tasks/{task_id}/
```

---

## Delete Task

```
DELETE /tasks/{task_id}/
```

---

## Assign Task

```
PATCH /tasks/{task_id}/assign/
```

---

## Change Task Status

```
PATCH /tasks/{task_id}/status/
```

---

## Change Task Priority

```
PATCH /tasks/{task_id}/priority/
```

---

## Move Task

```
PATCH /tasks/{task_id}/position/
```

---

## Set Due Date

```
PATCH /tasks/{task_id}/due-date/
```

---

## Estimate Task

```
PATCH /tasks/{task_id}/estimate/
```

---

# Labels

## List Labels

```
GET /labels/
```

---

## Create Label

```
POST /labels/
```

---

## Update Label

```
PUT /labels/{label_id}/
```

---

## Delete Label

```
DELETE /labels/{label_id}/
```

---

## Attach Label

```
POST /tasks/{task_id}/labels/
```

---

## Remove Label

```
DELETE /tasks/{task_id}/labels/{label_id}/
```

---

# Comments

## List Comments

```
GET /tasks/{task_id}/comments/
```

---

## Add Comment

```
POST /tasks/{task_id}/comments/
```

---

## Reply Comment

```
POST /comments/{comment_id}/reply/
```

---

## Update Comment

```
PUT /comments/{comment_id}/
```

---

## Delete Comment

```
DELETE /comments/{comment_id}/
```

---

# Attachments

## Upload Attachment

```
POST /tasks/{task_id}/attachments/
```

---

## Delete Attachment

```
DELETE /attachments/{attachment_id}/
```

---

# Notifications

## List Notifications

```
GET /notifications/
```

---

## Mark Notification As Read

```
PATCH /notifications/{notification_id}/read/
```

---

# Activity Logs

## List Activity Logs

```
GET /tasks/{task_id}/activities/
```

Returns all activities related to the selected task.

---

# HTTP Status Codes

| Code | Description           |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 204  | No Content            |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 409  | Conflict              |
| 500  | Internal Server Error |

---

# API Versioning

The API uses URL versioning.

```
/api/v1/
```

Future versions:

```
/api/v2/
```

---

# Pagination

List endpoints support pagination.

Example:

```
GET /tasks?page=1&page_size=20
```

---

# Filtering

Supported query parameters:

```
status=

priority=

assigned_to=

project=

workspace=

sprint=

label=

due_date=
```

---

# Sorting

Supported sorting fields:

```
created_at

updated_at

due_date

priority

position
```

Example:

```
GET /tasks?ordering=-created_at
```

---

# Search

Example:

```
GET /tasks?search=login
```

---

# File Upload

Attachments are uploaded using:

```
multipart/form-data
```

---

# Content Types

```
application/json

multipart/form-data
```

# API Documentation

Interactive API documentation is available through Swagger UI and OpenAPI Specification.

