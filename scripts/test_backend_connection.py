#!/usr/bin/env python3
"""
Script para probar la conexión del backend desde el directorio correcto
"""
import os
import sys
import sqlite3

def test_sqlite_direct():
    """Probar SQLite directamente"""
    print("🔍 PROBANDO SQLite DIRECTAMENTE")
    print("=" * 50)
    
    # Probar desde directorio raíz
    db_path = "hidro_data.db"
    if os.path.exists(db_path):
        print(f"✅ Base de datos encontrada en raíz: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM activities")
        count = cursor.fetchone()[0]
        print(f"✅ Actividades en raíz: {count}")
        conn.close()
    else:
        print(f"❌ Base de datos no encontrada en raíz: {db_path}")
    
    # Probar desde directorio backend
    backend_db_path = "../hidro_data.db"
    if os.path.exists(backend_db_path):
        print(f"✅ Base de datos encontrada desde backend: {backend_db_path}")
        conn = sqlite3.connect(backend_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM activities")
        count = cursor.fetchone()[0]
        print(f"✅ Actividades desde backend: {count}")
        conn.close()
    else:
        print(f"❌ Base de datos no encontrada desde backend: {backend_db_path}")

def test_backend_import():
    """Probar importación del backend"""
    print("\n🔍 PROBANDO IMPORTACIÓN DEL BACKEND")
    print("=" * 50)
    
    # Cambiar al directorio backend
    backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
    original_dir = os.getcwd()
    
    try:
        os.chdir(backend_dir)
        print(f"📁 Directorio actual: {os.getcwd()}")
        
        # Agregar el directorio backend al path
        sys.path.insert(0, backend_dir)
        
        # Importar dependencias
        from app.dependencies import get_engine, get_settings
        
        # Probar configuración
        settings = get_settings()
        print(f"✅ Configuración cargada:")
        print(f"   Ruta BD: {settings.db_path}")
        
        # Probar motor
        engine = get_engine()
        print(f"✅ Motor creado")
        
        # Probar conexión
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM activities"))
            count = result.fetchone()[0]
            print(f"✅ Actividades encontradas: {count}")
            
            # Probar otras tablas
            result = conn.execute(text("SELECT COUNT(*) FROM contracts"))
            contracts = result.fetchone()[0]
            print(f"✅ Contratos encontrados: {contracts}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM profiles"))
            profiles = result.fetchone()[0]
            print(f"✅ Usuarios encontrados: {profiles}")
        
        print(f"\n🎉 ¡CONEXIÓN EXITOSA!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir(original_dir)

def main():
    print("🚀 PRUEBA DE CONEXIÓN BACKEND-SQLite")
    print("=" * 60)
    
    # Probar SQLite directamente
    test_sqlite_direct()
    
    # Probar backend
    success = test_backend_import()
    
    if success:
        print(f"\n✅ ¡TODO FUNCIONANDO!")
        print(f"💡 Para iniciar el backend:")
        print(f"   python scripts/start_backend_sqlite.py")
    else:
        print(f"\n❌ Hay problemas que resolver")

if __name__ == "__main__":
    main()
