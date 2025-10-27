#!/usr/bin/env python3
"""
Script rápido para crear base hidro e importar dumps
"""
import psycopg2
import subprocess
import os

def main():
    try:
        print("🔍 Conectando a PostgreSQL...")
        
        # Conectar a postgres para crear hidro
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        
        # Crear base hidro si no existe
        try:
            cursor.execute("CREATE DATABASE hidro;")
            print("✅ Base 'hidro' creada")
        except psycopg2.errors.DuplicateDatabase:
            print("ℹ️ Base 'hidro' ya existe")
        
        conn.close()
        
        # Verificar que psql esté disponible
        try:
            result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
            print(f"✅ psql disponible: {result.stdout.strip()}")
        except:
            print("❌ psql no está disponible")
            return
        
        # Importar dumps
        dumps = [
            'dev_hdcr_activities.dump',
            'dev_hdcr_admin.dump', 
            'dev_hdcr_contracts.dump',
            'dev_hdcr_gateway.dump',
            'dev_hdcr_profile.dump'
        ]
        
        for dump_file in dumps:
            if os.path.exists(dump_file):
                print(f"📦 Importando {dump_file}...")
                cmd = f'psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f {dump_file}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dump_file} importado")
                else:
                    print(f"❌ Error importando {dump_file}: {result.stderr}")
            else:
                print(f"⚠️ {dump_file} no encontrado")
        
        # Verificar tablas
        print("\n🔍 Verificando tablas...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='hidro'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()




