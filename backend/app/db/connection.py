"""
Configuración de conexión a PostgreSQL
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.dependencies import Settings

def get_database_url(settings: 'Settings') -> str:
    """
    Construir URL de conexión a PostgreSQL
    """
    protocol = "postgresql+psycopg2"
    if settings.enable_ssl:
        protocol += "?sslmode=require"
    
    return f"{protocol}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

def test_connection():
    """
    Probar conexión a la base de datos
    """
    try:
        from app.dependencies import get_engine
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return True, "Conexión exitosa"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"
