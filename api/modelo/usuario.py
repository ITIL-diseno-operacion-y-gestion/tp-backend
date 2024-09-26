from sqlmodel import SQLModel, Field


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str
    contrasenia: str
