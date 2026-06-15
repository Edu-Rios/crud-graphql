from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from api.schema import schema
from api import models
from api.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Inventario GraphQL")

# --- NUEVO: Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que tu Vue (u otros puertos) se conecten
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "El servidor está corriendo."}