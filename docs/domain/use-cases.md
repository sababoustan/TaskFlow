# Use Cases

This document describes all business use cases supported by the TaskFlow system.

---

# Authentication

## Register

### Actor

Guest

### Goal

Create a new user account.

### Preconditions

* Email is not already registered.

### Main Flow

1. User submits registration information.
2. System validates the data.
3. Password is encrypted.
4. User account is created.
5. User receives a successful response.

### Alternative Flow

* Email already exists.
* Invalid input data.

### Postconditions

* User account is successfully created.

---

## Login

### Actor

Guest

### Goal

Authenticate a user.

### Preconditions

* User account exists.
* User account is active.

### Main Flow

1. User enters email and password.
2. System validates credentials.
3. Authentication tokens are generated.
4. User is logged in.

### Alternative Flow

* Invalid credentials.
* Inactive account.

### Postconditions

* User receives authentication tokens.

---

## Logout

### Actor

Authenticated User

### Goal

End the current session.

### Preconditions

* User is authenticated.

### Main Flow

1. User requests logout.
2. Authentication token is revoked.
3. Session is terminated.

### Postconditions

* User is logged out.

---

# Workspace

## Create Workspace

### Actor

Authenticated User

### Goal

Create a new workspace.

### Preconditions

* User is authenticated.

### Main Flow

1. User enters workspace information.
2. System validates the request.
3. Workspace is created.
4. User becomes the workspace owner.

### Alternative Flow

* Workspace title already exists.

### Postconditions

* Workspace is successfully created.

---

## Update Workspace

## Delete Workspace

## View Workspace

---

# Workspace Members

## Invite Member

### Actor

Workspace Admin

### Goal

Invite a new member to the workspace.

### Preconditions

* User has administrator permission.

### Main Flow

1. Admin enters member email.
2. Invitation token is generated.
3. Invitation is stored.
4. Invitation is sent.

### Alternative Flow

* User is already a member.
* Invitation already exists.

### Postconditions

* Invitation is waiting for acceptance.

---

## Accept Invitation

---

## Reject Invitation

---

## Remove Member

---

## Change Member Role

---

# Project

## Create Project

### Actor

Workspace Member

### Goal

Create a project.

### Preconditions

* User belongs to the workspace.

### Main Flow

1. User enters project information.
2. System validates the request.
3. Project is created.

### Alternative Flow

* Duplicate project name.

### Postconditions

* Project is successfully created.

---

## Update Project

---

## Archive Project

---

## Delete Project

---

# Sprint

## Create Sprint

---

## Update Sprint

---

## Start Sprint

---

## Complete Sprint

---

## Delete Sprint

---

# Task

## Create Task

### Actor

Workspace Member

### Goal

Create a new task.

### Preconditions

* User belongs to the workspace.
* Project exists.
* User has permission.

### Main Flow

1. User selects a project.
2. User enters task information.
3. System validates the request.
4. Task is created.
5. Activity log is created.
6. Notification is generated (if applicable).

### Alternative Flow

* Invalid input.
* Project does not exist.
* User has insufficient permissions.

### Postconditions

* Task is successfully created.

---

# Task

## Update Task

### Actor

Workspace Member

### Goal

Update an existing task.

### Preconditions

* Task exists.
* User has permission to edit the task.

### Main Flow

1. User opens the task.
2. User modifies one or more fields.
3. System validates the changes.
4. Task information is updated.
5. Activity log is recorded.

### Alternative Flow

* Task does not exist.
* User does not have permission.
* Invalid input data.

### Postconditions

* Task information is successfully updated.

---

## Delete Task

### Actor

Workspace Member

### Goal

Delete an existing task.

### Preconditions

* Task exists.
* User has delete permission.

### Main Flow

1. User selects a task.
2. User confirms deletion.
3. System removes the task.
4. Related entities are removed according to business rules.
5. Activity log is created.

### Alternative Flow

* Task does not exist.
* User has insufficient permission.

### Postconditions

* Task is permanently deleted.

---

## Assign Task

### Actor

Workspace Member

### Goal

Assign a task to another workspace member.

### Preconditions

* Task exists.
* Assigned user belongs to the same workspace.

### Main Flow

1. User selects a task.
2. User selects an assignee.
3. System validates membership.
4. Task assignment is updated.
5. Notification is sent.
6. Activity log is created.

### Alternative Flow

* Selected user is not a workspace member.
* Task does not exist.

### Postconditions

* Task is assigned successfully.

---

## Change Task Status

### Actor

Workspace Member

### Goal

Move a task to another status.

### Preconditions

* Task exists.
* Target status exists.

### Main Flow

1. User selects a new status.
2. System validates the transition.
3. Task status is updated.
4. Status history is recorded.
5. Activity log is created.
6. Notification is generated if necessary.

### Alternative Flow

* Invalid status.
* User has insufficient permission.

### Postconditions

* Task status is successfully updated.

---

## Change Task Priority

### Actor

Workspace Member

### Goal

Update the task priority.

### Preconditions

