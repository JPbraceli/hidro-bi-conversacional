#!/usr/bin/env python3
"""
Script para importar dumps desde el directorio backend
"""
import psycopg2
import subprocess
import os
import sys

def import_dumps():
    """Importar dumps a la base hidro"""
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
        
        # Verificar que la base 'hidro' existe
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'hidro';")
        if not cursor.fetchone():
            print("❌ La base 'hidro' no existe. Créala primero en pgAdmin")
            return
        
        print("✅ Base 'hidro' encontrada")
        conn.close()
        
        # Cambiar al directorio padre para encontrar los dumps
        os.chdir('..')
        print(f"📁 Directorio actual: {os.getcwd()}")
        
        # Lista de dumps
        dumps = [
            'dev_hdcr_activities.dump',
            'dev_hdcr_admin.dump', 
            'dev_hdcr_contracts.dump',
            'dev_hdcr_gateway.dump',
            'dev_hdcr_profile.dump'
        ]
        
        # Configurar entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = 'localpass'
        
        # Importar cada dump
        for dump_file in dumps:
            if os.path.exists(dump_file):
                print(f"📥 Importando {dump_file}...")
                
                cmd = [
                    'psql',
                    '-h', '127.0.0.1',
                    '-p', '15433',
                    '-U', 'hdcruser',
                    '-d', 'hidro',
                    '-f', dump_file
                ]
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dump_file} importado exitosamente")
                else:
                    print(f"⚠️ Error importando {dump_file}: {result.stderr[:200]}...")
            else:
                print(f"❌ Archivo {dump_file} no encontrado")
        
        print("\n🎉 ¡Importación completada!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import_dumps()




