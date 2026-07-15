from app.db.database import Base
from app.db.database import engine

import app.models

Base.metadata.create_all(bind=engine)

print("Database created successfully.")