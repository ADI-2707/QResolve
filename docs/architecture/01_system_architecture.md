# QResolve System Architecture

**Version:** 1.0

**Status:** Approved

**Last Updated:** July 14, 2026

---

# 1. Overview

QResolve is an enterprise-grade AI-powered support operations platform designed to help organizations classify, prioritize, assign, and manage customer support tickets using machine learning.

The platform follows a multi-tenant architecture where every organization operates in a completely isolated workspace while sharing the same application infrastructure.

The system consists of four major components:

* Frontend (React + TypeScript)
* Backend API (FastAPI)
* Machine Learning Engine
* Database

---

# 2. Core Principles

The architecture is built around the following principles.

## Multi-Tenancy

Every organization has complete logical isolation.

Organizations can never access another organization's:

* Users
* Tickets
* Departments
* Analytics
* Audit logs
* Settings

Isolation is enforced by the backend.

---

## Enterprise First

The product is designed to resemble enterprise internal software rather than a consumer SaaS application.

The first experience is authentication rather than marketing.

Every feature prioritizes security, auditing, maintainability, and scalability.

---

## AI Assisted

Artificial Intelligence assists users by predicting:

* Ticket Priority
* Ticket Category
* Responsible Department

Users always have the final decision.

Human overrides are stored for future model improvement.

---

## Security

Security is enforced through:

* JWT Authentication
* Organization Isolation
* Role Based Access Control
* Audit Logging
* Password Hashing
* Protected API Routes

---

# 3. High-Level Architecture

```text
                        Internet
                            │
                            ▼
                React Frontend (Vite)
                            │
                     HTTPS / REST API
                            │
                            ▼
                     FastAPI Backend
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Authentication      Business Logic      ML Prediction
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                     SQLite (Development)
                     PostgreSQL (Production)
```

---

# 4. Platform Layers

The platform contains three logical administration layers.

## Layer 1 — Platform Administration

Accessible only by QResolve platform administrators.

Responsibilities:

* Manage organizations
* Platform monitoring
* Platform analytics
* Global audit logs
* System health
* AI model management

---

## Layer 2 — Organization Administration

Accessible only by organization administrators.

Responsibilities:

* Invite users
* Manage roles
* View organization analytics
* Configure departments
* Review audit logs
* Manage organization settings

Organization administrators cannot access any other organization.

---

## Layer 3 — Organization Users

Roles include:

* Manager
* Agent
* Viewer

Users only access resources permitted by their assigned role.

---

# 5. Organization Lifecycle

```
Visitor

↓

Create Organization

↓

Organization Created

↓

ORG_ADMIN Created

↓

Invite Employees

↓

Employees Join

↓

Daily Operations

↓

Archive

↓

Retention Period

↓

Soft Delete
```

Organization slugs are permanent and globally unique.

---

# 6. Ticket Lifecycle

```
Ticket Created

↓

AI Prediction

↓

Unassigned Queue

↓

Agent Claims Ticket

↓

Assigned

↓

In Progress

↓

Resolved

↓

Closed
```

Tickets initially remain unassigned until claimed by an authorized user.

---

# 7. AI Workflow

For every ticket:

1. Extract features
2. Predict department
3. Predict priority
4. Store confidence score
5. Allow human override
6. Store override history

Predictions never replace human decisions.

---

# 8. Audit Logging

Every state-changing action generates an immutable audit event.

Examples include:

* Organization creation
* User invitation
* Login
* Ticket assignment
* Ticket resolution
* AI prediction
* Human override
* Role changes
* Department updates

Audit logs exist at:

* Platform level
* Organization level
* System level

---

# 9. Technology Stack

## Frontend

* React
* TypeScript
* Vite
* React Router
* CSS Modules

## Backend

* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## Database

Development:

* SQLite

Production:

* PostgreSQL

---

# 10. Design Goals

The architecture is designed to provide:

* Enterprise-grade scalability
* Maintainable codebase
* Clear separation of concerns
* Strong security boundaries
* Extensible AI integration
* High observability through audit logs
* Consistent user experience across organizations

This document serves as the architectural foundation for all future development within QResolve.
