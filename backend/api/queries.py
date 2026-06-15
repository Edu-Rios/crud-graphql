import strawberry
from typing import List
from .types import Product, Category
from .database import SessionLocal
from .models import ProductModel, CategoryModel # Importamos CategoryModel

@strawberry.type
class Query:
    @strawberry.field
    def get_products(self) -> List[Product]:
        db = SessionLocal()
        try:
            db_products = db.query(ProductModel).all()
            result = []
            for p in db_products:
                cat = Category(id=p.category.id, name=p.category.name) if p.category else None
                result.append(Product(id=p.id, name=p.name, price=p.price, stock=p.stock, category=cat))
            return result
        finally:
            db.close()

    # --- NUEVA CONSULTA ---
    @strawberry.field
    def get_categories(self) -> List[Category]:
        db = SessionLocal()
        try:
            db_categories = db.query(CategoryModel).all()
            return [Category(id=c.id, name=c.name) for c in db_categories]
        finally:
            db.close()