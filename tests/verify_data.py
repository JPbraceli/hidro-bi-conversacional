#!/usr/bin/env python3
"""
Script para verificar los datos en la base
"""
import psycopg2

def verify_data():
    """Verificar datos en la base"""
    try:
        print("🔍 Verificando datos en dev_hdcr_activities...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        cursor = conn.cursor()
        
        # Contar actividades
        cursor.execute("SELECT COUNT(*) FROM activities;")
        count = cursor.fetchone()[0]
        print(f"📊 Actividades: {count}")
        
        # Mostrar algunas actividades
        cursor.execute("SELECT name, vigente, anio_campania FROM activities LIMIT 5;")
        activities = cursor.fetchall()
        print(f"📋 Primeras actividades: {activities}")
        
        conn.close()
        print("✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_data()




