"""Create recipe data model.

Revision ID: 20260813_0001
Revises:
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260813_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ingredients_name"),
        "ingredients",
        ["name"],
        unique=True,
    )

    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("prep_time_minutes", sa.Integer(), nullable=True),
        sa.Column("cook_time_minutes", sa.Integer(), nullable=True),
        sa.Column("servings", sa.Integer(), nullable=True),
        sa.Column("cuisine", sa.String(length=100), nullable=True),
        sa.CheckConstraint(
            "cook_time_minutes IS NULL OR cook_time_minutes >= 0",
            name="ck_recipes_cook_time_nonnegative",
        ),
        sa.CheckConstraint(
            "prep_time_minutes IS NULL OR prep_time_minutes >= 0",
            name="ck_recipes_prep_time_nonnegative",
        ),
        sa.CheckConstraint(
            "servings IS NULL OR servings > 0",
            name="ck_recipes_servings_positive",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recipes_cuisine"), "recipes", ["cuisine"])
    op.create_index(op.f("ix_recipes_title"), "recipes", ["title"])

    op.create_table(
        "recipe_ingredients",
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=10, scale=3), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "quantity IS NULL OR quantity > 0",
            name="ck_recipe_ingredients_quantity_positive",
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("recipe_id", "ingredient_id"),
    )
    op.create_index(
        op.f("ix_recipe_ingredients_ingredient_id"),
        "recipe_ingredients",
        ["ingredient_id"],
    )

    op.create_table(
        "recipe_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("step_number", sa.Integer(), nullable=False),
        sa.Column("instruction", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "step_number > 0",
            name="ck_recipe_steps_step_number_positive",
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "recipe_id",
            "step_number",
            name="uq_recipe_steps_recipe_step_number",
        ),
    )
    op.create_index(
        op.f("ix_recipe_steps_recipe_id"),
        "recipe_steps",
        ["recipe_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_recipe_steps_recipe_id"), table_name="recipe_steps")
    op.drop_table("recipe_steps")
    op.drop_index(
        op.f("ix_recipe_ingredients_ingredient_id"),
        table_name="recipe_ingredients",
    )
    op.drop_table("recipe_ingredients")
    op.drop_index(op.f("ix_recipes_title"), table_name="recipes")
    op.drop_index(op.f("ix_recipes_cuisine"), table_name="recipes")
    op.drop_table("recipes")
    op.drop_index(op.f("ix_ingredients_name"), table_name="ingredients")
    op.drop_table("ingredients")
