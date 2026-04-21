from contextlib import asynccontextmanager
from fastapi import FastAPI

# Importar modelos para que SQLModel.metadata los registre antes de crear las tablas
import app.models  # noqa: F401

from app.database import crear_tablas
from app.routers import categorias, ingredientes, productos


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(
    title="API Parcial 1 - Catálogo de Productos",
    description="Backend del parcial integrador — FastAPI + SQLModel + PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(categorias.router)
app.include_router(ingredientes.router)
app.include_router(productos.router)
