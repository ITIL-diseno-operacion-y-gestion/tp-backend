"""cambiar_fecha_de_alta_a_datetime

Revision ID: 8385f6d8e555
Revises: 97834b4cd94a
Create Date: 2024-09-29 15:33:20.254046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '8385f6d8e555'
down_revision: Union[str, None] = '97834b4cd94a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"UPDATE articulos SET fecha_de_alta = '{datetime.now()}';")
    op.alter_column("articulos", "fecha_de_alta", type_=sa.DateTime, postgresql_using='fecha_de_alta::timestamp')
    pass


def downgrade() -> None:
    op.alter_column("articulos", "fecha_de_alta", type_=sa.String(50))
    pass
