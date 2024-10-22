"""crear_tabla_articulos_incidentes

Revision ID: 05a944b76ed9
Revises: fb83ff82c21b
Create Date: 2024-10-22 01:19:48.936170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "05a944b76ed9"
down_revision: Union[str, None] = "fb83ff82c21b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "articulos_incidentes",
        sa.Column(
            "id_articulo",
            sa.Integer,
            sa.ForeignKey("articulos.id"),
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
    op.drop_table("articulos_incidentes")
