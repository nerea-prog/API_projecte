from sqlmodel import SQLModel, Field
from typing import Optional

class Usuari(SQLModel, table=True):
    PK: Optional[int] = Field(default=None, primary_key=True)
    id_tarjeta: int = Field(foreign_key="Tarjeta.PK")
    id_rol: int = Field(foreign_key="Roles.PK")
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    correo: str
    activo: bool = True

class UsuariRequest(SQLModel):
    PK: int
    id_tarjeta: int
    id_rol: int
    apellido1: Optional[str]
    apellido2: Optional[str]
    correo: str
    activo: bool

class UsuariResponse(SQLModel):
    PK: int
    id_tarjeta: int
    id_rol: int
    apellido1: Optional[str]
    apellido2: Optional[str]
    correo: str
    activo: bool


class UsuariResponsePartial(SQLModel):
    PK: int
    apellido1: Optional[str]
    apellido2: Optional[str]
    correo: str
