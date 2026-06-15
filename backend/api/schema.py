import strawberry
from .queries import Query
from .mutations import Mutation

# Ahora el esquema recibe tanto las consultas como las mutaciones
schema = strawberry.Schema(query=Query, mutation=Mutation)