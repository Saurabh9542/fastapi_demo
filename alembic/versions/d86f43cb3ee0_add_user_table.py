"""add user table

Revision ID: d86f43cb3ee0
Revises: 6dcfbeea350d
Create Date: 2024-03-02 15:00:46.999928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd86f43cb3ee0'
down_revision: Union[str, None] = '6dcfbeea350d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                               server_default=sa.text('now()'), nullable=False)
                     )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
