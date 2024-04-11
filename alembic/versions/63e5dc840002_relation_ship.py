"""relation ship

Revision ID: 63e5dc840002
Revises: 1f15c2cda5ec
Create Date: 2024-03-14 14:44:09.632452

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "63e5dc840002"
down_revision: Union[str, None] = "1f15c2cda5ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    # op.drop_constraint("posts_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
