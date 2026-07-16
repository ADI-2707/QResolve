# QResolve API Specification

**Version:** 1.0

**Status:** Approved

**Last Updated:** July 14, 2026

---

# 1. Overview

QResolve exposes a versioned REST API consumed by the React frontend and future third-party integrations.

All client applications communicate exclusively through the API.

The API is designed to be:

* RESTful
* Versioned
* Secure
* Predictable
* Consistent
* Backward compatible whenever possible

---

# 2. Base URL

Development

```text
http://localhost:8000/api/v1
```

Production

```text
https://api.qresolve.com/v1
```

Every endpoint belongs to a version.

Future versions will coexist without breaking existing clients.

---

# 3. API Versioning Strategy

Current version:

```text
v1
```

Future versions:

```text
v2
v3
...
```

Breaking changes require a new API version.

Non-breaking enhancements are added to the existing version.

---

# 4. API Modules

The API is organized by domain.

```text
/api/v1
│
├── auth
├── organizations
├── users
├── invitations
├── roles
├── departments
├── tickets
├── predictions
├── comments
├── attachments
├── analytics
├── audit
├── settings
└── platform
```

Each module owns its endpoints, schemas, services, and repositories.

---

# 5. HTTP Methods

| Method | Purpose                      |
| ------ | ---------------------------- |
| GET    | Retrieve resources           |
| POST   | Create resources             |
| PUT    | Replace a resource           |
| PATCH  | Partially update a resource  |
| DELETE | Archive or delete a resource |

DELETE operations should prefer soft deletion where applicable.

---

# 6. Authentication

Protected endpoints require a JWT access token.

Example:

```http
Authorization: Bearer <access_token>
```

Authentication middleware is responsible for:

* Token validation
* User lookup
* Organization resolution
* Permission loading

Clients never send `organization_id`.

The backend derives it from the authenticated session.

---

# 7. Request Format

Requests use JSON.

Example:

```json
{
  "title": "Unable to login",
  "description": "Customer cannot access the dashboard."
}
```

---

# 8. Response Format

Successful responses follow a consistent structure.

Example:

```json
{
  "success": true,
  "data": {
    "...": "..."
  }
}
```

---

Errors follow a standard format.

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Ticket not found."
  }
}
```

Clients should rely on `error.code` for programmatic handling.

---

# 9. HTTP Status Codes

| Code | Meaning               |
| ---: | --------------------- |
|  200 | Success               |
|  201 | Created               |
|  204 | No Content            |
|  400 | Bad Request           |
|  401 | Unauthorized          |
|  403 | Forbidden             |
|  404 | Not Found             |
|  409 | Conflict              |
|  422 | Validation Error      |
|  429 | Too Many Requests     |
|  500 | Internal Server Error |

---

# 10. Pagination

List endpoints support pagination.

Example:

```text
GET /tickets?page=2&page_size=25
```

Response:

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 2,
    "page_size": 25,
    "total_items": 560,
    "total_pages": 23
  }
}
```

Default page size: **25**

Maximum page size: **100**

---

# 11. Filtering

Resources support filtering through query parameters.

Example:

```text
GET /tickets?status=open
GET /tickets?priority=high
GET /tickets?department=billing
```

Multiple filters may be combined.

---

# 12. Sorting

Sorting uses two query parameters.

```text
sort_by=created_at
sort_order=desc
```

Example:

```text
GET /tickets?sort_by=priority&sort_order=asc
```

---

# 13. Searching

Search uses a dedicated query parameter.

Example:

```text
GET /tickets?search=payment
```

Search behavior is defined per resource.

---

# 14. Route Naming Conventions

Use plural resource names.

Examples:

```text
/users
/tickets
/departments
/invitations
```

Avoid verbs in URLs.

Prefer:

```text
POST /tickets
```

Instead of:

```text
POST /createTicket
```

Actions that do not fit CRUD may use sub-resources.

Examples:

```text
POST /tickets/{id}/claim
POST /tickets/{id}/resolve
POST /tickets/{id}/comments
```

---

# 15. Idempotency

* GET requests are idempotent.
* PUT requests replace resources.
* PATCH requests partially update resources.
* DELETE requests archive resources where applicable.

Repeated requests should not produce inconsistent state.

---

# 16. Validation

All incoming data is validated using Pydantic schemas.

Validation occurs before business logic executes.

Validation failures return HTTP 422.

---

# 17. Rate Limiting

Authentication endpoints should be rate-limited.

Examples:

* Login
* Password reset
* Invitation acceptance

Rate-limiting helps reduce brute-force attacks.

---

# 18. File Uploads

Attachments use multipart form data.

Metadata is stored in the database.

Files are stored separately from relational data.

Supported file types and size limits are defined by organization settings.

---

# 19. Audit Logging

Mutating endpoints generate audit events.

Examples:

* Create
* Update
* Delete
* Assign
* Resolve
* Invite
* Suspend

Read operations are generally not audited unless required for compliance.

---

# 20. Error Handling

Errors should be:

* Human-readable
* Machine-readable
* Consistent
* Traceable

Internal implementation details must never be exposed.

Sensitive information must not appear in error messages.

---

# 21. Future API Features

The API is designed to support future capabilities, including:

* Webhooks
* API keys
* OAuth integrations
* GraphQL gateway
* Bulk operations
* Async jobs
* Streaming events
* Public integration APIs

---

# 22. Summary

The QResolve API follows consistent REST principles, strict versioning, standardized request and response formats, and organization-aware security.

This specification serves as the implementation guide for all current and future backend endpoints.
