from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, hash_token, new_secure_token
from app.models import Invitation, Membership, MembershipStatus, User, UserStatus
from app.models.membership import MembershipRole
from app.repositories.invitation_repository import InvitationRepository


class InvitationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = InvitationRepository(db)

    def create(
        self,
        *,
        organization_id: str,
        email: str,
        role: MembershipRole,
        invited_by: str,
    ) -> tuple[Invitation, str]:
        if self.db.execute(select(User).where(User.email == email)).scalar_one_or_none():
            raise ValueError("A user with this email already exists")
        if self.repository.get_pending_by_email(organization_id, email):
            raise ValueError("A pending invitation already exists for this email")

        token = new_secure_token()
        invitation = Invitation(
            organization_id=organization_id,
            email=email,
            role=role,
            token_hash=hash_token(token),
            invited_by=invited_by,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation, token

    def accept(
        self,
        *,
        token: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> tuple[User, Membership]:
        invitation = self.repository.get_by_token_hash(hash_token(token))
        now = datetime.utcnow()
        if invitation is None or invitation.accepted_at is not None or invitation.expires_at < now:
            raise ValueError("Invitation is invalid or expired")
        if self.db.execute(select(User).where(User.email == invitation.email)).scalar_one_or_none():
            raise ValueError("A user with this email already exists")

        try:
            user = User(
                organization_id=invitation.organization_id,
                first_name=first_name,
                last_name=last_name,
                email=invitation.email,
                password_hash=hash_password(password),
                status=UserStatus.ACTIVE,
            )
            self.db.add(user)
            self.db.flush()
            membership = Membership(
                organization_id=invitation.organization_id,
                user_id=user.id,
                role=invitation.role,
                status=MembershipStatus.ACTIVE,
                invited_by=invitation.invited_by,
                joined_at=now,
                accepted_at=now,
            )
            invitation.accepted_at = now
            self.db.add(membership)
            self.db.commit()
            self.db.refresh(user)
            self.db.refresh(membership)
            return user, membership
        except Exception:
            self.db.rollback()
            raise
