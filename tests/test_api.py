from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Welcome to QResolve API"
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_predict_endpoint_success():
    payload = {
        "text": "Customer cannot login after password reset.",
        "type": "Technical issue",
        "queue": "Support",
        "tag_1": "Authentication",
        "tag_2": "Login",
        "tag_3": "Password Reset",
        "tag_4": "Account",
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "priority" in data
    assert isinstance(data["priority"], str)


def test_predict_endpoint_validation_error():
    response = client.post(
        "/predict",
        json={},
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "Validation Error"
    assert "details" in data


def test_predict_endpoint_defaults():
    payload = {
        "text": "Unable to access account.",
        "type": "Technical issue",
        "queue": "Support",
        "tag_1": "Authentication",
    }

    response = client.post(
        "/predict",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "priority" in data


def test_prediction_history_endpoint():

    response = client.get(
        "/predictions"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list,
    )