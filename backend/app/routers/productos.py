from typing import Annotated, List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.schemas.producto import (
    ProductoCategoriaCreate,
    ProductoCreate,
    ProductoIngredienteCreate,
    ProductoRead,
    ProductoUpdate,
)
from app.services import producto_service

router = APIRouter(prefix="/productos", tags=["Productos"])

IdProducto = Annotated[int, Path(gt=0, description="ID del producto")]


# ─── CRUD de Producto ──────────────────────────────────────────────────────────

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate):
    return producto_service.crear_producto(datos)


@router.get("/", response_model=List[ProductoRead])
def listar_productos(
    skip: Annotated[int, Query(ge=0, description="Registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de resultados")] = 10,
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    disponible: Annotated[Optional[bool], Query(description="Filtrar por disponibilidad")] = None,
):
    return producto_service.obtener_productos(skip, limit, nombre, disponible)


@router.get("/{id}", response_model=ProductoRead)
def detalle_producto(id: IdProducto):
    producto = producto_service.obtener_producto(id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto


@router.patch("/{id}", response_model=ProductoRead)
def actualizar_producto(datos: ProductoUpdate, id: IdProducto):
    producto = producto_service.actualizar_producto(id, datos)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: IdProducto):
    encontrado = producto_service.eliminar_producto(id)
    if not encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )


# ─── Gestión de categorías del producto (ProductoCategoria N:N) ────────────────

@router.post(
    "/{id}/categorias",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar categoría a un producto",
)
def agregar_categoria(datos: ProductoCategoriaCreate, id: IdProducto):
    producto = producto_service.agregar_categoria(id, datos)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto o categoría no encontrado",
        )
    return producto


@router.delete(
    "/{id}/categorias/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Quitar categoría de un producto",
)
def quitar_categoria(
    id: IdProducto,
    cat_id: Annotated[int, Path(gt=0, description="ID de la categoría a quitar")],
):
    encontrado = producto_service.quitar_categoria(id, cat_id)
    if not encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vínculo producto-categoría no encontrado",
        )


# ─── Gestión de ingredientes del producto (ProductoIngrediente N:N) ────────────

@router.post(
    "/{id}/ingredientes",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar ingrediente a un producto",
)
def agregar_ingrediente(datos: ProductoIngredienteCreate, id: IdProducto):
    producto = producto_service.agregar_ingrediente(id, datos)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto o ingrediente no encontrado",
        )
    return producto


@router.delete(
    "/{id}/ingredientes/{ing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Quitar ingrediente de un producto",
)
def quitar_ingrediente(
    id: IdProducto,
    ing_id: Annotated[int, Path(gt=0, description="ID del ingrediente a quitar")],
):
    encontrado = producto_service.quitar_ingrediente(id, ing_id)
    if not encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vínculo producto-ingrediente no encontrado",
        )
