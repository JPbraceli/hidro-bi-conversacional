#!/usr/bin/env python3
"""
Script para ver los datos de la base de datos SQLite
"""
import sqlite3
import os

def view_database_data():
    """Ver datos de la base de datos"""
    db_path = "hidro_data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        print("💡 Ejecuta primero: python scripts/fix_sqlite_database.py")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📊 DATOS DE LA BASE HIDRO")
        print("=" * 50)
        
        # Resumen general
        print("\n📈 RESUMEN GENERAL:")
        cursor.execute("SELECT COUNT(*) FROM activities")
        activities = cursor.fetchone()[0]
        print(f"   Total actividades: {activities}")
        
        cursor.execute("SELECT COUNT(*) FROM contracts")
        contracts = cursor.fetchone()[0]
        print(f"   Total contratos: {contracts}")
        
        cursor.execute("SELECT COUNT(*) FROM profiles")
        profiles = cursor.fetchone()[0]
        print(f"   Total usuarios: {profiles}")
        
        cursor.execute("SELECT COUNT(*) FROM gateways")
        gateways = cursor.fetchone()[0]
        print(f"   Total gateways: {gateways}")
        
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        admins = cursor.fetchone()[0]
        print(f"   Total admins: {admins}")
        
        # Actividades
        print("\n📋 ACTIVIDADES:")
        print("-" * 30)
        cursor.execute("SELECT id, name, amount, vigente, anio_campania FROM activities")
        activities_data = cursor.fetchall()
        for row in activities_data:
            print(f"   ID: {row[0]} | {row[1]} | ${row[2]:,.2f} | Activo: {bool(row[3])} | Año: {row[4]}")
        
        # Contratos
        print("\n📋 CONTRATOS:")
        print("-" * 30)
        cursor.execute("SELECT id, contract_number, company, value, status FROM contracts")
        contracts_data = cursor.fetchall()
        for row in contracts_data:
            print(f"   ID: {row[0]} | {row[1]} | {row[2]} | ${row[3]:,.2f} | {row[4]}")
        
        # Usuarios
        print("\n👥 USUARIOS:")
        print("-" * 30)
        cursor.execute("SELECT id, first_name, last_name, role FROM profiles")
        profiles_data = cursor.fetchall()
        for row in profiles_data:
            print(f"   ID: {row[0]} | {row[1]} {row[2]} | {row[3]}")
        
        # Gateways
        print("\n🌐 GATEWAYS:")
        print("-" * 30)
        cursor.execute("SELECT id, name, location, status FROM gateways")
        gateways_data = cursor.fetchall()
        for row in gateways_data:
            print(f"   ID: {row[0]} | {row[1]} | {row[2]} | {row[3]}")
        
        # Análisis
        print("\n📊 ANÁLISIS:")
        print("-" * 30)
        
        # Actividades por año
        cursor.execute("SELECT anio_campania, COUNT(*) FROM activities GROUP BY anio_campania")
        years = cursor.fetchall()
        print("   Actividades por año:")
        for year, count in years:
            print(f"     {year}: {count} actividades")
        
        # Usuarios por rol
        cursor.execute("SELECT role, COUNT(*) FROM profiles GROUP BY role")
        roles = cursor.fetchall()
        print("   Usuarios por rol:")
        for role, count in roles:
            print(f"     {role}: {count} usuarios")
        
        # Contratos por estado
        cursor.execute("SELECT status, COUNT(*) FROM contracts GROUP BY status")
        statuses = cursor.fetchall()
        print("   Contratos por estado:")
        for status, count in statuses:
            print(f"     {status}: {count} contratos")
        
        # Gateways por estado
        cursor.execute("SELECT status, COUNT(*) FROM gateways GROUP BY status")
        gateway_statuses = cursor.fetchall()
        print("   Gateways por estado:")
        for status, count in gateway_statuses:
            print(f"     {status}: {count} gateways")
        
        # KPIs
        print("\n📈 KPIs PRINCIPALES:")
        print("-" * 30)
        
        cursor.execute("SELECT COUNT(*) FROM activities WHERE vigente = 1")
        active_activities = cursor.fetchone()[0]
        print(f"   Actividades activas: {active_activities}")
        
        cursor.execute("SELECT SUM(amount) FROM activities")
        total_value = cursor.fetchone()[0]
        print(f"   Valor total actividades: ${total_value:,.2f}")
        
        cursor.execute("SELECT COUNT(*) FROM contracts WHERE status = 'activo'")
        active_contracts = cursor.fetchone()[0]
        print(f"   Contratos activos: {active_contracts}")
        
        cursor.execute("SELECT SUM(value) FROM contracts")
        total_contracts_value = cursor.fetchone()[0]
        print(f"   Valor total contratos: ${total_contracts_value:,.2f}")
        
        cursor.execute("SELECT COUNT(*) FROM gateways WHERE status = 'activo'")
        active_gateways = cursor.fetchone()[0]
        print(f"   Gateways activos: {active_gateways}")
        
        conn.close()
        print(f"\n✅ Datos mostrados correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_database_data()
