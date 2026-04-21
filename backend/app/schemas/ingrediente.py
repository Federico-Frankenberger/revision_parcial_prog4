from typing import Optional
from pydantic import BaseModel, Field


class IngredienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, examples=["Queso cheddar"])
    descripcion: Optional[str] = Field(default=None, examples=["Queso cheddar fundido"])


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = None


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    model_config = {"from_attributes": True}
