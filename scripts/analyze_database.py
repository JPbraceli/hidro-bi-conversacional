#!/usr/bin/env python3
"""
Analizar la base de datos HIDRO para generar preguntas sugeridas
"""
import sqlite3
import json

def analyze_database():
    """Analizar la base de datos y generar preguntas sugeridas"""
    print("📊 ANÁLISIS DE LA BASE DE DATOS HIDRO")
    print("=" * 60)
    
    conn = sqlite3.connect('hidro_data.db')
    cursor = conn.cursor()
    
    # Obtener tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    tables = cursor.fetchall()
    
    print(f"📋 Tablas disponibles: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    print("\n" + "=" * 60)
    
    # Analizar cada tabla
    table_analysis = {}
    
    for table in tables:
        table_name = table[0]
        print(f"\n🔍 TABLA: {table_name.upper()}")
        
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   📊 Registros: {count}")
        
        # Obtener columnas
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"   📝 Columnas: {len(columns)}")
        
        column_info = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            print(f"      - {col_name} ({col_type})")
            column_info.append({"name": col_name, "type": col_type})
        
        # Muestra de datos
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample = cursor.fetchall()
            print(f"   📄 Muestra de datos:")
            for i, row in enumerate(sample, 1):
                print(f"      {i}. {row}")
        
        table_analysis[table_name] = {
            "count": count,
            "columns": column_info,
            "sample_data": sample if count > 0 else []
        }
    
    conn.close()
    
    # Generar preguntas sugeridas
    print("\n" + "=" * 60)
    print("💡 PREGUNTAS SUGERIDAS PARA EL AGENTE")
    print("=" * 60)
    
    generate_questions(table_analysis)

def generate_questions(table_analysis):
    """Generar preguntas basadas en el análisis de la BD"""
    
    # Preguntas generales
    print("\n🌐 PREGUNTAS GENERALES:")
    print("1. ¿Qué datos tengo disponibles en el sistema?")
    print("2. Muéstrame un resumen completo de todas las tablas")
    print("3. ¿Cuáles son las métricas principales del sistema?")
    print("4. Muéstrame un dashboard ejecutivo")
    
    # Preguntas por tabla
    for table_name, analysis in table_analysis.items():
        if analysis["count"] > 0:
            print(f"\n📊 PREGUNTAS SOBRE {table_name.upper()}:")
            
            if table_name == "activities":
                print("5. ¿Cuántas actividades hay en total?")
                print("6. ¿Cuántas actividades están activas?")
                print("7. Muéstrame las actividades por año")
                print("8. ¿Cuáles son las actividades más costosas?")
                print("9. Muéstrame la distribución de actividades por estado")
                print("10. ¿Cuál es el valor total de las actividades?")
                
            elif table_name == "contracts":
                print("11. ¿Cuántos contratos hay?")
                print("12. Muéstrame las empresas por número de contratos")
                print("13. ¿Cuál es el valor total de los contratos?")
                print("14. Muéstrame los contratos por empresa ordenados por valor")
                print("15. ¿Cuáles son los contratos más valiosos?")
                print("16. Muéstrame la distribución de contratos por estado")
                
            elif table_name == "profiles":
                print("17. ¿Cuántos usuarios hay registrados?")
                print("18. Muéstrame la distribución de usuarios por rol")
                print("19. ¿Cuáles son los roles más comunes?")
                print("20. Muéstrame los perfiles de usuario")
                
            elif table_name == "gateways":
                print("21. ¿Cuántos gateways hay?")
                print("22. Muéstrame los gateways por ubicación")
                print("23. ¿Cuál es el estado de los gateways?")
                print("24. Muéstrame la distribución de gateways por estado")
                
            elif table_name == "admin_users":
                print("25. ¿Cuántos administradores hay?")
                print("26. Muéstrame los usuarios admin por rol")
                print("27. ¿Cuáles son los permisos de administración?")
    
    # Preguntas de análisis cruzado
    print("\n🔗 ANÁLISIS CRUZADO:")
    print("28. Muéstrame la correlación entre actividades y contratos")
    print("29. ¿Cuáles son las empresas con más actividades?")
    print("30. Muéstrame el rendimiento por contrato")
    print("31. ¿Cuáles son las actividades más rentables?")
    print("32. Muéstrame un análisis completo de rentabilidad")
    
    # Preguntas de tendencias
    print("\n📈 ANÁLISIS DE TENDENCIAS:")
    print("33. Muéstrame las tendencias temporales de actividades")
    print("34. ¿Cómo han evolucionado los contratos en el tiempo?")
    print("35. Muéstrame la evolución de usuarios por año")
    print("36. ¿Cuáles son las tendencias principales del sistema?")
    
    # Preguntas de KPIs
    print("\n🎯 INDICADORES CLAVE (KPIs):")
    print("37. Muéstrame los KPIs principales del sistema")
    print("38. ¿Cuáles son las métricas más importantes?")
    print("39. Muéstrame un dashboard de KPIs")
    print("40. ¿Cuáles son los indicadores de rendimiento?")
    
    # Preguntas de visualización específica
    print("\n📊 VISUALIZACIONES ESPECÍFICAS:")
    print("41. Muéstrame un gráfico de barras de empresas por contratos")
    print("42. Muéstrame un gráfico de pastel de usuarios por rol")
    print("43. Muéstrame un gráfico de líneas de actividades por año")
    print("44. Muéstrame un mapa de calor de rendimiento")
    print("45. Muéstrame un gráfico de dispersión de valor vs tiempo")
    
    print("\n" + "=" * 60)
    print("💡 CONSEJOS PARA USAR EL AGENTE:")
    print("=" * 60)
    print("• Puedes hacer preguntas en lenguaje natural")
    print("• El agente te sugerirá análisis automáticamente")
    print("• Puedes pedir visualizaciones específicas (barras, pastel, líneas, etc.)")
    print("• El agente conectará datos entre tablas automáticamente")
    print("• Puedes pedir dashboards completos")
    print("• El agente detectará patrones y anomalías automáticamente")

if __name__ == "__main__":
    analyze_database()
