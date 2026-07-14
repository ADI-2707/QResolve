# QResolve Database Design

**Version:** 1.0

**Status:** Approved

**Last Updated:** July 14, 2026

---

# 1. Overview

QResolve uses a relational database designed around a multi-tenant architecture.

Every organization has complete logical isolation while sharing a single application instance. All organization-owned resources reference an `organization_id`, and every backend query must be scoped to the authenticated user's organization.

Development uses SQLite.

Production uses PostgreSQL.

---

# 2. Design Principles

The database is designed around the following principles:

* Multi-tenant by design
* Normalized relationships
* Strong referential integrity
* Immutable audit history
* Soft deletion for recoverable resources
* UUID primary keys for production (SQLite may use integers during development)
* Automatic timestamps

---

# 3. Core Entities

The platform consists of the following core entities.

```text
Organization
│
├── Users
│     ├── Roles
│     └── Invitations
│
├── Departments
│
├── Tickets
│     ├── Predictions
│     ├── Comments
│     └── Attachments
│
├── Audit Logs
│
└── Organization Settings
```

---

# 4. Entity Descriptions

## Organization

Represents a company using QResolve.

Fields:

* id
* name
* slug (globally unique)
* status
* subscription_plan
* created_at
* archived_at
* deleted_at

Rules:

* Slug is immutable after creation.
* Organizations never share data.
* Archived organizations become read-only.
* Soft deletion occurs after the retention period.

---

## User

Represents an employee within an organization.

Fields:

* id
* organization_id
* role_id
* department_id
* first_name
* last_name
* email
* password_hash
* status
* last_login
* created_at
* updated_at

Rules:

* Email is unique within an organization.
* Authentication always validates organization membership.
* Passwords are never stored in plain text.

---

## Role

Defines permissions.

Examples:

* ORG_ADMIN
* MANAGER
* AGENT
* VIEWER

Roles contain only permission definitions.

They do not contain users directly.

---

## Department

Represents operational departments.

Examples:

* Technical Support
* Billing
* Sales
* Customer Success

Departments are organization-specific.

---

## Invitation

Represents an invitation sent by an organization administrator.

Fields:

* id
* organization_id
* email
* role_id
* token
* expires_at
* accepted_at
* created_by

Rules:

* Invitation links expire.
* Invitations are single use.
* Public registration into existing organizations is not allowed.

---

## Ticket

Represents a customer support request.

Fields:

* id
* organization_id
* department_id
* created_by
* assigned_to
* title
* description
* priority
* category
* status
* source
* created_at
* updated_at
* resolved_at

Rules:

* Tickets initially remain unassigned.
* Agents claim tickets.
* Organization administrators may reassign tickets.
* Every ticket belongs to exactly one organization.

---

## Prediction

Stores AI-generated predictions.

Fields:

* id
* ticket_id
* predicted_priority
* predicted_department
* confidence_score
* model_version
* overridden
* overridden_by

Purpose:

Track AI decisions independently from human decisions.

---

## Comment

Internal discussion attached to a ticket.

Fields:

* id
* ticket_id
* user_id
* content
* created_at

Comments are internal only.

Customers cannot access them.

---

## Attachment

Represents uploaded files associated with a ticket.

Examples:

* Images
* PDFs
* Log files

Metadata is stored in the database.

Binary files are stored separately.

---

## Audit Log

Stores immutable security and operational events.

Fields:

* id
* organization_id
* actor_id
* action
* entity_type
* entity_id
* metadata
* created_at

Audit records are never modified.

---

## Organization Settings

Stores organization-level configuration.

Examples:

* Branding
* Default ticket priority
* Time zone
* Business hours
* AI preferences

---

# 5. Relationship Diagram

```text
Organization
│
├── Users
│     ├── Role
│     └── Department
│
├── Departments
│
├── Invitations
│
├── Tickets
│     ├── Predictions
│     ├── Comments
│     └── Attachments
│
├── Audit Logs
│
└── Organization Settings
```

---

# 6. Multi-Tenant Isolation

Every organization-owned table includes an `organization_id`.

Examples:

* users
* departments
* invitations
* tickets
* predictions
* comments
* attachments
* audit_logs
* organization_settings

Every API request must automatically scope queries using the authenticated user's organization.

Clients must never provide an organization identifier in API requests.

The backend derives the organization from the authenticated session.

---

# 7. Soft Deletion Strategy

The following entities support soft deletion:

* Organization
* User
* Department
* Ticket

Soft deletion uses a `deleted_at` timestamp.

Deleted records remain recoverable until the retention policy expires.

Audit logs are never deleted.

---

# 8. Timestamp Strategy

Every primary entity includes:

* created_at
* updated_at

Additional timestamps are used where applicable:

* last_login
* accepted_at
* archived_at
* resolved_at
* deleted_at

All timestamps are stored in UTC.

---

# 9. Future Expansion

The schema is designed to support future additions without major redesign.

Planned modules include:

* SLA management
* Workflow automation
* Notification center
* Email ingestion
* Customer portal
* Knowledge base
* AI conversation assistant
* Analytics warehouse
* Model version history
* API keys
* Webhooks
* Integrations

---

# 10. Summary

The database architecture provides:

* Strong tenant isolation
* Enterprise-grade security
* Extensible domain model
* AI prediction tracking
* Complete auditability
* Long-term maintainability

This document serves as the authoritative reference for all database models, migrations, and repository implementations within QResolve.
