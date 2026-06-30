# Aggregate Design

This document defines the aggregate boundaries of the TaskFlow domain model based on Domain-Driven Design (DDD).

An aggregate is a consistency boundary that groups related entities and enforces business rules through a single Aggregate Root.

---

# Workspace Aggregate

## Aggregate Root

- Workspace

## Entities

- Membership
- WorkspaceInvitation

## References

- User

## Responsibilities

- Create and manage workspaces.
- Manage workspace members.
- Invite users to the workspace.
- Assign member roles.
- Ensure each workspace has exactly one owner.
- Prevent duplicate memberships.
- Validate workspace invitations.

---

# Project Aggregate

## Aggregate Root

- Project

## Entities

- Sprint

## References

- Workspace

## Responsibilities

- Create and manage projects.
- Archive projects.
- Manage project sprints.
- Ensure project names are unique within a workspace.
- Maintain project lifecycle.

---

# Task Aggregate

## Aggregate Root

- Task

## Entities

- Comment
- Attachment

## References

- Project
- Sprint
- User (Creator)
- User (Assignee)
- Status
- Priority
- Label

## Responsibilities

- Create tasks.
- Update task information.
- Delete tasks.
- Assign tasks to users.
- Move tasks between columns.
- Change task status.
- Change task priority.
- Set due dates.
- Estimate task duration.
- Assign tasks to sprints.
- Add labels.
- Remove labels.
- Validate task business rules.
- Record task activities.
- Record task status changes.

---

# Notification Aggregate

## Aggregate Root

- Notification

## References

- User (Recipient)
- User (Sender)

## Responsibilities

- Generate notifications.
- Store notification information.
- Mark notifications as read.
- Deliver task-related notifications.

---

# Comment Aggregate

## Aggregate Root

- Comment

## References

- Task
- User

## Responsibilities

- Create comments.
- Reply to comments.
- Edit comments.
- Delete comments.
- Maintain comment hierarchy.

---

# Attachment Aggregate

## Aggregate Root

- Attachment

## References

- Task
- User

## Responsibilities

- Upload attachments.
- Store file metadata.
- Delete attachments.
- Validate uploaded files.

---

# Aggregate Communication

Aggregates communicate through identifiers (IDs) instead of direct object references.

Examples:

- A Task references a Project by `project_id`.
- A Task references a Sprint by `sprint_id`.
- A Membership references a Workspace by `workspace_id`.
- A Notification references a User by `user_id`.

This approach keeps aggregates loosely coupled and improves scalability.

---

# Aggregate Rules

- Every aggregate has exactly one Aggregate Root.
- External objects may only access an aggregate through its Aggregate Root.
- Business rules are enforced inside aggregate boundaries.
- References between aggregates should be made using IDs.
- Aggregates should remain small and focused on a single business responsibility.

---

# Aggregate Summary

| Aggregate | Aggregate Root | Main Entities |
|-----------|----------------|---------------|
| Workspace | Workspace | Membership, WorkspaceInvitation |
| Project | Project | Sprint |
| Task | Task | Comment, Attachment |
| Notification | Notification | — |
| Comment | Comment | — |
| Attachment | Attachment | — |