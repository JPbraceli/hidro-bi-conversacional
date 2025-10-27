#!/usr/bin/env python3
"""
Script manual para configurar hidro
"""
import psycopg2
import os

def create_hidro_db():
    """Crear base de datos hidro"""
    try:
        print("🔍 Conectando a PostgreSQL...")
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
        
        # Crear base hidro
        try:
            cursor.execute("CREATE DATABASE hidro;")
            print("✅ Base 'hidro' creada exitosamente")
        except psycopg2.errors.DuplicateDatabase:
            print("ℹ️ Base 'hidro' ya existe")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando base: {e}")
        return False

def check_dumps():
    """Verificar archivos dump"""
    dumps = [
        'dev_hdcr_activities.dump',
        'dev_hdcr_admin.dump', 
        'dev_hdcr_contracts.dump',
        'dev_hdcr_gateway.dump',
        'dev_hdcr_profile.dump'
    ]
    
    print("📦 Verificando archivos dump...")
    for dump in dumps:
        if os.path.exists(dump):
            size = os.path.getsize(dump)
            print(f"✅ {dump} ({size:,} bytes)")
        else:
            print(f"❌ {dump} no encontrado")
    
    return all(os.path.exists(dump) for dump in dumps)

def main():
    print("🚀 Configuración manual de hidro")
    print("=" * 50)
    
    # 1. Crear base
    if not create_hidro_db():
        return
    
    # 2. Verificar dumps
    if not check_dumps():
        print("❌ Faltan archivos dump")
        return
    
    print("\n✅ Base hidro creada")
    print("📋 Ahora necesitas importar los dumps manualmente:")
    print("\nComandos para importar:")
    print("psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_activities.dump")
    print("psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_admin.dump")
    print("psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_contracts.dump")
    print("psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_gateway.dump")
    print("psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_profile.dump")

if __name__ == "__main__":
    main()




