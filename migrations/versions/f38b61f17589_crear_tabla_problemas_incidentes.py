"""crear_tabla_problemas_incidentes

Revision ID: f38b61f17589
Revises: 421bff6e2680
Create Date: 2024-10-18 13:10:00.259579

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f38b61f17589"
down_revision: Union[str, None] = "421bff6e2680"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "problemas_incidentes",
        sa.Column(
            "id_problema",
            sa.Integer,
            sa.ForeignKey("problemas.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "id_incidente",
            sa.Integer,
            sa.ForeignKey("incidentes.id"),
            primary_key=True,
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("problemas_incidentes")
