"""msg

Revision ID: f289fcb6880d
Revises: 9c98ffd3e96b
Create Date: 2025-07-08 09:34:21.264402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f289fcb6880d'
down_revision: Union[str, Sequence[str], None] = '9c98ffd3e96b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
