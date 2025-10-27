#!/usr/bin/env python3
"""
Importar todos los dumps originales del ambiente de desarrollo HIDRO
"""
import sqlite3
import os
import re
from datetime import datetime

def create_fresh_database():
    """Crear una nueva base de datos limpia"""
    print("🗄️ CREANDO NUEVA BASE DE DATOS CON DATOS COMPLETOS")
    print("=" * 60)
    
    # Crear nueva BD con nombre temporal
    new_db_name = "hidro_data_complete.db"
    if os.path.exists(new_db_name):
        os.remove(new_db_name)
        print("✅ Base de datos anterior eliminada")
    
    # Crear nueva BD
    conn = sqlite3.connect(new_db_name)
    cursor = conn.cursor()
    
    print("✅ Nueva base de datos creada")
    return conn, cursor

def parse_dump_file(dump_file):
    """Parsear un archivo dump de PostgreSQL"""
    print(f"📄 Procesando: {dump_file}")
    
    if not os.path.exists(dump_file):
        print(f"❌ Archivo no encontrado: {dump_file}")
        return None
    
    with open(dump_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extraer datos INSERT
    insert_pattern = r"INSERT INTO\s+(\w+)\s+\([^)]+\)\s+VALUES\s+(.+?);"
    matches = re.findall(insert_pattern, content, re.DOTALL | re.IGNORECASE)
    
    table_data = {}
    for table_name, values in matches:
        if table_name not in table_data:
            table_data[table_name] = []
        
        # Parsear valores
        values_clean = values.strip()
        if values_clean.startswith('(') and values_clean.endswith(')'):
            values_clean = values_clean[1:-1]
        
        # Dividir por filas
        rows = values_clean.split('),(')
        for row in rows:
            row = row.strip()
            if row.startswith('('):
                row = row[1:]
            if row.endswith(')'):
                row = row[:-1]
            
            # Parsear valores individuales
            values_list = []
            current_value = ""
            in_quotes = False
            quote_char = None
            
            for char in row:
                if char in ["'", '"'] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_value += char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                    current_value += char
                elif char == ',' and not in_quotes:
                    values_list.append(current_value.strip())
                    current_value = ""
                else:
                    current_value += char
            
            if current_value.strip():
                values_list.append(current_value.strip())
            
            if values_list:
                table_data[table_name].append(values_list)
    
    print(f"   📊 Tablas encontradas: {len(table_data)}")
    for table, rows in table_data.items():
        print(f"      - {table}: {len(rows)} registros")
    
    return table_data

def create_table_schema(cursor, table_name, sample_row):
    """Crear esquema de tabla basado en una fila de muestra"""
    print(f"🔧 Creando esquema para tabla: {table_name}")
    
    # Detectar tipos de datos
    columns = []
    for i, value in enumerate(sample_row):
        col_name = f"col_{i+1}"
        
        # Limpiar valor
        clean_value = value.strip().strip("'\"")
        
        # Detectar tipo
        if clean_value.lower() in ['true', 'false', '1', '0']:
            col_type = 'BOOLEAN'
        elif clean_value.isdigit():
            col_type = 'INTEGER'
        elif clean_value.replace('.', '').isdigit():
            col_type = 'REAL'
        elif clean_value.startswith('20') and len(clean_value) >= 10:
            col_type = 'TEXT'  # Fecha
        else:
            col_type = 'TEXT'
        
        columns.append(f"{col_name} {col_type}")
    
    # Crear tabla
    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(columns)})"
    cursor.execute(create_sql)
    print(f"   ✅ Tabla creada: {table_name}")

def insert_data(cursor, table_name, data_rows):
    """Insertar datos en la tabla"""
    if not data_rows:
        return
    
    print(f"📥 Insertando datos en: {table_name}")
    
    # Usar la primera fila para determinar columnas
    sample_row = data_rows[0]
    columns = [f"col_{i+1}" for i in range(len(sample_row))]
    
    # Preparar SQL de inserción
    placeholders = ', '.join(['?' for _ in columns])
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    
    # Insertar datos
    for row in data_rows:
        try:
            # Limpiar valores
            clean_row = []
            for value in row:
                clean_value = value.strip().strip("'\"")
                
                # Convertir tipos
                if clean_value.lower() in ['true', '1']:
                    clean_value = 1
                elif clean_value.lower() in ['false', '0']:
                    clean_value = 0
                elif clean_value.isdigit():
                    clean_value = int(clean_value)
                elif clean_value.replace('.', '').isdigit():
                    clean_value = float(clean_value)
                
                clean_row.append(clean_value)
            
            cursor.execute(insert_sql, clean_row)
        except Exception as e:
            print(f"   ⚠️ Error insertando fila: {e}")
            continue
    
    print(f"   ✅ Datos insertados en: {table_name}")

def import_all_dumps():
    """Importar todos los dumps"""
    print("🚀 IMPORTANDO TODOS LOS DUMPS ORIGINALES")
    print("=" * 60)
    
    # Crear nueva BD
    conn, cursor = create_fresh_database()
    
    # Lista de dumps a importar
    dumps = [
        "dev_hdcr_activities.dump",
        "dev_hdcr_admin.dump", 
        "dev_hdcr_contracts.dump",
        "dev_hdcr_gateway.dump",
        "dev_hdcr_profile.dump"
    ]
    
    total_records = 0
    
    for dump_file in dumps:
        print(f"\n📦 Procesando: {dump_file}")
        print("-" * 40)
        
        # Parsear dump
        table_data = parse_dump_file(dump_file)
        
        if table_data:
            for table_name, rows in table_data.items():
                if rows:
                    # Crear esquema
                    create_table_schema(cursor, table_name, rows[0])
                    
                    # Insertar datos
                    insert_data(cursor, table_name, rows)
                    total_records += len(rows)
        
        print(f"✅ {dump_file} procesado")
    
    # Commit y cerrar
    conn.commit()
    conn.close()
    
    print(f"\n🎉 IMPORTACIÓN COMPLETADA")
    print(f"📊 Total de registros importados: {total_records:,}")
    
    # Verificar resultado
    verify_import()

def verify_import():
    """Verificar la importación"""
    print("\n🔍 VERIFICANDO IMPORTACIÓN")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect("hidro_data_complete.db")
        cursor = conn.cursor()
        
        # Obtener tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        tables = cursor.fetchall()
        
        print(f"📋 Tablas creadas: {len(tables)}")
        total_records = 0
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   - {table_name}: {count:,} registros")
        
        print(f"\n📊 Total de registros: {total_records:,}")
        
        # Muestra de datos
        print("\n🔍 MUESTRA DE DATOS:")
        for table in tables[:2]:  # Solo primeras 2 tablas
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample = cursor.fetchall()
            print(f"\n📋 {table_name.upper()}:")
            for i, row in enumerate(sample, 1):
                print(f"   {i}. {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando: {e}")

if __name__ == "__main__":
    import_all_dumps()
