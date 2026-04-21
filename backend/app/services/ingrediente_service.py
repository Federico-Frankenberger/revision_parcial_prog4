from typing import List, Optional

from sqlmodel import select

from app.models.ingrediente import Ingrediente
from app.schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate
from app.uow.uow import UnidadDeTrabajo


def crear_ingrediente(datos: IngredienteCreate) -> IngredienteRead:
    with UnidadDeTrabajo() as uow:
        ingrediente = Ingrediente(**datos.model_dump())
        uow.sesion.add(ingrediente)
        uow.sesion.flush()
        uow.sesion.refresh(ingrediente)
        return IngredienteRead.model_validate(ingrediente)


def obtener_ingredientes(
    skip: int = 0,
    limit: int = 10,
    nombre: Optional[str] = None,
) -> List[IngredienteRead]:
    with UnidadDeTrabajo() as uow:
        consulta = select(Ingrediente)
        if nombre:
            consulta = consulta.where(Ingrediente.nombre.icontains(nombre))
        consulta = consulta.offset(skip).limit(limit)
        ingredientes = uow.sesion.exec(consulta).all()
        return [IngredienteRead.model_validate(i) for i in ingredientes]


def obtener_ingrediente(id: int) -> Optional[IngredienteRead]:
    with UnidadDeTrabajo() as uow:
        ingrediente = uow.sesion.get(Ingrediente, id)
        if not ingrediente:
            return None
        return IngredienteRead.model_validate(ingrediente)


def actualizar_ingrediente(id: int, datos: IngredienteUpdate) -> Optional[IngredienteRead]:
    with UnidadDeTrabajo() as uow:
        ingrediente = uow.sesion.get(Ingrediente, id)
        if not ingrediente:
            return None
        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(ingrediente, campo, valor)
        uow.sesion.add(ingrediente)
        uow.sesion.flush()
        uow.sesion.refresh(ingrediente)
        return IngredienteRead.model_validate(ingrediente)


def eliminar_ingrediente(id: int) -> bool:
    with UnidadDeTrabajo() as uow:
        ingrediente = uow.sesion.get(Ingrediente, id)
        if not ingrediente:
            return False
        if ingrediente.productos_link:
            raise ValueError("No se puede eliminar: el ingrediente tiene productos asociados")
        uow.sesion.delete(ingrediente)
        return True
