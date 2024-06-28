"""Photo updated at

Revision ID: 8d7a2db416a1
Revises: 465f84e5c2ea
Create Date: 2024-06-28 01:39:46.112019

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8d7a2db416a1"
down_revision: Union[str, None] = "465f84e5c2ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "photos", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("photos", "updated_at")
    # ### end Alembic commands ###
