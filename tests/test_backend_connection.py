#!/usr/bin/env python3
"""
Script para verificar la conexión del backend
"""
import sys
import os
sys.path.append('backend')

from backend.app.dependencies import get_settings, get_db
import psycopg2

def test_backend_connection():
    """Verificar conexión del backend"""
    try:
        print("🔍 Verificando configuración del backend...")
        
        # Obtener configuración
        settings = get_settings()
        print(f"📋 Configuración del backend:")
        print(f"  - Host: {settings.db_host}")
        print(f"  - Puerto: {settings.db_port}")
        print(f"  - Usuario: {settings.db_user}")
        print(f"  - Base: {settings.db_name}")
        print(f"  - LLM: {settings.ollama_model}")
        
        # Probar conexión directa
        print("\n🔍 Probando conexión directa...")
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            dbname=settings.db_name
        )
        print("✅ Conexión directa exitosa!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM activities;")
        count = cursor.fetchone()[0]
        print(f"📊 Actividades en {settings.db_name}: {count}")
        
        conn.close()
        
        # Probar conexión a través del backend
        print("\n🔍 Probando conexión a través del backend...")
        db = next(get_db())
        cursor = db.execute("SELECT COUNT(*) FROM activities;")
        count = cursor.fetchone()[0]
        print(f"📊 Actividades a través del backend: {count}")
        
        print("✅ Backend funcionando correctamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_backend_connection()




