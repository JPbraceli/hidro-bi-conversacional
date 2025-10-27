#!/usr/bin/env python3
import psycopg2

try:
    print("🔍 Probando conexión a PostgreSQL...")
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=15433,
        user='hdcruser',
        password='localpass',
        dbname='postgres'
    )
    print("✅ Conexión exitosa!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📊 PostgreSQL: {version[0]}")
    
    cursor.execute("SELECT datname FROM pg_database;")
    databases = cursor.fetchall()
    print(f"📋 Bases disponibles: {[db[0] for db in databases]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")




