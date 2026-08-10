"""adding role and account_status column to users table

Revision ID: f34d731b468b
Revises: e7099676d49d
Create Date: 2026-08-09 00:06:17.255962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f34d731b468b'
down_revision: Union[str, Sequence[str], None] = 'e7099676d49d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('role', sa.String(50), server_default='user', nullable=False))
    op.add_column('users', sa.Column('account_status', sa.String(20), server_default='active', nullable=False)) 

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    op.drop_column('users', 'account_status')