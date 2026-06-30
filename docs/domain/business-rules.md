# Business Rules

## Workspace

* Each workspace must have exactly one owner.
* Only the workspace owner can delete the workspace.
* A workspace owner cannot leave the workspace unless ownership is transferred.

## Membership

* A user can join a workspace only once.
* Only users with sufficient permissions can invite new members.
* A member's role determines the actions they are allowed to perform.

## Project

* Every project must belong to a workspace.
* Project names must be unique within the same workspace.
* Archived projects cannot be modified.

## Sprint

* Every sprint must belong to a project.
* A sprint cannot overlap with another active sprint in the same project.
* A sprint cannot be started after its end date.

## Task

* Every task must belong to a project.
* A task may optionally belong to a sprint.
* A task may remain unassigned.
* Only workspace members can create tasks.
* Only authorized members can update or delete tasks.
* The due date must be later than the task creation date.
* Completed tasks cannot be moved back if project policy forbids it.

## Labels

* Label names must be unique within a workspace.
* A task cannot have the same label more than once.

## Comments

* Only workspace members can add comments.
* Deleted tasks cannot receive new comments.

## Attachments

* Only workspace members can upload attachments.
* Attachments must belong to an existing task.

## Notifications

* Notifications are created automatically after specific events.
* A notification can only be marked as read by its recipient.

## Workspace Invitations

* Invitation tokens can only be used once.
* Invitations expire after their expiration date.
* An invitation cannot be accepted twice.
* A user who is already a workspace member cannot accept another invitation to the same workspace.

## Task Status History

* Every status change must be recorded.
* The previous and new status must always be stored.
* The user who changed the status must be recorded.
