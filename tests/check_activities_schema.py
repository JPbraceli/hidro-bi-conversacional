#!/usr/bin/env python3
"""
Script para verificar el esquema de la tabla activities
"""
import psycopg2

def check_activities_schema():
    """Verificar esquema de activities"""
    try:
        print("🔍 Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        print("✅ Conexión exitosa!")
        
        cursor = conn.cursor()
        
        # Verificar columnas de activities
        print("📋 Columnas de activities:")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'activities' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Mostrar algunas actividades
        print("\n📊 Primeras 3 actividades:")
        cursor.execute("SELECT name, start_date, end_date, amount, vigente, anio_campania FROM activities LIMIT 3;")
        activities = cursor.fetchall()
        for i, activity in enumerate(activities, 1):
            print(f"  {i}. {activity}")
        
        # Verificar tablas de contratos
        print("\n📋 Tablas de contratos:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%contract%';
        """)
        contract_tables = cursor.fetchall()
        print(f"  {[table[0] for table in contract_tables]}")
        
        # Verificar tablas de usuarios
        print("\n📋 Tablas de usuarios:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%user%';
        """)
        user_tables = cursor.fetchall()
        print(f"  {[table[0] for table in user_tables]}")
        
        conn.close()
        print("\n🎉 ¡Esquema verificado!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_activities_schema()




