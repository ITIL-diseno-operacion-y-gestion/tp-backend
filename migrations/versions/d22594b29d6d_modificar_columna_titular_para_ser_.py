"""modificar_columna_titular_para_ser_foreign_key

Revision ID: d22594b29d6d
Revises: 0ac6020eec1b
Create Date: 2024-10-19 12:41:40.128392

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "d22594b29d6d"
down_revision: Union[str, None] = "0ac6020eec1b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE articulos SET titular = 1;")
    op.alter_column(
        "articulos",
        "titular",
        nullable=False,
        new_column_name="id_titular",
        type_=sa.Integer,
        postgresql_using="titular::integer",
    )
    op.create_foreign_key(
        "fk_titular_articulo", "articulos", "usuarios", ["id_titular"], ["id"]
    )


def downgrade() -> None:
    op.alter_column("articulos", "titular", type_=sa.String(50))
    op.drop_constraint("fk_titular_articulo", "articulos", type_="foreignkey")
