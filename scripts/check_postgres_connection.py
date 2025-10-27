#!/usr/bin/env python3
"""
Script para verificar y configurar la conexión a PostgreSQL
"""
import psycopg2
import subprocess
import os

def check_postgres_connection():
    """Verificar conexión a PostgreSQL"""
    print("🔍 VERIFICANDO CONEXIÓN A POSTGRESQL")
    print("=" * 50)
    
    # Configuraciones a probar
    configs = [
        {
            "name": "Puerto estándar 5432",
            "host": "127.0.0.1",
            "port": 5432,
            "user": "postgres",
            "password": "postgres",
            "dbname": "postgres"
        },
        {
            "name": "Puerto estándar 5432 (usuario hdcruser)",
            "host": "127.0.0.1", 
            "port": 5432,
            "user": "hdcruser",
            "password": "localpass",
            "dbname": "postgres"
        },
        {
            "name": "Puerto 15433 (configuración actual)",
            "host": "127.0.0.1",
            "port": 15433,
            "user": "hdcruser", 
            "password": "localpass",
            "dbname": "dev_hdcr_activities"
        }
    ]
    
    working_config = None
    
    for config in configs:
        print(f"\n🔍 Probando: {config['name']}")
        try:
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                dbname=config['dbname']
            )
            print(f"✅ Conexión exitosa!")
            
            # Verificar version
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"📊 PostgreSQL: {version[:50]}...")
            
            # Listar bases de datos
            cursor.execute("SELECT datname FROM pg_database;")
            databases = cursor.fetchall()
            print(f"📋 Bases disponibles: {[db[0] for db in databases]}")
            
            # Verificar si existe dev_hdcr_activities
            if 'dev_hdcr_activities' in [db[0] for db in databases]:
                print("✅ Base dev_hdcr_activities encontrada!")
                
                # Conectar a dev_hdcr_activities
                conn.close()
                conn = psycopg2.connect(
                    host=config['host'],
                    port=config['port'],
                    user=config['user'],
                    password=config['password'],
                    dbname='dev_hdcr_activities'
                )
                cursor = conn.cursor()
                
                # Listar tablas
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                print(f"📋 Tablas en dev_hdcr_activities: {[table[0] for table in tables]}")
                
                # Contar registros en activities
                if tables:
                    table_name = tables[0][0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    print(f"📊 Registros en {table_name}: {count}")
            
            conn.close()
            working_config = config
            break
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    if working_config:
        print(f"\n🎉 CONFIGURACIÓN FUNCIONANDO:")
        print(f"   Host: {working_config['host']}")
        print(f"   Puerto: {working_config['port']}")
        print(f"   Usuario: {working_config['user']}")
        print(f"   Base: {working_config['dbname']}")
        
        # Generar configuración para el backend
        print(f"\n🔧 CONFIGURACIÓN PARA BACKEND:")
        print(f"   db_host: {working_config['host']}")
        print(f"   db_port: {working_config['port']}")
        print(f"   db_user: {working_config['user']}")
        print(f"   db_password: {working_config['password']}")
        print(f"   db_name: dev_hdcr_activities")
        
        return working_config
    else:
        print("\n❌ No se pudo conectar a PostgreSQL")
        print("💡 Posibles soluciones:")
        print("   1. Instalar PostgreSQL")
        print("   2. Iniciar servicio PostgreSQL")
        print("   3. Verificar credenciales")
        return None

def suggest_database_setup():
    """Sugerir configuración de base de datos"""
    print(f"\n🎯 ESTRATEGIA RECOMENDADA:")
    print("=" * 50)
    
    print("1. 📊 USAR POSTGRESQL ESTÁNDAR (puerto 5432)")
    print("   ✅ Ya está funcionando")
    print("   ✅ Puerto estándar")
    print("   ✅ Fácil de configurar")
    
    print("\n2. 🔄 IMPORTAR DUMP FILES:")
    print("   A) Crear base 'hidro' unificada")
    print("   B) Importar todos los dumps")
    print("   C) Configurar backend para usar 'hidro'")
    
    print("\n3. 🚀 PRÓXIMOS PASOS:")
    print("   - Actualizar configuración del backend")
    print("   - Importar dumps a base 'hidro'")
    print("   - Probar chat con datos reales")
    
    print("\n4. 📋 COMANDOS PARA IMPORTAR:")
    print("   # Crear base hidro")
    print("   createdb -h 127.0.0.1 -p 5432 -U postgres hidro")
    print("   ")
    print("   # Importar dumps")
    print("   psql -h 127.0.0.1 -p 5432 -U postgres -d hidro -f dev_hdcr_activities.dump")
    print("   psql -h 127.0.0.1 -p 5432 -U postgres -d hidro -f dev_hdcr_admin.dump")
    print("   psql -h 127.0.0.1 -p 5432 -U postgres -d hidro -f dev_hdcr_contracts.dump")
    print("   psql -h 127.0.0.1 -p 5432 -U postgres -d hidro -f dev_hdcr_gateway.dump")
    print("   psql -h 127.0.0.1 -p 5432 -U postgres -d hidro -f dev_hdcr_profile.dump")

def main():
    print("🔍 VERIFICACIÓN DE CONEXIÓN POSTGRESQL")
    print("=" * 50)
    
    # Verificar conexión
    config = check_postgres_connection()
    
    if config:
        # Sugerir configuración
        suggest_database_setup()
    else:
        print("\n❌ No se pudo conectar a PostgreSQL")
        print("💡 Necesitas instalar y configurar PostgreSQL primero")

if __name__ == "__main__":
    main()
