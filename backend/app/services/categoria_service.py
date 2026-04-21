from typing import List, Optional

from sqlmodel import select

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from app.uow.uow import UnidadDeTrabajo


def crear_categoria(datos: CategoriaCreate) -> CategoriaRead:
    with UnidadDeTrabajo() as uow:
        categoria = Categoria(**datos.model_dump())
        uow.sesion.add(categoria)
        uow.sesion.flush()
        uow.sesion.refresh(categoria)
        return CategoriaRead.model_validate(categoria)


def obtener_categorias(
    skip: int = 0,
    limit: int = 10,
    nombre: Optional[str] = None,
) -> List[CategoriaRead]:
    with UnidadDeTrabajo() as uow:
        consulta = select(Categoria)
        if nombre:
            consulta = consulta.where(Categoria.nombre.icontains(nombre))
        consulta = consulta.offset(skip).limit(limit)
        categorias = uow.sesion.exec(consulta).all()
        return [CategoriaRead.model_validate(c) for c in categorias]


def obtener_categoria(id: int) -> Optional[CategoriaRead]:
    with UnidadDeTrabajo() as uow:
        categoria = uow.sesion.get(Categoria, id)
        if not categoria:
            return None
        return CategoriaRead.model_validate(categoria)


def actualizar_categoria(id: int, datos: CategoriaUpdate) -> Optional[CategoriaRead]:
    with UnidadDeTrabajo() as uow:
        categoria = uow.sesion.get(Categoria, id)
        if not categoria:
            return None
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(categoria, campo, valor)
        uow.sesion.add(categoria)
        uow.sesion.flush()
        uow.sesion.refresh(categoria)
        return CategoriaRead.model_validate(categoria)


def eliminar_categoria(id: int) -> bool:
    with UnidadDeTrabajo() as uow:
        categoria = uow.sesion.get(Categoria, id)
        if not categoria:
            return False
        if categoria.productos_link:
            raise ValueError("No se puede eliminar: la categoría tiene productos asociados")
        uow.sesion.delete(categoria)
        return True
