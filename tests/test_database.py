from sqlalchemy import inspect

from app.database import engine


def test_database_tables_exist():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "predictions" in tables