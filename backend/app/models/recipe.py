from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .recipe_ingredient import RecipeIngredient
    from .recipe_step import RecipeStep


class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = (
        CheckConstraint(
            "prep_time_minutes IS NULL OR prep_time_minutes >= 0",
            name="ck_recipes_prep_time_nonnegative",
        ),
        CheckConstraint(
            "cook_time_minutes IS NULL OR cook_time_minutes >= 0",
            name="ck_recipes_cook_time_nonnegative",
        ),
        CheckConstraint(
            "servings IS NULL OR servings > 0",
            name="ck_recipes_servings_positive",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(2048))
    prep_time_minutes: Mapped[int | None] = mapped_column(Integer)
    cook_time_minutes: Mapped[int | None] = mapped_column(Integer)
    servings: Mapped[int | None] = mapped_column(Integer)
    cuisine: Mapped[str | None] = mapped_column(String(100), index=True)

    steps: Mapped[list[RecipeStep]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStep.step_number",
    )
    recipe_ingredients: Mapped[list[RecipeIngredient]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
