import strawberry
from typing import Optional
from .types import Product, Category
from .database import SessionLocal
from .models import ProductModel, CategoryModel

@strawberry.type
class Mutation:
    
    # --- 1. Crear Categoría ---
    @strawberry.mutation
    def create_category(self, name: str) -> Category:
        db = SessionLocal()
        try:
            new_category = CategoryModel(name=name)
            db.add(new_category)
            db.commit()
            db.refresh(new_category) # Obtenemos el ID generado por PostgreSQL
            
            return Category(id=new_category.id, name=new_category.name)
        finally:
            db.close()

    # --- 2. Crear Producto ---
    @strawberry.mutation
    def create_product(self, name: str, price: float, stock: int, category_id: int) -> Product:
        db = SessionLocal()
        try:
            new_product = ProductModel(
                name=name, price=price, stock=stock, category_id=category_id
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            
            cat = Category(id=new_product.category.id, name=new_product.category.name) if new_product.category else None
            return Product(id=new_product.id, name=new_product.name, price=new_product.price, stock=new_product.stock, category=cat)
        finally:
            db.close()

    # --- 3. Registrar Venta (Actualizar Stock) ---
    @strawberry.mutation
    def register_sale(self, product_id: int, quantity: int) -> Optional[Product]:
        db = SessionLocal()
        try:
            # Buscamos el producto en la DB
            product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
            
            if not product:
                raise Exception("Producto no encontrado")
            
            if product.stock >= quantity:
                # Restamos el stock y guardamos en PostgreSQL
                product.stock -= quantity
                db.commit()
                db.refresh(product)
                
                cat = Category(id=product.category.id, name=product.category.name) if product.category else None
                return Product(id=product.id, name=product.name, price=product.price, stock=product.stock, category=cat)
            else:
                raise Exception("Stock insuficiente")
        finally:
            db.close()
    
    # --- 4. Actualizar Producto (Update) ---
    @strawberry.mutation
    def update_product(self, product_id: int, name: str, price: float, stock: int) -> Optional[Product]:
        db = SessionLocal()
        try:
            product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
            if not product:
                raise Exception("Producto no encontrado")
            
            # Actualizamos los valores
            product.name = name
            product.price = price
            product.stock = stock
            db.commit()
            db.refresh(product)
            
            cat = Category(id=product.category.id, name=product.category.name) if product.category else None
            return Product(id=product.id, name=product.name, price=product.price, stock=product.stock, category=cat)
        finally:
            db.close()

    # --- 5. Eliminar Producto (Delete) ---
    @strawberry.mutation
    def delete_product(self, product_id: int) -> bool:
        db = SessionLocal()
        try:
            product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
            if not product:
                return False
            
            db.delete(product)
            db.commit()
            return True
        finally:
            db.close()