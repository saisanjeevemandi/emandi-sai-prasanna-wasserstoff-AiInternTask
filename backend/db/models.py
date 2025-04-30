# backend/db/models.py

# backend/db/models.py

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# ✅ Declare Base at the top level
Base = declarative_base()

# ✅ Your table
class GuessCounter(Base):
    __tablename__ = "guess_counter"

    word = Column(String, primary_key=True, index=True)
    count = Column(Integer, default=1)
