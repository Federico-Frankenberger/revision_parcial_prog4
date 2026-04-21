from typing import List, Optional

from sqlmodel import select

from app.models.producto import Producto
from app.models.producto_categoria import ProductoCategoria
from app.models.producto_ingrediente import ProductoIngrediente
from app.schemas.producto import (
    CategoriaResumen,
    IngredienteResumen,
    ProductoCategoriaCreate,
    ProductoCreate,
    ProductoIngredienteCreate,
    ProductoRead,
    ProductoUpdate,
)
from app.uow.uow import UnidadDeTrabajo


def _construir_producto_read(producto: Producto) -> ProductoRead:
    """Convierte un Producto (con sus relaciones cargadas) al schema de salida."""
    categorias = [
        CategoriaResumen(id=link.categoria_id, nombre=link.categoria.nombre)
        for link in producto.categorias_link
    ]
    ingredientes = [
        IngredienteResumen(
            id=link.ingrediente_id,
            nombre=link.ingrediente.nombre,
            es_removible=link.es_removible,
        )
        for link in producto.ingredientes_link
    ]
    return ProductoRead(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_base=producto.precio_base,
        stock_cantidad=producto.stock_cantidad,
        disponible=producto.disponible,
        categorias=categorias,
        ingredientes=ingredientes,
    )


def crear_producto(datos: ProductoCreate) -> ProductoRead:
    with UnidadDeTrabajo() as uow:
        producto = Producto(
            nombre=datos.nombre,
            descripcion=datos.descripcion,
            precio_base=datos.precio_base,
            stock_cantidad=datos.stock_cantidad,
            disponible=datos.disponible,
        )
        uow.sesion.add(producto)
        uow.sesion.flush()  # Necesario para obtener el ID antes de crear los vínculos

        for cat_id in datos.categoria_ids:
            uow.sesion.add(ProductoCategoria(producto_id=producto.id, categoria_id=cat_id))

        for asignacion in datos.ingredientes:
            uow.sesion.add(
                ProductoIngrediente(
                    producto_id=producto.id,
                    ingrediente_id=asignacion.ingrediente_id,
                    es_removible=asignacion.es_removible,
                )
            )

        uow.sesion.flush()
        uow.sesion.refresh(producto)
        return _construir_producto_read(producto)


def obtener_productos(
    skip: int = 0,
    limit: int = 10,
    nombre: Optional[str] = None,
    disponible: Optional[bool] = None,
) -> List[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        consulta = select(Producto)
        if nombre:
            consulta = consulta.where(Producto.nombre.icontains(nombre))
        if disponible is not None:
            consulta = consulta.where(Producto.disponible == disponible)
        consulta = consulta.offset(skip).limit(limit)
        productos = uow.sesion.exec(consulta).all()
        return [_construir_producto_read(p) for p in productos]


def obtener_producto(id: int) -> Optional[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        producto = uow.sesion.get(Producto, id)
        if not producto:
            return None
        return _construir_producto_read(producto)


def actualizar_producto(id: int, datos: ProductoUpdate) -> Optional[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        producto = uow.sesion.get(Producto, id)
        if not producto:
            return None
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(producto, campo, valor)
        uow.sesion.add(producto)
        uow.sesion.flush()
        uow.sesion.refresh(producto)
        return _construir_producto_read(producto)


def eliminar_producto(id: int) -> bool:
    with UnidadDeTrabajo() as uow:
        producto = uow.sesion.get(Producto, id)
        if not producto:
            return False
        uow.sesion.delete(producto)  # El cascade elimina los vínculos automáticamente
        return True


# --- Gestión de vínculos N:N (ProductoCategoria y ProductoIngrediente) ---

def agregar_categoria(id_producto: int, datos: ProductoCategoriaCreate) -> Optional[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        producto = uow.sesion.get(Producto, id_producto)
        if not producto:
            return None
        vinculo = ProductoCategoria(producto_id=id_producto, categoria_id=datos.categoria_id)
        uow.sesion.add(vinculo)
        uow.sesion.flush()
        uow.sesion.refresh(producto)
        return _construir_producto_read(producto)


def quitar_categoria(id_producto: int, id_categoria: int) -> bool:
    with UnidadDeTrabajo() as uow:
        vinculo = uow.sesion.get(ProductoCategoria, (id_producto, id_categoria))
        if not vinculo:
            return False
        uow.sesion.delete(vinculo)
        return True


def agregar_ingrediente(
    id_producto: int, datos: ProductoIngredienteCreate
) -> Optional[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        producto = uow.sesion.get(Producto, id_producto)
        if not producto:
            return None
        vinculo = ProductoIngrediente(
            producto_id=id_producto,
            ingrediente_id=datos.ingrediente_id,
            es_removible=datos.es_removible,
        )
        uow.sesion.add(vinculo)
        uow.sesion.flush()
        uow.sesion.refresh(producto)
        return _construir_producto_read(producto)


def quitar_ingrediente(id_producto: int, id_ingrediente: int) -> bool:
    with UnidadDeTrabajo() as uow:
        vinculo = uow.sesion.get(ProductoIngrediente, (id_producto, id_ingrediente))
        if not vinculo:
            return False
        uow.sesion.delete(vinculo)
        return True
