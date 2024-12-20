"""crear tabla usuarios

Revision ID: 3bb62d5a3c22
Revises:
Create Date: 2024-09-26 04:12:50.136060

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3bb62d5a3c22"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String(50), nullable=False),
        sa.Column("apellido", sa.String(50), nullable=False),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("contrasenia", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("usuarios")
