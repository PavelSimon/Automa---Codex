"""baseline

Revision ID: 0001_baseline
Revises: 
Create Date: 2025-09-20
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Baseline: application creates tables on startup via SQLModel
    pass


def downgrade() -> None:
    pass

