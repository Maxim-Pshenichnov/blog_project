"""add_cascade_delete

Revision ID: d35afadb251f
Revises: 533e9bd4cf74
Create Date: 2025-06-04 22:56:50.432030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd35afadb251f'
down_revision: Union[str, None] = '533e9bd4cf74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
