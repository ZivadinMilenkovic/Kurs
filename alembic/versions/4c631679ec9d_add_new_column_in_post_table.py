"""add new column in post table

Revision ID: 4c631679ec9d
Revises: a38f475d7001
Create Date: 2024-03-14 14:26:24.560522

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c631679ec9d"
down_revision: Union[str, None] = "a38f475d7001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
