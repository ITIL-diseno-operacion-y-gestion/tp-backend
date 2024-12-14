"""crear rol de usuarios

Revision ID: e61b1d97c60a
Revises: 805e87971297
Create Date: 2024-11-04 23:07:42.461100

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e61b1d97c60a"
down_revision: Union[str, None] = "805e87971297"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "usuarios",
        sa.Column("rol", sa.String(50), nullable=False, server_default="cliente"),
    )


def downgrade():
    op.drop_column("usuarios", "rol")
