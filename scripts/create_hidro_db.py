#!/usr/bin/env python3
"""
Script para crear la base 'hidro' automáticamente
"""
import psycopg2

def create_hidro_db():
    """Crear la base de datos hidro"""
    try:
        print("🔍 Conectando a PostgreSQL...")
        
        # Conectar a postgres (base por defecto)
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        
        # Verificar si la base ya existe
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'hidro';")
        if cursor.fetchone():
            print("✅ La base 'hidro' ya existe")
        else:
            # Crear la base
            print("📦 Creando base 'hidro'...")
            cursor.execute("CREATE DATABASE hidro;")
            print("✅ Base 'hidro' creada exitosamente")
        
        # Verificar que se creó
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'hidro';")
        if cursor.fetchone():
            print("🎉 ¡Base 'hidro' lista para usar!")
        else:
            print("❌ Error creando la base")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_hidro_db()