"""modificar_tabla_tickets

Revision ID: 7941d8eaedbb
Revises: e09aeb65d6d5
Create Date: 2024-10-13 12:55:42.686533

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = "7941d8eaedbb"
down_revision: Union[str, None] = "e09aeb65d6d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("tickets", "incidentes")
    op.execute("ALTER SEQUENCE tickets_id_seq RENAME TO incidentes_id_seq")
    op.execute("ALTER INDEX tickets_pkey RENAME TO incidentes_pkey")
    op.execute(f"UPDATE incidentes SET fecha_de_alta = '{datetime.now()}';")
    op.alter_column(
        "incidentes",
        "fecha_de_alta",
        type_=sa.DateTime,
        postgresql_using="fecha_de_alta::timestamp",
    )


def downgrade() -> None:
    op.rename_table("incidentes", "tickets")
    op.execute("ALTER SEQUENCE incidentes_id_seq RENAME TO tickets_id_seq")
    op.execute("ALTER INDEX incidentes_pkey RENAME TO tickets_pkey")
    op.alter_column("tickets", "fecha_de_alta", type_=sa.String(50))
