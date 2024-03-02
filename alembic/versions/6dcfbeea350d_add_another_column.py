"""add another column

Revision ID: 6dcfbeea350d
Revises: b3480332422d
Create Date: 2024-03-02 14:52:06.931394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dcfbeea350d'
down_revision: Union[str, None] = 'b3480332422d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
