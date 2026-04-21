from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .producto_categoria import ProductoCategoria
    from .producto_ingrediente import ProductoIngrediente


class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = Field(default=None)
    precio_base: float = Field(ge=0)
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

    # Relación 1:N hacia la tabla intermedia ProductoCategoria (N:N con Categoria)
    categorias_link: List["ProductoCategoria"] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    # Relación 1:N hacia la tabla intermedia ProductoIngrediente (N:N con Ingrediente)
    ingredientes_link: List["ProductoIngrediente"] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
