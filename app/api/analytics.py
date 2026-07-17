from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.core.authorization import AuthenticatedSession
from app.db.database import get_db
from app.schemas.analytics import TicketAnalyticsResponse
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/tickets/overview", response_model=TicketAnalyticsResponse)
def ticket_overview(
    db: Session = Depends(get_db),
    session: AuthenticatedSession = Depends(get_current_session),
):
    return AnalyticsService(db).ticket_overview(session.organization.id)
