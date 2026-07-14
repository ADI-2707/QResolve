# QResolve Authentication Design

**Version:** 1.0

**Status:** Approved

**Last Updated:** July 14, 2026

---

# 1. Overview

QResolve uses an organization-centric authentication system designed for enterprise environments.

Users belong to organizations, not to the platform globally.

Authentication verifies:

* Identity
* Organization membership
* Account status
* Assigned role

Authorization is handled separately through Role-Based Access Control (RBAC).

---

# 2. Design Principles

The authentication system follows these principles:

* Invitation-only organization membership
* Organization isolation by design
* Secure password storage
* Stateless API authentication using JWT
* Refresh token support
* Secure session management
* Audit logging for all authentication events

---

# 3. Organization Registration

Anyone can create a new organization.

Registration requires:

* Organization name
* Organization slug
* Administrator name
* Administrator email
* Password

Upon successful registration:

1. A new organization is created.
2. The first user is created.
3. The first user is assigned the `ORG_ADMIN` role.
4. Default departments and settings are initialized.
5. The administrator is signed in.

Organization slugs are globally unique and cannot be changed after creation.

---

# 4. User Invitations

Organizations do not allow public user registration.

Only an `ORG_ADMIN` can invite users.

Each invitation contains:

* Email address
* Assigned role
* Optional department
* Expiration time
* Secure invitation token

Invitation links are:

* Single use
* Time limited
* Cryptographically secure

After accepting an invitation, the invited user sets their password and activates their account.

---

# 5. Login Flow

Users log in using:

* Organization slug
* Email address
* Password

Authentication process:

1. Validate organization slug.
2. Locate organization.
3. Verify user belongs to the organization.
4. Verify account status.
5. Verify password hash.
6. Generate access token.
7. Generate refresh token.
8. Record login event in the audit log.
9. Return authenticated session.

Users cannot authenticate without a valid organization slug.

---

# 6. Session Architecture

Authentication uses JWT.

Two token types are issued:

## Access Token

Purpose:

Authenticate API requests.

Characteristics:

* Short-lived
* Included in the `Authorization` header
* Contains organization and role claims

---

## Refresh Token

Purpose:

Obtain a new access token.

Characteristics:

* Longer lifetime
* Stored securely
* Can be revoked
* Rotated after use

---

# 7. JWT Claims

Access tokens contain:

* user_id
* organization_id
* organization_slug
* role
* issued_at
* expires_at

No sensitive information is stored inside the token.

---

# 8. Password Policy

Passwords must satisfy:

* Minimum length of 12 characters
* Uppercase letter
* Lowercase letter
* Number
* Special character

Passwords are stored using a strong password hashing algorithm (e.g. Argon2 or bcrypt).

Passwords are never reversible.

---

# 9. Password Reset

Users may request a password reset.

Process:

1. User submits email.
2. System verifies account.
3. Secure reset token is generated.
4. Reset email is sent.
5. User chooses a new password.
6. Existing refresh tokens are revoked.
7. Audit event is recorded.

Reset tokens are:

* Single use
* Time limited
* Cryptographically secure

---

# 10. Email Verification

The first organization administrator verifies their email during organization creation.

Invited users verify ownership of their email when accepting an invitation.

Accounts remain inactive until verification is complete.

---

# 11. Logout

Logout invalidates the current refresh token.

Access tokens expire naturally.

Logout events are recorded in the audit log.

---

# 12. Account Status

A user account may be in one of the following states:

* Pending Invitation
* Active
* Suspended
* Locked
* Archived

Only active accounts may authenticate.

---

# 13. Account Lockout

To reduce brute-force attacks:

* Failed login attempts are tracked.
* Accounts are temporarily locked after repeated failures.
* Lockouts expire automatically or may be cleared by an `ORG_ADMIN`.

Every lockout event is audited.

---

# 14. Organization Isolation

Every authenticated request carries the organization context.

The backend derives the organization from the authenticated token.

Clients never send an `organization_id` in API requests.

All queries are automatically scoped to the authenticated organization.

Attempts to access another organization's data are rejected.

---

# 15. Audit Events

The following authentication events are recorded:

* Organization registration
* Invitation created
* Invitation accepted
* Login success
* Login failure
* Logout
* Password reset requested
* Password changed
* Account locked
* Account unlocked
* Email verified

Audit logs are immutable.

---

# 16. Authentication Flow

```text
Visitor
    │
    ▼
Organization Registration
    │
    ▼
ORG_ADMIN Created
    │
    ▼
Administrator Login
    │
    ▼
Invite Employees
    │
    ▼
Invitation Email
    │
    ▼
Accept Invitation
    │
    ▼
Set Password
    │
    ▼
Email Verification
    │
    ▼
Authenticated Session
```

---

# 17. Security Considerations

The authentication system enforces:

* HTTPS in production
* Secure password hashing
* JWT expiration
* Refresh token rotation
* Token revocation
* Invitation expiration
* Password complexity
* Audit logging
* Organization isolation
* Session invalidation after password reset

---

# 18. Summary

QResolve authenticates users as members of organizations rather than as standalone platform users.

Organization registration is public, but user membership is invitation-only.

This approach ensures strong tenant isolation, enterprise-grade security, and a clear separation between authentication and authorization.

This document serves as the authoritative reference for implementing the authentication subsystem.
