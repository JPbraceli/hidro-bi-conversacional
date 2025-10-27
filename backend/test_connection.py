#!/usr/bin/env python3
"""
Script para probar la conexión a PostgreSQL
"""
import psycopg2
from psycopg2 import sql

def test_connection():
    """Probar conexión a PostgreSQL"""
    try:
        # Intentar conectar a la base principal
        print("🔍 Probando conexión a dev_hdcr_activities...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        print("✅ Conexión exitosa a dev_hdcr_activities")
        
        # Probar consulta
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 PostgreSQL version: {version[0]}")
        
        # Listar tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        
        # Intentar conectar a 'postgres' (base por defecto)
        try:
            print("\n🔍 Probando conexión a base 'postgres'...")
            conn = psycopg2.connect(
                host='127.0.0.1',
                port=15433,
                user='hdcruser',
                password='localpass',
                dbname='postgres'
            )
            print("✅ Conexión exitosa a 'postgres'")
            
            # Listar bases de datos
            cursor = conn.cursor()
            cursor.execute("SELECT datname FROM pg_database;")
            databases = cursor.fetchall()
            print(f"📋 Bases de datos disponibles: {[db[0] for db in databases]}")
            
            conn.close()
            return True
            
        except Exception as e2:
            print(f"❌ Error conectando a 'postgres': {e2}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Probando conexión a PostgreSQL...")
    success = test_connection()
    if success:
        print("\n🎉 ¡Conexión exitosa! El problema puede estar en el backend.")
    else:
        print("\n💡 Necesitamos configurar PostgreSQL correctamente.")




