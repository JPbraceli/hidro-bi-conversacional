#!/usr/bin/env python3
"""
Script interactivo para hacer consultas personalizadas a la base de datos
"""
import sqlite3
import os

def interactive_query():
    """Interfaz interactiva para consultas SQL"""
    db_path = "hidro_data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 CONSULTAS INTERACTIVAS A LA BASE HIDRO")
        print("=" * 50)
        print("💡 Escribe 'help' para ver comandos disponibles")
        print("💡 Escribe 'exit' para salir")
        print("💡 Escribe 'tables' para ver las tablas disponibles")
        print()
        
        while True:
            try:
                query = input("SQL> ").strip()
                
                if query.lower() == 'exit':
                    print("👋 ¡Hasta luego!")
                    break
                
                if query.lower() == 'help':
                    print("\n📋 COMANDOS DISPONIBLES:")
                    print("   help     - Mostrar esta ayuda")
                    print("   tables   - Listar tablas disponibles")
                    print("   exit     - Salir del programa")
                    print("   SQL      - Escribir consulta SQL directamente")
                    print("\n📋 EJEMPLOS DE CONSULTAS:")
                    print("   SELECT * FROM activities LIMIT 5")
                    print("   SELECT COUNT(*) FROM contracts")
                    print("   SELECT role, COUNT(*) FROM profiles GROUP BY role")
                    print()
                    continue
                
                if query.lower() == 'tables':
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
                    tables = cursor.fetchall()
                    print("\n📋 TABLAS DISPONIBLES:")
                    for table_name, in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        print(f"   {table_name} ({count} registros)")
                    print()
                    continue
                
                if not query:
                    continue
                
                # Ejecutar consulta
                cursor.execute(query)
                results = cursor.fetchall()
                
                if results:
                    print(f"\n✅ Resultados ({len(results)} filas):")
                    print("-" * 50)
                    for i, row in enumerate(results, 1):
                        print(f"   {i}. {row}")
                    print()
                else:
                    print("✅ Consulta ejecutada (sin resultados)")
                    print()
                    
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_query()
