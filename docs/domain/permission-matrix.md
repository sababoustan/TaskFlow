# Permission Matrix

This document defines the authorization rules for each role in the TaskFlow system.

---

## Roles

The system supports the following roles:

| Role    | Description                                                                 |
| ------- | --------------------------------------------------------------------------- |
| Admin   | Full access to all workspace resources.                                     |
| Manager | Can manage projects, sprints, tasks and members except workspace ownership. |
| Member  | Can work on assigned tasks and collaborate within the workspace.            |
| Viewer  | Read-only access.                                                           |

---

# Workspace

| Permission         | Admin | Manager | Member | Viewer |
| ------------------ | :---: | :-----: | :----: | :----: |
| View Workspace     |   ✅   |    ✅    |    ✅   |    ✅   |
| Update Workspace   |   ✅   |    ❌    |    ❌   |    ❌   |
| Delete Workspace   |   ✅   |    ❌    |    ❌   |    ❌   |
| Transfer Ownership |   ✅   |    ❌    |    ❌   |    ❌   |

---

# Members

| Permission         | Admin | Manager | Member | Viewer |
| ------------------ | :---: | :-----: | :----: | :----: |
| View Members       |   ✅   |    ✅    |    ✅   |    ✅   |
| Invite Member      |   ✅   |    ✅    |    ❌   |    ❌   |
| Remove Member      |   ✅   |    ✅    |    ❌   |    ❌   |
| Change Member Role |   ✅   |    ❌    |    ❌   |    ❌   |

---

# Project

| Permission      | Admin | Manager | Member | Viewer |
| --------------- | :---: | :-----: | :----: | :----: |
| View Project    |   ✅   |    ✅    |    ✅   |    ✅   |
| Create Project  |   ✅   |    ✅    |    ❌   |    ❌   |
| Update Project  |   ✅   |    ✅    |    ❌   |    ❌   |
| Archive Project |   ✅   |    ✅    |    ❌   |    ❌   |
| Delete Project  |   ✅   |    ❌    |    ❌   |    ❌   |

---

# Sprint

| Permission      | Admin | Manager | Member | Viewer |
| --------------- | :---: | :-----: | :----: | :----: |
| View Sprint     |   ✅   |    ✅    |    ✅   |    ✅   |
| Create Sprint   |   ✅   |    ✅    |    ❌   |    ❌   |
| Update Sprint   |   ✅   |    ✅    |    ❌   |    ❌   |
| Start Sprint    |   ✅   |    ✅    |    ❌   |    ❌   |
| Complete Sprint |   ✅   |    ✅    |    ❌   |    ❌   |
| Delete Sprint   |   ✅   |    ❌    |    ❌   |    ❌   |

---

# Task

| Permission      | Admin | Manager | Member | Viewer |
| --------------- | :---: | :-----: | :----: | :----: |
| View Task       |   ✅   |    ✅    |    ✅   |    ✅   |
| Create Task     |   ✅   |    ✅    |    ✅   |    ❌   |
| Update Task     |   ✅   |    ✅    |   ✅*   |    ❌   |
| Delete Task     |   ✅   |    ✅    |    ❌   |    ❌   |
| Assign Task     |   ✅   |    ✅    |    ❌   |    ❌   |
| Change Status   |   ✅   |    ✅    |    ✅   |    ❌   |
| Change Priority |   ✅   |    ✅    |    ✅   |    ❌   |
| Move Task       |   ✅   |    ✅    |    ✅   |    ❌   |
| Set Due Date    |   ✅   |    ✅    |    ✅   |    ❌   |
| Estimate Task   |   ✅   |    ✅    |    ✅   |    ❌   |

* Members may edit tasks they created or tasks assigned to them.

---

# Label

| Permission   | Admin | Manager | Member | Viewer |
| ------------ | :---: | :-----: | :----: | :----: |
| View Labels  |   ✅   |    ✅    |    ✅   |    ✅   |
| Create Label |   ✅   |    ✅    |    ✅   |    ❌   |
| Update Label |   ✅   |    ✅    |    ✅   |    ❌   |
| Delete Label |   ✅   |    ✅    |    ❌   |    ❌   |
| Assign Label |   ✅   |    ✅    |    ✅   |    ❌   |
| Remove Label |   ✅   |    ✅    |    ✅   |    ❌   |

---

# Comment

| Permission         | Admin | Manager | Member | Viewer |
| ------------------ | :---: | :-----: | :----: | :----: |
| View Comments      |   ✅   |    ✅    |    ✅   |    ✅   |
| Add Comment        |   ✅   |    ✅    |    ✅   |    ❌   |
| Reply Comment      |   ✅   |    ✅    |    ✅   |    ❌   |
| Edit Own Comment   |   ✅   |    ✅    |    ✅   |    ❌   |
| Delete Own Comment |   ✅   |    ✅    |    ✅   |    ❌   |
| Delete Any Comment |   ✅   |    ✅    |    ❌   |    ❌   |

---

# Attachment

| Permission            | Admin | Manager | Member | Viewer |
| --------------------- | :---: | :-----: | :----: | :----: |
| View Attachments      |   ✅   |    ✅    |    ✅   |    ✅   |
| Upload Attachment     |   ✅   |    ✅    |    ✅   |    ❌   |
| Delete Own Attachment |   ✅   |    ✅    |    ✅   |    ❌   |
| Delete Any Attachment |   ✅   |    ✅    |    ❌   |    ❌   |

---

# Notification

| Permission         | Admin | Manager | Member | Viewer |
| ------------------ | :---: | :-----: | :----: | :----: |
| View Notifications |   ✅   |    ✅    |    ✅   |    ✅   |
| Mark as Read       |   ✅   |    ✅    |    ✅   |    ✅   |

---

# Activity Log

| Permission        | Admin | Manager | Member | Viewer |
| ----------------- | :---: | :-----: | :----: | :----: |
| View Activity Log |   ✅   |    ✅    |    ✅   |    ✅   |

---

# Workspace Invitation

| Permission        | Admin | Manager | Member | Viewer |
| ----------------- | :---: | :-----: | :----: | :----: |
| Create Invitation |   ✅   |    ✅    |    ❌   |    ❌   |
| Cancel Invitation |   ✅   |    ✅    |    ❌   |    ❌   |
| Accept Invitation |   ✅   |    ✅    |    ✅   |    ✅   |
| Reject Invitation |   ✅   |    ✅    |    ✅   |    ✅   |

---

# Status

| Permission         | Admin | Manager | Member | Viewer |
| ------------------ | :---: | :-----: | :----: | :----: |
| View Statuses      |   ✅   |    ✅    |    ✅   |    ✅   |
| Change Task Status |   ✅   |    ✅    |    ✅   |    ❌   |

---

# Priority

| Permission           | Admin | Manager | Member | Viewer |
| -------------------- | :---: | :-----: | :----: | :----: |
| View Priorities      |   ✅   |    ✅    |    ✅   |    ✅   |
| Change Task Priority |   ✅   |    ✅    |    ✅   |    ❌   |

---

## Notes

* Only the workspace owner can transfer workspace ownership.
* Members can modify only their own comments and attachments.
* Members can edit only tasks they created or tasks assigned to them.
* Viewers have read-only access throughout the workspace.
* Notifications are generated automatically by the system and cannot be created manually.
* Activity logs are created automatically and cannot be modified by users.
* Workspace invitations expire automatically after the configured expiration time.
* Role permissions apply only within the associated workspace.
