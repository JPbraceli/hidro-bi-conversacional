#!/usr/bin/env python3
"""
Script para probar conexión a PostgreSQL con datos reales
"""
import psycopg2

def test_postgres():
    """Probar conexión a PostgreSQL"""
    try:
        print("🔍 Probando conexión a dev_hdcr_activities...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        print("✅ Conexión exitosa!")
        
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        print(f"📋 Tablas: {[table[0] for table in tables]}")
        
        # Contar actividades
        cursor.execute("SELECT COUNT(*) FROM activities;")
        count = cursor.fetchone()[0]
        print(f"📊 Actividades: {count}")
        
        # Mostrar algunas actividades
        cursor.execute("SELECT name, vigente, anio_campania FROM activities LIMIT 3;")
        activities = cursor.fetchall()
        print(f"📋 Primeras actividades: {activities}")
        
        conn.close()
        print("✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_postgres()




