# QResolve Authorization Matrix

**Version:** 1.0

**Status:** Approved

**Last Updated:** July 14, 2026

---

# 1. Overview

QResolve uses Role-Based Access Control (RBAC) to authorize users after successful authentication.

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

Every authenticated request is evaluated against the user's assigned role before access is granted.

---

# 2. Design Principles

Authorization follows these principles:

* Least privilege
* Organization isolation
* Explicit permissions
* Deny by default
* Audit privileged actions
* Backend-enforced security

The frontend may hide unavailable actions, but **all authorization decisions are enforced by the backend**.

---

# 3. Role Hierarchy

```text
PLATFORM_ADMIN
        │
        ▼
--------------------------------
(Platform Boundary)
--------------------------------
        │
        ▼
ORG_ADMIN
        │
        ▼
MANAGER
        │
        ▼
AGENT
        │
        ▼
VIEWER
```

Platform roles never belong to an organization.

Organization roles always belong to exactly one organization.

---

# 4. Platform Administrator

Purpose:

Manage the entire QResolve platform.

Platform administrators are internal QResolve personnel.

Capabilities:

* View all organizations
* Create platform administrators
* Archive organizations
* Restore organizations
* View global audit logs
* View platform analytics
* Monitor system health
* Manage AI model versions
* Manage feature flags
* View platform usage statistics

Restrictions:

* Cannot impersonate users
* Cannot modify organization business data
* Cannot change customer tickets unless using explicit support tooling

---

# 5. Organization Administrator

Purpose:

Manage one organization.

Capabilities:

* Invite users
* Manage users
* Suspend users
* Assign roles
* Manage departments
* View organization audit logs
* Configure organization settings
* Reassign tickets
* View analytics
* Configure AI preferences

Restrictions:

* Cannot access another organization.
* Cannot perform platform administration.

---

# 6. Manager

Purpose:

Supervise operational work.

Capabilities:

* View all organization tickets
* Assign tickets
* Reassign tickets
* Review AI predictions
* View reports
* Resolve escalations
* View department metrics

Restrictions:

* Cannot invite users.
* Cannot change organization settings.
* Cannot manage permissions.

---

# 7. Agent

Purpose:

Handle support tickets.

Capabilities:

* View assigned tickets
* View unassigned ticket queue
* Claim tickets
* Update ticket status
* Add comments
* Upload attachments
* Resolve assigned tickets
* Override AI predictions (with audit logging)

Restrictions:

* Cannot manage users.
* Cannot access audit logs.
* Cannot change organization configuration.

---

# 8. Viewer

Purpose:

Read-only organizational access.

Capabilities:

* View permitted dashboards
* View tickets
* View analytics
* View reports

Restrictions:

* Cannot modify tickets.
* Cannot claim tickets.
* Cannot resolve tickets.
* Cannot change any data.

---

# 9. Permission Matrix

| Permission                   | PLATFORM_ADMIN | ORG_ADMIN | MANAGER |    AGENT    |     VIEWER    |
| ---------------------------- | :------------: | :-------: | :-----: | :---------: | :-----------: |
| View Platform Dashboard      |        ✓       |     ✗     |    ✗    |      ✗      |       ✗       |
| View Organizations           |        ✓       |     ✗     |    ✗    |      ✗      |       ✗       |
| Archive Organization         |        ✓       |     ✗     |    ✗    |      ✗      |       ✗       |
| Restore Organization         |        ✓       |     ✗     |    ✗    |      ✗      |       ✗       |
| View Global Audit Logs       |        ✓       |     ✗     |    ✗    |      ✗      |       ✗       |
| Invite Users                 |        ✗       |     ✓     |    ✗    |      ✗      |       ✗       |
| Manage Users                 |        ✗       |     ✓     |    ✗    |      ✗      |       ✗       |
| Assign Roles                 |        ✗       |     ✓     |    ✗    |      ✗      |       ✗       |
| Manage Departments           |        ✗       |     ✓     |    ✗    |      ✗      |       ✗       |
| Configure Organization       |        ✗       |     ✓     |    ✗    |      ✗      |       ✗       |
| View Organization Audit Logs |        ✗       |     ✓     |    ✗    |      ✗      |       ✗       |
| View All Tickets             |        ✗       |     ✓     |    ✓    |      ✗      | ✓ (read-only) |
| Claim Ticket                 |        ✗       |     ✓     |    ✓    |      ✓      |       ✗       |
| Assign Ticket                |        ✗       |     ✓     |    ✓    |      ✗      |       ✗       |
| Reassign Ticket              |        ✗       |     ✓     |    ✓    |      ✗      |       ✗       |
| Resolve Ticket               |        ✗       |     ✓     |    ✓    |      ✓      |       ✗       |
| Override AI Prediction       |        ✗       |     ✓     |    ✓    |      ✓      |       ✗       |
| Upload Attachment            |        ✗       |     ✓     |    ✓    |      ✓      |       ✗       |
| View Analytics               |        ✓       |     ✓     |    ✓    | ✓ (limited) |  ✓ (limited)  |

---

# 10. Resource Ownership

Every protected resource belongs to exactly one organization.

Examples:

* User
* Department
* Ticket
* Comment
* Attachment
* Prediction
* Audit Log
* Settings

Before any action is performed, the backend verifies:

1. User is authenticated.
2. User belongs to the resource's organization.
3. User has the required permission.
4. Resource is active.

---

# 11. Authorization Flow

```text
Incoming Request
        │
        ▼
Validate JWT
        │
        ▼
Load User
        │
        ▼
Determine Organization
        │
        ▼
Load Role
        │
        ▼
Check Permission
        │
        ▼
Permission Granted?
      /     \
    Yes      No
     │        │
     ▼        ▼
 Continue   Return 403 Forbidden
```

---

# 12. Audit Requirements

The following actions must generate audit events:

* User invitations
* Role assignments
* Department changes
* Organization settings updates
* Ticket assignment
* Ticket reassignment
* AI overrides
* User suspension
* Organization archival
* Organization restoration

Audit records include:

* Actor
* Timestamp
* Organization
* Action
* Target resource
* Metadata

---

# 13. Future Roles

The authorization model is designed to support additional roles without structural changes.

Examples:

* Auditor
* Billing Administrator
* AI Reviewer
* Compliance Officer
* Read-only Executive
* Integration Service Account
* API Client

These roles inherit no permissions by default and must be explicitly configured.

---

# 14. Summary

QResolve uses a hierarchical Role-Based Access Control model that separates platform administration from organization administration.

Every authorization decision is enforced on the backend, scoped to the authenticated organization, and recorded through audit logging where appropriate.

This document serves as the authoritative reference for implementing permissions throughout the platform.
