#!/usr/bin/env python3
"""
Script para hacer consultas específicas a la base de datos
"""
import sqlite3
import os

def query_database():
    """Hacer consultas específicas a la base de datos"""
    db_path = "hidro_data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 CONSULTAS ESPECÍFICAS A LA BASE HIDRO")
        print("=" * 50)
        
        # Consulta 1: Actividades más costosas
        print("\n💰 TOP 3 ACTIVIDADES MÁS COSTOSAS:")
        print("-" * 40)
        cursor.execute("SELECT name, amount FROM activities ORDER BY amount DESC LIMIT 3")
        top_activities = cursor.fetchall()
        for i, (name, amount) in enumerate(top_activities, 1):
            print(f"   {i}. {name}: ${amount:,.2f}")
        
        # Consulta 2: Contratos por valor
        print("\n📋 CONTRATOS POR VALOR:")
        print("-" * 40)
        cursor.execute("SELECT contract_number, company, value FROM contracts ORDER BY value DESC")
        contracts_by_value = cursor.fetchall()
        for contract_number, company, value in contracts_by_value:
            print(f"   {contract_number} - {company}: ${value:,.2f}")
        
        # Consulta 3: Usuarios por rol
        print("\n👥 DISTRIBUCIÓN DE USUARIOS:")
        print("-" * 40)
        cursor.execute("SELECT role, COUNT(*) as cantidad FROM profiles GROUP BY role ORDER BY cantidad DESC")
        users_by_role = cursor.fetchall()
        for role, count in users_by_role:
            print(f"   {role}: {count} usuarios")
        
        # Consulta 4: Gateways por estado
        print("\n🌐 ESTADO DE GATEWAYS:")
        print("-" * 40)
        cursor.execute("SELECT status, COUNT(*) as cantidad FROM gateways GROUP BY status")
        gateways_by_status = cursor.fetchall()
        for status, count in gateways_by_status:
            print(f"   {status}: {count} gateways")
        
        # Consulta 5: Resumen financiero
        print("\n💵 RESUMEN FINANCIERO:")
        print("-" * 40)
        cursor.execute("SELECT SUM(amount) FROM activities")
        total_activities = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(value) FROM contracts")
        total_contracts = cursor.fetchone()[0]
        print(f"   Valor total actividades: ${total_activities:,.2f}")
        print(f"   Valor total contratos: ${total_contracts:,.2f}")
        print(f"   Total general: ${total_activities + total_contracts:,.2f}")
        
        # Consulta 6: Actividades por contrato
        print("\n🔗 ACTIVIDADES POR CONTRATO:")
        print("-" * 40)
        cursor.execute("""
            SELECT c.contract_number, c.company, COUNT(a.id) as actividades, SUM(a.amount) as valor_total
            FROM contracts c
            LEFT JOIN activities a ON c.id = a.id_contract
            GROUP BY c.id, c.contract_number, c.company
            ORDER BY actividades DESC
        """)
        activities_by_contract = cursor.fetchall()
        for contract_number, company, activities, valor_total in activities_by_contract:
            print(f"   {contract_number} ({company}): {activities} actividades, ${valor_total or 0:,.2f}")
        
        # Consulta 7: Actividades activas vs inactivas
        print("\n📊 ESTADO DE ACTIVIDADES:")
        print("-" * 40)
        cursor.execute("SELECT vigente, COUNT(*) FROM activities GROUP BY vigente")
        activities_by_status = cursor.fetchall()
        for status, count in activities_by_status:
            status_text = "Activas" if status else "Inactivas"
            print(f"   {status_text}: {count} actividades")
        
        # Consulta 8: Promedio de valor por actividad
        print("\n📈 ESTADÍSTICAS DE ACTIVIDADES:")
        print("-" * 40)
        cursor.execute("SELECT AVG(amount), MIN(amount), MAX(amount) FROM activities")
        avg, min_val, max_val = cursor.fetchone()
        print(f"   Valor promedio: ${avg:,.2f}")
        print(f"   Valor mínimo: ${min_val:,.2f}")
        print(f"   Valor máximo: ${max_val:,.2f}")
        
        conn.close()
        print(f"\n✅ Consultas completadas")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    query_database()
