#!/usr/bin/env python3
"""
Script para mostrar un resumen visual de los datos de HIDRO
"""
import sqlite3
import os

def show_data_summary():
    """Mostrar resumen visual de los datos"""
    db_path = "hidro_data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🏢 HIDRO - RESUMEN EJECUTIVO")
        print("=" * 60)
        
        # KPIs principales
        print("\n📊 KPIs PRINCIPALES:")
        print("┌─────────────────────────────────────────────────────────────┐")
        
        cursor.execute("SELECT COUNT(*) FROM activities")
        activities = cursor.fetchone()[0]
        print(f"│ 📋 Actividades totales: {activities:>45} │")
        
        cursor.execute("SELECT COUNT(*) FROM activities WHERE vigente = 1")
        active_activities = cursor.fetchone()[0]
        print(f"│ ✅ Actividades activas: {active_activities:>44} │")
        
        cursor.execute("SELECT SUM(amount) FROM activities")
        total_activities_value = cursor.fetchone()[0]
        print(f"│ 💰 Valor actividades: ${total_activities_value:>40,.2f} │")
        
        cursor.execute("SELECT COUNT(*) FROM contracts")
        contracts = cursor.fetchone()[0]
        print(f"│ 📄 Contratos totales: {contracts:>45} │")
        
        cursor.execute("SELECT SUM(value) FROM contracts")
        total_contracts_value = cursor.fetchone()[0]
        print(f"│ 💵 Valor contratos: ${total_contracts_value:>42,.2f} │")
        
        cursor.execute("SELECT COUNT(*) FROM profiles")
        users = cursor.fetchone()[0]
        print(f"│ 👥 Usuarios registrados: {users:>40} │")
        
        cursor.execute("SELECT COUNT(*) FROM gateways WHERE status = 'activo'")
        active_gateways = cursor.fetchone()[0]
        print(f"│ 🌐 Gateways activos: {active_gateways:>43} │")
        
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Top actividades
        print("\n💰 TOP 3 ACTIVIDADES MÁS COSTOSAS:")
        print("┌─────────────────────────────────────────────────────────────┐")
        cursor.execute("SELECT name, amount FROM activities ORDER BY amount DESC LIMIT 3")
        top_activities = cursor.fetchall()
        for i, (name, amount) in enumerate(top_activities, 1):
            print(f"│ {i}. {name:<45} ${amount:>10,.2f} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Contratos por empresa
        print("\n🏢 CONTRATOS POR EMPRESA:")
        print("┌─────────────────────────────────────────────────────────────┐")
        cursor.execute("SELECT company, value, status FROM contracts ORDER BY value DESC")
        contracts_data = cursor.fetchall()
        for company, value, status in contracts_data:
            status_icon = "✅" if status == "activo" else "⏸️"
            print(f"│ {status_icon} {company:<40} ${value:>10,.2f} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Usuarios por rol
        print("\n👥 DISTRIBUCIÓN DE USUARIOS:")
        print("┌─────────────────────────────────────────────────────────────┐")
        cursor.execute("SELECT role, COUNT(*) FROM profiles GROUP BY role ORDER BY COUNT(*) DESC")
        users_by_role = cursor.fetchall()
        for role, count in users_by_role:
            print(f"│ {role:<50} {count:>5} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Estado de gateways
        print("\n🌐 ESTADO DE GATEWAYS:")
        print("┌─────────────────────────────────────────────────────────────┐")
        cursor.execute("SELECT name, location, status FROM gateways ORDER BY status, name")
        gateways_data = cursor.fetchall()
        for name, location, status in gateways_data:
            status_icon = "🟢" if status == "activo" else "🟡"
            print(f"│ {status_icon} {name:<25} {location:<20} {status:>8} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Resumen financiero
        print("\n💵 RESUMEN FINANCIERO:")
        print("┌─────────────────────────────────────────────────────────────┐")
        total_general = total_activities_value + total_contracts_value
        print(f"│ 💰 Valor total actividades: ${total_activities_value:>30,.2f} │")
        print(f"│ 💵 Valor total contratos: ${total_contracts_value:>32,.2f} │")
        print(f"│ 🏆 TOTAL GENERAL: ${total_general:>40,.2f} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Estadísticas adicionales
        print("\n📈 ESTADÍSTICAS ADICIONALES:")
        print("┌─────────────────────────────────────────────────────────────┐")
        
        cursor.execute("SELECT AVG(amount) FROM activities")
        avg_activity = cursor.fetchone()[0]
        print(f"│ 📊 Valor promedio por actividad: ${avg_activity:>25,.2f} │")
        
        cursor.execute("SELECT AVG(value) FROM contracts")
        avg_contract = cursor.fetchone()[0]
        print(f"│ 📊 Valor promedio por contrato: ${avg_contract:>26,.2f} │")
        
        cursor.execute("SELECT COUNT(*) FROM gateways")
        total_gateways = cursor.fetchone()[0]
        print(f"│ 🌐 Total de gateways: {total_gateways:>42} │")
        
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        admins = cursor.fetchone()[0]
        print(f"│ 👨‍💼 Administradores: {admins:>44} │")
        
        print("└─────────────────────────────────────────────────────────────┘")
        
        conn.close()
        print(f"\n✅ Resumen generado correctamente")
        print(f"📁 Base de datos: {db_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_data_summary()