* Task exists.

### Main Flow

1. User selects a priority.
2. System validates the request.
3. Priority is updated.
4. Activity log is created.

### Alternative Flow

* Invalid priority.

### Postconditions

* Task priority is successfully updated.

---

## Move Task

### Actor

Workspace Member

### Goal

Move a task within the project board.

### Preconditions

* Task exists.

### Main Flow

1. User drags the task.
2. System updates the task position.
3. Activity log is recorded.

### Alternative Flow

* Invalid destination.

### Postconditions

* Task position is updated.

---

## Set Due Date

### Actor

Workspace Member

### Goal

Set or update a task due date.

### Preconditions

* Task exists.

### Main Flow

1. User selects a due date.
2. System validates the date.
3. Due date is saved.
4. Activity log is recorded.

### Alternative Flow

* Invalid date.

### Postconditions

* Due date is updated.

---

## Estimate Task

### Actor

Workspace Member

### Goal

Estimate the required work time.

### Preconditions

* Task exists.

### Main Flow

1. User enters the estimated time.
2. System validates the value.
3. Estimate is stored.
4. Activity log is created.

### Alternative Flow

* Invalid estimation value.

### Postconditions

* Estimated time is updated.

---

# Label

## Create Label

### Actor

Workspace Member

### Goal

Create a new label.

### Preconditions

* User belongs to the workspace.

### Main Flow

1. User enters label information.
2. System validates uniqueness.
3. Label is created.

### Alternative Flow

* Duplicate label name.

### Postconditions

* Label is successfully created.

---

## Update Label

### Actor

Workspace Member

### Goal

Update label information.

### Preconditions

* Label exists.

### Main Flow

1. User edits the label.
2. System validates changes.
3. Label is updated.

### Alternative Flow

* Duplicate label name.

### Postconditions

* Label information is updated.

---

## Delete Label

### Actor

Workspace Member

### Goal

Delete a label.

### Preconditions

* Label exists.

### Main Flow

1. User selects the label.
2. System removes label associations.
3. Label is deleted.

### Alternative Flow

* Label does not exist.

### Postconditions

* Label is removed.

---

## Assign Label to Task

### Actor

Workspace Member

### Goal

Assign a label to a task.

### Preconditions

* Task exists.
* Label exists.

### Main Flow

1. User selects a task.
2. User selects a label.
3. System creates the relationship.

### Alternative Flow

* Label already assigned.

### Postconditions

* Label is attached to the task.

---

## Remove Label from Task

### Actor

Workspace Member

### Goal

Remove a label from a task.

### Preconditions

* Task has the selected label.

### Main Flow

1. User removes the label.
2. System deletes the relationship.

### Alternative Flow

* Label is not attached.

### Postconditions

* Label is removed from the task.

---

# Comment

## Add Comment

### Actor

Workspace Member

### Goal

Add a comment to a task.

### Preconditions

* Task exists.

### Main Flow

1. User writes a comment.
2. System stores the comment.
3. Notification is generated if needed.
4. Activity log is created.

### Postconditions

* Comment is added.

---

## Reply to Comment

### Actor

Workspace Member

### Goal

Reply to an existing comment.

### Preconditions

* Parent comment exists.

### Main Flow

1. User selects a comment.
2. User writes a reply.
3. System stores the reply.

### Postconditions

* Reply is created.

---

## Edit Comment

### Actor

Workspace Member

### Goal

Modify an existing comment.

### Preconditions

* Comment belongs to the user.

### Main Flow

1. User edits the comment.
2. System saves the changes.

### Postconditions

* Comment is updated.

---

## Delete Comment

### Actor

Workspace Member

### Goal

Delete a comment.

### Preconditions

* User has permission.

### Main Flow

1. User selects a comment.
2. System removes it.

### Postconditions

* Comment is deleted.

---

# Attachment

## Upload Attachment

### Actor

Workspace Member

### Goal

Upload a file to a task.

### Preconditions

* Task exists.

### Main Flow

1. User selects a file.
2. System validates the file.
3. File is uploaded.
4. Attachment record is created.

### Alternative Flow

* Unsupported file type.
* File exceeds allowed size.

### Postconditions

* Attachment is available.

---

## Delete Attachment

### Actor

Workspace Member

### Goal

Delete an uploaded attachment.

### Preconditions

* Attachment exists.

### Main Flow

1. User selects an attachment.
2. System deletes the file.
3. Attachment record is removed.

### Postconditions

* Attachment is deleted.

---

# Notification

## View Notifications

### Actor

Authenticated User

### Goal

View personal notifications.

### Preconditions

* User is authenticated.

### Main Flow

1. User opens the notification page.
2. System retrieves notifications.
3. Notifications are displayed.

### Postconditions

* Notifications are visible.

---

## Mark Notification as Read

### Actor

Authenticated User

### Goal

Mark a notification as read.

### Preconditions

* Notification exists.

### Main Flow

1. User selects a notification.
2. System updates the `read_at` field.

### Postconditions

* Notification is marked as read.
