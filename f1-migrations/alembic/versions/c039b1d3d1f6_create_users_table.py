"""create users table

Revision ID: c039b1d3d1f6
Revises: 
Create Date: 2026-07-30 18:44:12.625424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c039b1d3d1f6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password", sa.String(60), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")