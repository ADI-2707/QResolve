from app.main import app


def test_direct_user_creation_route_is_not_exposed():
    paths = app.openapi()["paths"]

    assert "/users" not in paths
