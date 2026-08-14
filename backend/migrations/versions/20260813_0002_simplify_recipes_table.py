"""Simplify recipes to a single table.

Revision ID: 20260813_0002
Revises: 20260813_0001
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260813_0002"
down_revision: Union[str, None] = "20260813_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("recipe_ingredients")
    op.drop_table("recipe_steps")
    op.drop_table("ingredients")

    op.drop_index(op.f("ix_recipes_cuisine"), table_name="recipes")
    op.drop_index(op.f("ix_recipes_title"), table_name="recipes")

    op.add_column(
        "recipes",
        sa.Column(
            "ingredients",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "recipes",
        sa.Column(
            "instructions",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "recipes",
        sa.Column(
            "image_name",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "recipes",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.alter_column(
        "recipes",
        "title",
        existing_type=sa.String(length=255),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.alter_column(
        "recipes",
        "image_url",
        existing_type=sa.String(length=2048),
        type_=sa.Text(),
        existing_nullable=True,
    )

    op.drop_column("recipes", "description")
    op.drop_column("recipes", "prep_time_minutes")
    op.drop_column("recipes", "cook_time_minutes")
    op.drop_column("recipes", "servings")
    op.drop_column("recipes", "cuisine")

    op.alter_column("recipes", "ingredients", server_default=None)
    op.alter_column("recipes", "instructions", server_default=None)
    op.alter_column("recipes", "image_name", server_default=None)


def downgrade() -> None:
    op.add_column("recipes", sa.Column("description", sa.Text(), nullable=True))
    op.add_column(
        "recipes",
        sa.Column("prep_time_minutes", sa.Integer(), nullable=True),
    )
    op.add_column(
        "recipes",
        sa.Column("cook_time_minutes", sa.Integer(), nullable=True),
    )
    op.add_column("recipes", sa.Column("servings", sa.Integer(), nullable=True))
    op.add_column(
        "recipes",
        sa.Column("cuisine", sa.String(length=100), nullable=True),
    )

    op.create_check_constraint(
        "ck_recipes_prep_time_nonnegative",
        "recipes",
        "prep_time_minutes IS NULL OR prep_time_minutes >= 0",
    )
    op.create_check_constraint(
        "ck_recipes_cook_time_nonnegative",
        "recipes",
        "cook_time_minutes IS NULL OR cook_time_minutes >= 0",
    )
    op.create_check_constraint(
        "ck_recipes_servings_positive",
        "recipes",
        "servings IS NULL OR servings > 0",
    )

    op.alter_column(
        "recipes",
        "title",
        existing_type=sa.Text(),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        "recipes",
        "image_url",
        existing_type=sa.Text(),
        type_=sa.String(length=2048),
        existing_nullable=True,
    )
    op.create_index(op.f("ix_recipes_title"), "recipes", ["title"])
    op.create_index(op.f("ix_recipes_cuisine"), "recipes", ["cuisine"])

    op.drop_column("recipes", "created_at")
    op.drop_column("recipes", "image_name")
    op.drop_column("recipes", "instructions")
    op.drop_column("recipes", "ingredients")

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
            ["recipe_id"], ["recipes.id"], ondelete="CASCADE"
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

    op.create_table(
        "recipe_ingredients",
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 3), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "quantity IS NULL OR quantity > 0",
            name="ck_recipe_ingredients_quantity_positive",
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"], ["ingredients.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"], ["recipes.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("recipe_id", "ingredient_id"),
    )
    op.create_index(
        op.f("ix_recipe_ingredients_ingredient_id"),
        "recipe_ingredients",
        ["ingredient_id"],
    )
