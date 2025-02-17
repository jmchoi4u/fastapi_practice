"""create posts and users table

Revision ID: f9278f7c0c31
Revises: 
Create Date: 2025-01-04 21:00:23.618130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f9278f7c0c31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'createtime_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.add_column('users', sa.Column('createtime_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'createtime_at')
    op.alter_column('posts', 'createtime_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
