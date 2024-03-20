"""Add column type and expire

Revision ID: ec1f668a4ae2
Revises: 0e11b062cf3a
Create Date: 2024-03-20 13:15:09.796547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec1f668a4ae2'
down_revision: Union[str, None] = '0e11b062cf3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('type_of_post', sa.String(), server_default='text', nullable=False))
    op.add_column('posts', sa.Column('expire', sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'expire')
    op.drop_column('posts', 'type_of_post')
    # ### end Alembic commands ###
