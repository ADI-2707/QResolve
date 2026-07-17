from sqlalchemy.orm import Session

from app.models import Prediction, Ticket, TicketPriority
from app.predictor import predict_priority_with_confidence


MODEL_VERSION = "tfidf-random-forest-v1"


class TicketPredictionService:
    def __init__(self, db: Session):
        self.db = db

    def predict(self, ticket: Ticket, department_name: str | None) -> Prediction:
        prediction_input = {
            "text": f"{ticket.subject}\n\n{ticket.description}",
            "type": ticket.category.value,
            "queue": department_name or "Unassigned",
            "tag_1": ticket.category.value,
            "tag_2": "Unknown",
            "tag_3": "Unknown",
            "tag_4": "Unknown",
        }
        priority, confidence = predict_priority_with_confidence(prediction_input)
        prediction = Prediction(
            organization_id=ticket.organization_id,
            ticket_id=ticket.id,
            text=prediction_input["text"],
            type=prediction_input["type"],
            queue=prediction_input["queue"],
            tag_1=prediction_input["tag_1"],
            tag_2=prediction_input["tag_2"],
            tag_3=prediction_input["tag_3"],
            tag_4=prediction_input["tag_4"],
            predicted_priority=priority,
            predicted_department=department_name,
            confidence_score=confidence,
            model_version=MODEL_VERSION,
        )
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def override(
        self,
        prediction: Prediction,
        ticket: Ticket,
        *,
        priority: TicketPriority,
        department_id: str | None,
        overridden_by: str,
    ) -> Prediction:
        if prediction.overridden:
            raise ValueError("This prediction has already been overridden")

        ticket.priority = priority
        if department_id is not None:
            ticket.department_id = department_id
        prediction.overridden = True
        prediction.overridden_by = overridden_by
        self.db.commit()
        self.db.refresh(prediction)
        return prediction
