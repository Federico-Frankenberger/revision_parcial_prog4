from typing import Annotated, List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorías"])

# Tipo reutilizable para el parámetro ID en la URL
IdCategoria = Annotated[int, Path(gt=0, description="ID de la categoría")]


@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CategoriaCreate):
    return categoria_service.crear_categoria(datos)


@router.get("/", response_model=List[CategoriaRead])
def listar_categorias(
    skip: Annotated[int, Query(ge=0, description="Registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de resultados")] = 10,
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
):
    return categoria_service.obtener_categorias(skip, limit, nombre)


@router.get("/{id}", response_model=CategoriaRead)
def detalle_categoria(id: IdCategoria):
    categoria = categoria_service.obtener_categoria(id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


@router.patch("/{id}", response_model=CategoriaRead)
def actualizar_categoria(datos: CategoriaUpdate, id: IdCategoria):
    categoria = categoria_service.actualizar_categoria(id, datos)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(id: IdCategoria):
    try:
        encontrada = categoria_service.eliminar_categoria(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
