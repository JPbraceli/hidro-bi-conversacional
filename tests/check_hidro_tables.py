#!/usr/bin/env python3
"""
Script para verificar qué tablas existen en la base hidro
"""
import psycopg2

def check_hidro_tables():
    """Verificar tablas en la base hidro"""
    try:
        print("🔍 Conectando a base 'hidro'...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='hidro'
        )
        print("✅ Conexión exitosa a hidro")
        
        cursor = conn.cursor()
        
        # Listar todas las tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"📋 Tablas en hidro: {[table[0] for table in tables]}")
        
        # Verificar si existe tabla contracts
        if any('contract' in table[0].lower() for table in tables):
            print("✅ Tabla de contratos encontrada")
            contract_tables = [table[0] for table in tables if 'contract' in table[0].lower()]
            print(f"📋 Tablas de contratos: {contract_tables}")
        else:
            print("❌ No se encontraron tablas de contratos")
        
        # Verificar si existe tabla activities
        if any('activit' in table[0].lower() for table in tables):
            print("✅ Tabla de actividades encontrada")
            activity_tables = [table[0] for table in tables if 'activit' in table[0].lower()]
            print(f"📋 Tablas de actividades: {activity_tables}")
        else:
            print("❌ No se encontraron tablas de actividades")
        
        # Contar registros en tablas principales
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"📊 {table_name}: {count} registros")
            except Exception as e:
                print(f"⚠️ Error contando {table_name}: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_hidro_tables()




