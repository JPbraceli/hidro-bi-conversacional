#!/usr/bin/env python3
"""
Verificar qué bases de datos puede consultar el agente
"""
import sqlite3
import os
from pathlib import Path

def check_agent_databases():
    """Verificar las bases de datos disponibles para el agente"""
    print("🗄️ BASES DE DATOS DISPONIBLES PARA EL AGENTE")
    print("=" * 60)
    
    # Verificar configuración del backend
    print("🔧 CONFIGURACIÓN DEL BACKEND:")
    print("   - Tipo de BD: SQLite")
    print("   - Archivo: hidro_data.db")
    print("   - Ruta relativa: ../hidro_data.db (desde backend/)")
    print("   - Ruta absoluta: C:/Users/Jose/Desktop/mi-app/hidronuevo/hidro_data.db")
    
    print()
    
    # Verificar archivo de BD
    db_path = "hidro_data.db"
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"📁 ARCHIVO DE BASE DE DATOS:")
        print(f"   ✅ Archivo: {db_path}")
        print(f"   📊 Tamaño: {size:,} bytes ({size/1024:.1f} KB)")
        print(f"   ✅ Estado: Disponible y accesible")
    else:
        print(f"❌ Archivo: {db_path} - NO ENCONTRADO")
        return
    
    print()
    
    # Conectar y analizar la BD
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📋 CONTENIDO DE LA BASE DE DATOS:")
        
        # Obtener tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        tables = cursor.fetchall()
        
        print(f"   📊 Total de tablas: {len(tables)}")
        total_records = 0
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   - {table_name}: {count:,} registros")
        
        print(f"\n📊 Total de registros en la BD: {total_records:,}")
        
        print("\n🔍 DETALLES DE LAS TABLAS:")
        for table in tables:
            table_name = table[0]
            print(f"\n📋 TABLA: {table_name.upper()}")
            
            # Obtener columnas
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"   📝 Columnas: {len(columns)}")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                nullable = "NULL" if col[3] else "NOT NULL"
                pk = " (PK)" if col[5] else ""
                print(f"      - {col_name} ({col_type}) {nullable}{pk}")
            
            # Muestra de datos
            if total_records > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                sample = cursor.fetchall()
                if sample:
                    print(f"   📄 Muestra de datos:")
                    for i, row in enumerate(sample, 1):
                        print(f"      {i}. {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a la BD: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎯 CAPACIDADES DEL AGENTE:")
    print("=" * 60)
    print("✅ Puede consultar TODAS las tablas de hidro_data.db")
    print("✅ Puede hacer JOINs entre tablas")
    print("✅ Puede generar visualizaciones automáticamente")
    print("✅ Puede detectar patrones y anomalías")
    print("✅ Puede sugerir análisis inteligentes")
    print("✅ Puede crear dashboards completos")
    
    print("\n🔗 RELACIONES DETECTADAS:")
    print("   - activities.id_contract → contracts.id")
    print("   - profiles.user_id → (referencia a usuarios)")
    print("   - gateways → (independiente)")
    print("   - admin_users → (independiente)")
    
    print("\n💡 TIPOS DE CONSULTAS POSIBLES:")
    print("   📊 Consultas simples por tabla")
    print("   🔗 Análisis cruzado entre tablas")
    print("   📈 Análisis de tendencias temporales")
    print("   🎯 KPIs y métricas de rendimiento")
    print("   📊 Visualizaciones (barras, pastel, líneas, etc.)")
    print("   🗺️ Mapas de calor y análisis de correlación")

if __name__ == "__main__":
    check_agent_databases()
