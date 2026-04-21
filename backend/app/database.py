import os
from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/parcial_db")

motor = create_engine(DATABASE_URL, echo=True)


def crear_tablas():
    SQLModel.metadata.create_all(motor)
