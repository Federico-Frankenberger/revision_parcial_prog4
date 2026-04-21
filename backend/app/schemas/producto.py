from typing import List, Optional
from pydantic import BaseModel, Field


# --- Schemas auxiliares para mostrar datos relacionados dentro de ProductoRead ---

class CategoriaResumen(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}


class IngredienteResumen(BaseModel):
    id: int
    nombre: str
    es_removible: bool

    model_config = {"from_attributes": True}


# --- Schema para asignar un ingrediente al crear/actualizar un producto ---

class IngredienteAsignacion(BaseModel):
    ingrediente_id: int = Field(..., gt=0)
    es_removible: bool = Field(default=False)


# --- Schemas principales de Producto ---

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, examples=["Hamburguesa clásica"])
    descripcion: Optional[str] = Field(default=None, examples=["Pan brioche, carne 200g, lechuga"])
    precio_base: float = Field(..., ge=0, examples=[1500.00])
    stock_cantidad: int = Field(default=0, ge=0, examples=[50])
    disponible: bool = Field(default=True)


class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = Field(default_factory=list, examples=[[1, 2]])
    ingredientes: List[IngredienteAsignacion] = Field(default_factory=list)


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[float] = Field(default=None, ge=0)
    stock_cantidad: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    stock_cantidad: int
    disponible: bool
    categorias: List[CategoriaResumen] = []
    ingredientes: List[IngredienteResumen] = []

    model_config = {"from_attributes": True}


# --- Schemas para gestionar los vínculos N:N desde sus propios endpoints ---

class ProductoCategoriaCreate(BaseModel):
    categoria_id: int = Field(..., gt=0)


class ProductoIngredienteCreate(BaseModel):
    ingrediente_id: int = Field(..., gt=0)
    es_removible: bool = Field(default=False)
