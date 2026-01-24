from database.db import engine, Base
from models.user import User

print(Base.metadata.tables.keys())  # 👈 add this
Base.metadata.create_all(bind=engine)