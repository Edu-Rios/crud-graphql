import strawberry
from typing import Optional

@strawberry.type
class Category:
    id: int
    name: str

@strawberry.type
class Product:
    id: int
    name: str
    price: float
    stock: int
    # Relacionamos el producto directamente con su categoría
    category: Category