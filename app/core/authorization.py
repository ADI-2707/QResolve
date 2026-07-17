from dataclasses import dataclass

from fastapi import HTTPException, status

from app.models import Membership, Organization, User
from app.models.membership import MembershipRole


@dataclass(frozen=True)
class AuthenticatedSession:
    user: User
    organization: Organization
    membership: Membership

    @property
    def role(self) -> MembershipRole:
        return self.membership.role


def require_role(
    session: AuthenticatedSession,
    *allowed_roles: MembershipRole,
) -> None:
    if session.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
