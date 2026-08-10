"""create favorites table

Revision ID: e7099676d49d
Revises: c039b1d3d1f6
Create Date: 2026-07-31 15:40:48.344184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7099676d49d'
down_revision: Union[str, Sequence[str], None] = 'c039b1d3d1f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "favorites",
        sa.Column("favorites_id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("list_name", sa.String(60), nullable=False),
         sa.Column("item_id", sa.String(255), nullable=False),
        sa.Column("item_type", sa.String(60), nullable=False),
        sa.Column("item_name", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(
                ["user_id"], ["users.user_id"],
                name="fk_favorites_users",
                ),
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("favorites")