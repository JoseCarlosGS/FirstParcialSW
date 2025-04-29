from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# Configuración de la conexión a la base de datos PostgreSQL
#DATABASE_URL = "postgresql://postgres:postgres@db:5432/wsio"
DATABASE_URL = "postgresql://wsio_owner:npg_MOWmTiLU8Np4@ep-autumn-dream-a40h1j7p-pooler.us-east-1.aws.neon.tech/wsio?sslmode=require"


# Crear el engine de SQLModel
engine = create_engine(DATABASE_URL)

# Función para inicializar la base de datos
def init_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]