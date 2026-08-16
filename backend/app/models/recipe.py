from sqlalchemy import Column, DateTime, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from ..database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    ingredients = Column(JSONB, nullable=False)
    instructions = Column(Text, nullable=False)
    image_name = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    embedding = Column(Vector(1024), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
