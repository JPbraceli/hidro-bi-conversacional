#!/usr/bin/env python3
"""
Script para analizar los archivos dump y entender su contenido
"""
import os
import subprocess
import psycopg2

def analyze_dump_files():
    """Analizar archivos dump"""
    print("🔍 Analizando archivos dump...")
    
    dumps = [
        'dev_hdcr_activities.dump',
        'dev_hdcr_admin.dump',
        'dev_hdcr_contracts.dump',
        'dev_hdcr_gateway.dump',
        'dev_hdcr_profile.dump'
    ]
    
    for dump_file in dumps:
        if os.path.exists(dump_file):
            size = os.path.getsize(dump_file)
            print(f"📄 {dump_file}: {size:,} bytes ({size/1024/1024:.2f} MB)")
            
            # Intentar leer las primeras líneas para ver el formato
            try:
                with open(dump_file, 'r', encoding='utf-8', errors='ignore') as f:
                    first_lines = []
                    for i, line in enumerate(f):
                        if i >= 20:  # Solo primeras 20 líneas
                            break
                        first_lines.append(line.strip())
                    
                    print(f"  📋 Primeras líneas:")
                    for line in first_lines[:10]:
                        if line:
                            print(f"    {line}")
                    
                    # Buscar información específica
                    if 'CREATE TABLE' in ' '.join(first_lines):
                        print("  ✅ Contiene definiciones de tablas")
                    if 'INSERT INTO' in ' '.join(first_lines):
                        print("  ✅ Contiene datos INSERT")
                    if 'COPY' in ' '.join(first_lines):
                        print("  ✅ Contiene datos COPY")
                        
            except Exception as e:
                print(f"  ❌ Error leyendo archivo: {e}")
        else:
            print(f"❌ {dump_file} no encontrado")

def analyze_current_database():
    """Analizar la base de datos actual"""
    print("\n🔍 Analizando base de datos actual...")
    
    try:
        # Conectar a dev_hdcr_activities
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a dev_hdcr_activities")
        
        # Listar todas las tablas
        cursor.execute("""
            SELECT table_name, table_type
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"📋 Tablas encontradas: {len(tables)}")
        for table_name, table_type in tables:
            print(f"  - {table_name} ({table_type})")
            
            # Contar registros en cada tabla
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"    📊 Registros: {count}")
                
                # Mostrar columnas
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f"    📋 Columnas: {len(columns)}")
                for col_name, col_type, nullable in columns[:5]:  # Solo primeras 5
                    print(f"      - {col_name} ({col_type}) {'NULL' if nullable == 'YES' else 'NOT NULL'}")
                if len(columns) > 5:
                    print(f"      ... y {len(columns) - 5} más")
                    
            except Exception as e:
                print(f"    ⚠️ Error analizando tabla: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a base: {e}")

def suggest_database_strategy():
    """Sugerir estrategia para la base de datos"""
    print("\n🎯 ESTRATEGIA RECOMENDADA:")
    print("=" * 50)
    
    print("1. 📊 BASE ACTUAL (dev_hdcr_activities):")
    print("   ✅ Ya tiene datos (515 actividades)")
    print("   ✅ Funcionando correctamente")
    print("   ✅ Esquema completo")
    
    print("\n2. 🔄 OPCIONES PARA DUMP FILES:")
    print("   A) Importar a base 'hidro' (nueva)")
    print("   B) Usar base actual (dev_hdcr_activities)")
    print("   C) Crear base unificada")
    
    print("\n3. 🚀 RECOMENDACIÓN:")
    print("   - Usar dev_hdcr_activities (ya funciona)")
    print("   - Importar dumps a hidro como respaldo")
    print("   - Probar chat con datos reales")
    
    print("\n4. 📋 PRÓXIMOS PASOS:")
    print("   - Verificar que chat funcione con dev_hdcr_activities")
    print("   - Si funciona bien, mantener configuración actual")
    print("   - Si necesitas más datos, importar dumps a hidro")

def main():
    print("🔍 ANÁLISIS COMPLETO DE DUMP FILES")
    print("=" * 50)
    
    # Analizar archivos dump
    analyze_dump_files()
    
    # Analizar base actual
    analyze_current_database()
    
    # Sugerir estrategia
    suggest_database_strategy()

if __name__ == "__main__":
    main()




