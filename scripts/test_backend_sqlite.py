#!/usr/bin/env python3
"""
Script para probar la conexión del backend con SQLite
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.dependencies import get_engine, get_db, get_settings
from app.db.schema import get_database_schema

def test_backend_sqlite():
    """Probar conexión del backend con SQLite"""
    print("🔍 PROBANDO BACKEND CON SQLite")
    print("=" * 50)
    
    try:
        # Probar configuración
        settings = get_settings()
        print(f"✅ Configuración cargada:")
        print(f"   Tipo de BD: {settings.db_type}")
        print(f"   Ruta BD: {settings.db_path}")
        print(f"   Ollama Host: {settings.ollama_host}")
        print(f"   Modelo: {settings.ollama_model}")
        
        # Probar motor de base de datos
        engine = get_engine()
        print(f"\n✅ Motor de SQLite creado")
        
        # Probar conexión
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT sqlite_version();"))
            version = result.fetchone()[0]
            print(f"✅ Conectado a SQLite version: {version}")
        
        # Probar sesión
        db = next(get_db())
        print(f"✅ Sesión de base de datos creada")
        
        # Probar esquema
        schema = get_database_schema(db)
        print(f"\n✅ Esquema obtenido ({len(schema)} caracteres)")
        
        # Mostrar resumen del esquema
        lines = schema.split('\n')
        for line in lines[:20]:  # Primeras 20 líneas
            print(f"   {line}")
        if len(lines) > 20:
            print(f"   ... ({len(lines) - 20} líneas más)")
        
        # Probar consulta simple
        from sqlalchemy import text
        result = db.execute(text("SELECT COUNT(*) FROM activities"))
        count = result.fetchone()[0]
        print(f"\n✅ Consulta de prueba exitosa: {count} actividades")
        
        # Probar consulta de KPIs
        result = db.execute(text("SELECT SUM(amount) FROM activities"))
        total = result.fetchone()[0]
        print(f"✅ Valor total actividades: ${total:,.2f}")
        
        result = db.execute(text("SELECT COUNT(*) FROM contracts"))
        contracts = result.fetchone()[0]
        print(f"✅ Total contratos: {contracts}")
        
        result = db.execute(text("SELECT COUNT(*) FROM profiles"))
        users = result.fetchone()[0]
        print(f"✅ Total usuarios: {users}")
        
        result = db.execute(text("SELECT COUNT(*) FROM gateways"))
        gateways = result.fetchone()[0]
        print(f"✅ Total gateways: {gateways}")
        
        db.close()
        
        print(f"\n🎉 ¡BACKEND CONECTADO EXITOSAMENTE!")
        print(f"📁 Base de datos: {settings.db_path}")
        print(f"🤖 Ollama: {settings.ollama_host}")
        print(f"🧠 Modelo: {settings.ollama_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ollama_connection():
    """Probar conexión a Ollama"""
    print("\n🤖 PROBANDO CONEXIÓN A OLLAMA")
    print("=" * 50)
    
    try:
        import requests
        
        settings = get_settings()
        ollama_url = f"{settings.ollama_host}/api/tags"
        
        response = requests.get(ollama_url, timeout=5)
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama conectado en: {settings.ollama_host}")
            print(f"📋 Modelos disponibles:")
            
            for model in models.get('models', []):
                name = model.get('name', 'Unknown')
                size = model.get('size', 0)
                size_mb = size / (1024 * 1024) if size > 0 else 0
                print(f"   - {name} ({size_mb:.1f} MB)")
            
            # Verificar si el modelo phi3:mini está disponible
            model_names = [model.get('name', '') for model in models.get('models', [])]
            if 'phi3:mini' in model_names:
                print(f"✅ Modelo phi3:mini disponible")
            else:
                print(f"⚠️ Modelo phi3:mini no encontrado")
                print(f"💡 Modelos disponibles: {', '.join(model_names)}")
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ No se puede conectar a Ollama en {settings.ollama_host}")
        print(f"💡 Asegúrate de que Ollama esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 PRUEBA COMPLETA DEL BACKEND HIDRO")
    print("=" * 60)
    
    # Probar SQLite
    sqlite_ok = test_backend_sqlite()
    
    # Probar Ollama
    ollama_ok = test_ollama_connection()
    
    print(f"\n📊 RESUMEN DE PRUEBAS:")
    print(f"   SQLite: {'✅ OK' if sqlite_ok else '❌ ERROR'}")
    print(f"   Ollama: {'✅ OK' if ollama_ok else '❌ ERROR'}")
    
    if sqlite_ok and ollama_ok:
        print(f"\n🎉 ¡TODO LISTO PARA EL CHAT!")
        print(f"💡 Para iniciar el backend:")
        print(f"   cd backend && python -m uvicorn app.main:app --reload")
        print(f"💡 Para iniciar el frontend:")
        print(f"   cd frontend && npm run dev")
    else:
        print(f"\n⚠️ Hay problemas que resolver:")
        if not sqlite_ok:
            print(f"   - Verificar base de datos SQLite")
        if not ollama_ok:
            print(f"   - Verificar que Ollama esté ejecutándose")

if __name__ == "__main__":
    main()
