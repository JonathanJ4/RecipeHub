"""Add a pgvector embedding to recipes.

Revision ID: 20260815_0003
Revises: 20260813_0002
Create Date: 2026-08-15
"""

from typing import Sequence, Union

from alembic import op
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa


revision: str = "20260815_0003"
down_revision: Union[str, None] = "20260813_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column("recipes", sa.Column("embedding", Vector(1024), nullable=True))


def downgrade() -> None:
    op.drop_column("recipes", "embedding")
