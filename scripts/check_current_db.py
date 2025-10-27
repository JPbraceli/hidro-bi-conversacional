#!/usr/bin/env python3
"""
Verificar qué hay en la base de datos actual
"""
import psycopg2

def check_current_db():
    """Verificar base de datos actual"""
    try:
        print("🔍 Conectando a dev_hdcr_activities...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        
        # Listar tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 Tablas encontradas: {len(tables)}")
        for table_name, in tables:
            print(f"  - {table_name}")
            
            # Contar registros
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"    📊 Registros: {count}")
                
                # Mostrar columnas principales
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position
                    LIMIT 5;
                """)
                columns = cursor.fetchall()
                print(f"    📋 Columnas principales:")
                for col_name, col_type in columns:
                    print(f"      - {col_name} ({col_type})")
                    
            except Exception as e:
                print(f"    ⚠️ Error: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_current_db()




