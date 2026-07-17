from app.main import app


def test_domain_routes_are_exposed_under_api_v1():
    paths = app.openapi()["paths"]

    assert "/api/v1/auth/login" in paths
    assert "/api/v1/tickets" in paths
    assert "/api/v1/analytics/tickets/overview" in paths
    assert "/tickets" not in paths
