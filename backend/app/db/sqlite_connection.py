"""
Configuración de conexión a SQLite para HIDRO Chat
"""
import sqlite3
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

def get_sqlite_database_url() -> str:
    """
    Construir URL de conexión a SQLite
    """
    return "sqlite:///./hidro_data.db"

def get_sqlite_engine():
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
SQLiteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_sqlite_engine())

def get_sqlite_db():
    """Dependency para obtener sesión de SQLite"""
    db = SQLiteSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_sqlite_connection():
    """
    Probar conexión a SQLite
    """
    try:
        conn = sqlite3.connect('hidro_data.db')
        cursor = conn.cursor()
        
        # Probar consulta básica
        cursor.execute("SELECT COUNT(*) FROM activities")
        count = cursor.fetchone()[0]
        
        conn.close()
        return True, f"Conexión exitosa. {count} actividades encontradas"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

def get_sqlite_schema():
    """
    Obtener esquema de SQLite para el contexto del LLM
    """
    try:
        conn = sqlite3.connect('hidro_data.db')
        cursor = conn.cursor()
        
        # Obtener información de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_text = "ESQUEMA DE BASE DE DATOS HIDRO (SQLite):\n\n"
        
        for table_name, in tables:
            if table_name == 'sqlite_sequence':
                continue
                
            schema_text += f"=== TABLA: {table_name.upper()} ===\n"
            
            # Obtener columnas
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                nullable = "NULL" if not_null == 0 else "NOT NULL"
                default = f" DEFAULT {default_val}" if default_val else ""
                primary = " PRIMARY KEY" if pk == 1 else ""
                schema_text += f"  - {col_name}: {col_type} {nullable}{default}{primary}\n"
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            schema_text += f"  📊 Registros: {count}\n\n"
        
        conn.close()
        return schema_text
        
    except Exception as e:
        return f"Error obteniendo esquema: {str(e)}"
