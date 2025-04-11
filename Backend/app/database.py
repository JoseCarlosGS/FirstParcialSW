from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# Configuración de la conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://postgres:71194970@localhost:5432/1erparcialSW1"

# Crear el engine de SQLModel
engine = create_engine(DATABASE_URL)

# Función para inicializar la base de datos
def init_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]