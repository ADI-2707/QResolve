from datetime import datetime

from pydantic import BaseModel

from app.models import MembershipRole, MembershipStatus


class MembershipResponse(BaseModel):
    id: str
    organization_id: str
    user_id: str
    role: MembershipRole
    status: MembershipStatus
    created_at: datetime
    accepted_at: datetime | None


class MembershipRoleUpdate(BaseModel):
    role: MembershipRole
