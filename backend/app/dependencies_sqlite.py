"""
Dependencias y configuración para SQLite
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.sqlite_connection import get_sqlite_database_url, get_sqlite_engine

class SQLiteSettings(BaseSettings):
    """Configuración para SQLite"""
    
    # Base de datos SQLite
    db_type: str = "sqlite"
    db_path: str = "./hidro_data.db"
    
    # LLM
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "phi3:mini"
    
    # Seguridad
    enable_ssl: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_sqlite_settings():
    """Obtener configuración SQLite (cached)"""
    return SQLiteSettings()

# Configurar motor de SQLite
def get_engine():
    """Crear motor de SQLAlchemy para SQLite"""
    database_url = get_sqlite_database_url()
    
    engine = create_engine(
        database_url,
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        echo=True  # Habilitar logs SQL detallados
    )
    return engine

# Session factory para SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_db():
    """Dependency para obtener sesión de SQLite"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
