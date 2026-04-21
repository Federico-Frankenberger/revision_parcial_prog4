# Importar todos los modelos para que SQLModel.metadata los registre al iniciar la app
from .categoria import Categoria
from .ingrediente import Ingrediente
from .producto import Producto
from .producto_categoria import ProductoCategoria
from .producto_ingrediente import ProductoIngrediente

__all__ = ["Categoria", "Ingrediente", "Producto", "ProductoCategoria", "ProductoIngrediente"]
