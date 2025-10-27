#!/usr/bin/env python3
"""
Listar las operadoras/empresas del sistema HIDRO
"""
import sqlite3

def list_operadoras():
    """Listar todas las operadoras/empresas"""
    print("OPERADORAS/EMPRESAS EN EL SISTEMA HIDRO")
    print("=" * 50)
    
    conn = sqlite3.connect("hidro_data.db")
    cursor = conn.cursor()
    
    # Obtener empresas de la tabla contracts
    cursor.execute("SELECT DISTINCT company FROM contracts ORDER BY company")
    companies = cursor.fetchall()
    
    print(f"Total de empresas: {len(companies)}")
    print()
    
    for i, company in enumerate(companies, 1):
        print(f"{i}. {company[0]}")
    
    # Obtener estadísticas adicionales
    cursor.execute("""
        SELECT company, COUNT(*) as contratos, SUM(value) as valor_total 
        FROM contracts 
        GROUP BY company 
        ORDER BY valor_total DESC
    """)
    stats = cursor.fetchall()
    
    print()
    print("ESTADISTICAS POR EMPRESA:")
    print("-" * 50)
    for company, contratos, valor in stats:
        print(f"Empresa: {company}")
        print(f"  Contratos: {contratos}")
        print(f"  Valor total: ${valor:,.2f}")
        print()
    
    conn.close()

if __name__ == "__main__":
    list_operadoras()
