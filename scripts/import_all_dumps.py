#!/usr/bin/env python3
"""
Script para importar todos los dumps a la base 'hidro'
"""
import psycopg2
import subprocess
import os

def import_all_dumps():
    """Importar todos los dumps a la base hidro"""
    try:
        print("🔍 Conectando a PostgreSQL...")
        
        # Conectar a postgres
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
        
        # Verificar si la base hidro existe
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'hidro';")
        if not cursor.fetchone():
            print("❌ La base 'hidro' no existe. Créala primero en pgAdmin")
            return
        
        conn.close()
        
        # Verificar que psql esté disponible
        try:
            result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
            print(f"✅ psql disponible: {result.stdout.strip()}")
        except:
            print("❌ psql no está disponible. Instálalo o usa pgAdmin")
            return
        
        # Lista de dumps a importar
        dumps = [
            'dev_hdcr_activities.dump',
            'dev_hdcr_admin.dump',
            'dev_hdcr_contracts.dump', 
            'dev_hdcr_gateway.dump',
            'dev_hdcr_profile.dump'
        ]
        
        print(f"📦 Importando {len(dumps)} dumps a la base 'hidro'...")
        
        for dump_file in dumps:
            if os.path.exists(dump_file):
                print(f"📦 Importando {dump_file}...")
                cmd = f'psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f {dump_file}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dump_file} importado exitosamente")
                else:
                    print(f"❌ Error importando {dump_file}: {result.stderr}")
            else:
                print(f"⚠️ {dump_file} no encontrado")
        
        # Verificar tablas importadas
        print("\n🔍 Verificando tablas importadas...")
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
        
        print("🎉 ¡Importación completada!")
        print("🚀 Ahora puedes usar la base 'hidro' en el chat")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import_all_dumps()




