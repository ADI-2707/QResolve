from app.core.security import create_access_token
from app.models import Membership, Organization, User
from app.schemas.session import SessionResponse


def create_session_response(
    user: User,
    organization: Organization,
    membership: Membership,
) -> SessionResponse:
    return SessionResponse(
        access_token=create_access_token(
            user.id,
            organization_id=organization.id,
            organization_slug=organization.slug,
            role=membership.role.value,
        ),
        organization_id=organization.id,
        organization_slug=organization.slug,
        role=membership.role.value,
    )
