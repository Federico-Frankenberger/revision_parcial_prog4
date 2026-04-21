from sqlmodel import Session
from app.database import motor


class UnidadDeTrabajo:
    """
    Contexto de trabajo que encapsula la sesión de base de datos.
    Al salir del bloque 'with', hace commit automático si no hubo errores,
    o rollback si ocurrió una excepción.
    """

    def __enter__(self) -> "UnidadDeTrabajo":
        self.sesion = Session(motor)
        return self

    def __exit__(self, tipo_exc, valor_exc, traza_exc):
        if tipo_exc:
            self.sesion.rollback()
        else:
            self.sesion.commit()
        self.sesion.close()
