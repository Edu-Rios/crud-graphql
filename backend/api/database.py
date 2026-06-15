import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

# Obtenemos la URL de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creamos una fábrica de sesiones para interactuar con los datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta clase base la heredarán nuestros modelos para mapear las tablas
Base = declarative_base()

# Función útil para abrir y cerrar la sesión automáticamente en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()