#!/usr/bin/env python3
"""
Script para probar la conexión a SQLite
"""
import sqlite3
import os

def test_sqlite_connection():
    """Probar conexión a SQLite"""
    print("🔍 PROBANDO CONEXIÓN A SQLITE")
    print("=" * 50)
    
    db_path = "hidro_data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        print("💡 Ejecuta primero: python scripts/fix_sqlite_database.py")
        return False
    
    try:
        # Conectar a SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ Conectado a SQLite: {db_path}")
        
        # Verificar version
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        print(f"📊 SQLite version: {version}")
        
        # Listar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
        # Probar consultas
        print("\n🔍 Probando consultas...")
        
        queries = [
            ("Total actividades", "SELECT COUNT(*) FROM activities"),
            ("Actividades activas", "SELECT COUNT(*) FROM activities WHERE vigente = 1"),
            ("Valor total actividades", "SELECT SUM(amount) FROM activities"),
            ("Total contratos", "SELECT COUNT(*) FROM contracts"),
            ("Contratos activos", "SELECT COUNT(*) FROM contracts WHERE status = 'activo'"),
            ("Total usuarios", "SELECT COUNT(*) FROM profiles"),
            ("Gateways activos", "SELECT COUNT(*) FROM gateways WHERE status = 'activo'"),
            ("Usuarios admin", "SELECT COUNT(*) FROM admin_users")
        ]
        
        for name, query in queries:
            try:
                result = cursor.execute(query).fetchone()
                print(f"📊 {name}: {result[0]}")
            except Exception as e:
                print(f"❌ Error en {name}: {e}")
        
        # Probar consultas complejas
        print("\n🔍 Probando consultas complejas...")
        
        # Actividades por año
        cursor.execute("SELECT anio_campania, COUNT(*) FROM activities GROUP BY anio_campania")
        years = cursor.fetchall()
        print(f"📈 Actividades por año: {dict(years)}")
        
        # Usuarios por rol
        cursor.execute("SELECT role, COUNT(*) FROM profiles GROUP BY role")
        roles = cursor.fetchall()
        print(f"👥 Usuarios por rol: {dict(roles)}")
        
        # Contratos por estado
        cursor.execute("SELECT status, COUNT(*) FROM contracts GROUP BY status")
        statuses = cursor.fetchall()
        print(f"📋 Contratos por estado: {dict(statuses)}")
        
        # Gateways por estado
        cursor.execute("SELECT status, COUNT(*) FROM gateways GROUP BY status")
        gateway_statuses = cursor.fetchall()
        print(f"🌐 Gateways por estado: {dict(gateway_statuses)}")
        
        conn.close()
        
        print(f"\n🎉 ¡CONEXIÓN EXITOSA!")
        print(f"📁 Base de datos: {db_path}")
        print(f"💡 Para usar en el chat, actualiza la configuración del backend")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def suggest_backend_config():
    """Sugerir configuración para el backend"""
    print(f"\n🔧 CONFIGURACIÓN PARA BACKEND:")
    print("=" * 50)
    
    print("1. 📝 Actualizar dependencies.py:")
    print("   - Cambiar de PostgreSQL a SQLite")
    print("   - Usar get_sqlite_db() en lugar de get_db()")
    print("   - Actualizar schema.py para SQLite")
    
    print("\n2. 🚀 Ventajas de SQLite:")
    print("   ✅ Sin configuración de servidor")
    print("   ✅ Archivo único (hidro_data.db)")
    print("   ✅ Fácil de respaldar")
    print("   ✅ Funciona en cualquier sistema")
    print("   ✅ Compatible con Python")
    
    print("\n3. 📋 Próximos pasos:")
    print("   - Actualizar backend para usar SQLite")
    print("   - Probar chat con datos reales")
    print("   - Verificar que las consultas funcionen")
    
    print("\n4. 🎯 Comandos para probar:")
    print("   python -c \"import sqlite3; conn=sqlite3.connect('hidro_data.db'); print(conn.execute('SELECT COUNT(*) FROM activities').fetchone()[0])\"")
    print("   python -c \"import sqlite3; conn=sqlite3.connect('hidro_data.db'); print(conn.execute('SELECT * FROM activities LIMIT 3').fetchall())\"")

def main():
    print("🚀 PRUEBA DE CONEXIÓN SQLITE")
    print("=" * 50)
    
    # Probar conexión
    success = test_sqlite_connection()
    
    if success:
        # Sugerir configuración
        suggest_backend_config()
    else:
        print("\n❌ No se pudo conectar a SQLite")
        print("💡 Ejecuta primero: python scripts/fix_sqlite_database.py")

if __name__ == "__main__":
    main()
