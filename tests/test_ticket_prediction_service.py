from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models
from app.db.database import Base
from app.models import (
    Organization,
    Ticket,
    TicketCategory,
    TicketPriority,
    User,
    UserStatus,
)
from app.services.ticket_prediction_service import TicketPredictionService


def test_ticket_prediction_service_persists_ticket_scoped_prediction(monkeypatch):
    monkeypatch.setattr(
        "app.services.ticket_prediction_service.predict_priority_with_confidence",
        lambda _: ("HIGH", 0.91),
    )
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    try:
        organization = Organization(name="Acme", slug="acme-predictions")
        db.add(organization)
        db.flush()
        user = User(
            organization_id=organization.id,
            first_name="Ada",
            last_name="Agent",
            email="prediction-agent@example.com",
            password_hash="not-used",
            status=UserStatus.ACTIVE,
        )
        db.add(user)
        db.flush()
        ticket = Ticket(
            organization_id=organization.id,
            created_by=user.id,
            subject="Login issue",
            description="The customer cannot sign in after resetting a password.",
            priority=TicketPriority.MEDIUM,
            category=TicketCategory.ACCOUNT,
        )
        db.add(ticket)
        db.commit()

        prediction = TicketPredictionService(db).predict(ticket, "Technical Support")
        overridden = TicketPredictionService(db).override(
            prediction,
            ticket,
            priority=TicketPriority.CRITICAL,
            department_id=None,
            overridden_by=user.id,
        )

        assert prediction.ticket_id == ticket.id
        assert prediction.organization_id == organization.id
        assert overridden.predicted_priority == "HIGH"
        assert overridden.confidence_score == 0.91
        assert overridden.model_version == "tfidf-random-forest-v1"
        assert overridden.overridden is True
        assert overridden.overridden_by == user.id
        assert ticket.priority == TicketPriority.CRITICAL
    finally:
        db.close()
