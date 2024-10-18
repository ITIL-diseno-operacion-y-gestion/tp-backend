"""eliminar_columna_id_usuario_de_problemas

Revision ID: 0ac6020eec1b
Revises: f38b61f17589
Create Date: 2024-10-18 15:15:39.711193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0ac6020eec1b"
down_revision: Union[str, None] = "f38b61f17589"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("problemas", "id_usuario")


def downgrade() -> None:
    op.add_column(
        "problemas",
        sa.Column(
            "id_usuario", sa.Integer, sa.ForeignKey("usuarios.id"), nullable=False
        ),
    )
