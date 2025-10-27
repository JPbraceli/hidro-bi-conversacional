#!/usr/bin/env python3
"""
Generar lista de preguntas para la base de datos expandida
"""
import sqlite3

def generate_expanded_questions():
    """Generar preguntas para la base de datos expandida"""
    print("🎯 PREGUNTAS PARA LA BASE DE DATOS EXPANDIDA")
    print("=" * 70)
    
    # Conectar a la BD
    conn = sqlite3.connect("hidro_data.db")
    cursor = conn.cursor()
    
    # Obtener estadísticas
    cursor.execute("SELECT COUNT(*) FROM activities")
    activities_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM contracts")
    contracts_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM profiles")
    profiles_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM gateways")
    gateways_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    admin_count = cursor.fetchone()[0]
    
    print(f"📊 DATOS DISPONIBLES:")
    print(f"   - {activities_count} actividades")
    print(f"   - {contracts_count} contratos")
    print(f"   - {profiles_count} perfiles de usuario")
    print(f"   - {gateways_count} gateways")
    print(f"   - {admin_count} usuarios admin")
    print(f"   📊 Total: {activities_count + contracts_count + profiles_count + gateways_count + admin_count} registros")
    
    print("\n" + "=" * 70)
    print("💡 PREGUNTAS RECOMENDADAS PARA EL AGENTE")
    print("=" * 70)
    
    # Preguntas generales
    print("\n🌐 PREGUNTAS GENERALES:")
    print("1. ¿Qué datos tengo disponibles en el sistema?")
    print("2. Muéstrame un resumen ejecutivo completo")
    print("3. ¿Cuáles son las métricas principales del sistema?")
    print("4. Muéstrame un dashboard ejecutivo completo")
    print("5. ¿Cuál es el estado general del sistema?")
    
    # Preguntas sobre actividades (50 registros)
    print(f"\n📊 PREGUNTAS SOBRE ACTIVIDADES ({activities_count} registros):")
    print("6. ¿Cuántas actividades hay en total?")
    print("7. ¿Cuántas actividades están activas vs inactivas?")
    print("8. Muéstrame las actividades por año de campaña")
    print("9. ¿Cuáles son las actividades más costosas?")
    print("10. Muéstrame la distribución de actividades por tipo")
    print("11. ¿Cuál es el valor total de todas las actividades?")
    print("12. Muéstrame las actividades por ubicación")
    print("13. ¿Cuáles son las tendencias de actividades por mes?")
    print("14. Muéstrame un análisis de rentabilidad por actividad")
    print("15. ¿Cuáles son las actividades con mayor duración?")
    
    # Preguntas sobre contratos (20 registros)
    print(f"\n🏢 PREGUNTAS SOBRE CONTRATOS ({contracts_count} registros):")
    print("16. ¿Cuántos contratos hay en total?")
    print("17. Muéstrame las empresas por número de contratos")
    print("18. ¿Cuál es el valor total de todos los contratos?")
    print("19. Muéstrame los contratos por empresa ordenados por valor")
    print("20. ¿Cuáles son los contratos más valiosos?")
    print("21. Muéstrame la distribución de contratos por estado")
    print("22. ¿Cuál es el valor promedio de los contratos?")
    print("23. Muéstrame los contratos por rango de valor")
    print("24. ¿Cuáles son las empresas con mayor inversión?")
    print("25. Muéstrame la evolución de contratos en el tiempo")
    
    # Preguntas sobre perfiles (30 registros)
    print(f"\n👥 PREGUNTAS SOBRE PERFILES ({profiles_count} registros):")
    print("26. ¿Cuántos usuarios hay registrados?")
    print("27. Muéstrame la distribución de usuarios por rol")
    print("28. ¿Cuáles son los roles más comunes?")
    print("29. Muéstrame los perfiles por ubicación")
    print("30. ¿Cuál es la distribución de usuarios por experiencia?")
    print("31. Muéstrame los usuarios más activos")
    print("32. ¿Cuáles son los perfiles más recientes?")
    print("33. Muéstrame un análisis de recursos humanos")
    print("34. ¿Cuál es la distribución de usuarios por departamento?")
    print("35. Muéstrame los perfiles por nivel de responsabilidad")
    
    # Preguntas sobre gateways (15 registros)
    print(f"\n🌐 PREGUNTAS SOBRE GATEWAYS ({gateways_count} registros):")
    print("36. ¿Cuántos gateways hay en total?")
    print("37. Muéstrame los gateways por ubicación")
    print("38. ¿Cuál es el estado de los gateways?")
    print("39. Muéstrame la distribución de gateways por estado")
    print("40. ¿Cuáles son los gateways más utilizados?")
    print("41. Muéstrame los gateways por región")
    print("42. ¿Cuál es la disponibilidad de los gateways?")
    print("43. Muéstrame un análisis de rendimiento de gateways")
    print("44. ¿Cuáles son los gateways que necesitan mantenimiento?")
    print("45. Muéstrame la distribución geográfica de gateways")
    
    # Preguntas sobre admin (10 registros)
    print(f"\n🔐 PREGUNTAS SOBRE ADMINISTRACIÓN ({admin_count} registros):")
    print("46. ¿Cuántos administradores hay?")
    print("47. Muéstrame los usuarios admin por rol")
    print("48. ¿Cuáles son los permisos de administración?")
    print("49. Muéstrame la distribución de administradores por nivel")
    print("50. ¿Cuál es la estructura organizacional?")
    
    # Análisis cruzado
    print(f"\n🔗 ANÁLISIS CRUZADO (Datos completos):")
    print("51. Muéstrame la correlación entre actividades y contratos")
    print("52. ¿Cuáles son las empresas con más actividades?")
    print("53. Muéstrame el rendimiento por contrato")
    print("54. ¿Cuáles son las actividades más rentables?")
    print("55. Muéstrame un análisis completo de rentabilidad")
    print("56. ¿Cuál es la eficiencia por empresa?")
    print("57. Muéstrame la correlación entre usuarios y actividades")
    print("58. ¿Cuáles son los gateways más utilizados por actividad?")
    print("59. Muéstrame un análisis de costos por ubicación")
    print("60. ¿Cuál es el ROI por contrato?")
    
    # Análisis de tendencias
    print(f"\n📈 ANÁLISIS DE TENDENCIAS:")
    print("61. Muéstrame las tendencias temporales de actividades")
    print("62. ¿Cómo han evolucionado los contratos en el tiempo?")
    print("63. Muéstrame la evolución de usuarios por año")
    print("64. ¿Cuáles son las tendencias principales del sistema?")
    print("65. Muéstrame la evolución de costos por período")
    print("66. ¿Cuáles son los patrones estacionales?")
    print("67. Muéstrame la evolución de la rentabilidad")
    print("68. ¿Cuáles son las tendencias de crecimiento?")
    print("69. Muéstrame la evolución de la eficiencia operacional")
    print("70. ¿Cuáles son las proyecciones futuras?")
    
    # KPIs y métricas
    print(f"\n🎯 INDICADORES CLAVE (KPIs):")
    print("71. Muéstrame los KPIs principales del sistema")
    print("72. ¿Cuáles son las métricas más importantes?")
    print("73. Muéstrame un dashboard de KPIs")
    print("74. ¿Cuáles son los indicadores de rendimiento?")
    print("75. Muéstrame los indicadores de eficiencia")
    print("76. ¿Cuáles son los indicadores de rentabilidad?")
    print("77. Muéstrame los indicadores de crecimiento")
    print("78. ¿Cuáles son los indicadores de calidad?")
    print("79. Muéstrame los indicadores de satisfacción")
    print("80. ¿Cuáles son los indicadores de riesgo?")
    
    # Visualizaciones específicas
    print(f"\n📊 VISUALIZACIONES ESPECÍFICAS:")
    print("81. Muéstrame un gráfico de barras de empresas por contratos")
    print("82. Muéstrame un gráfico de pastel de usuarios por rol")
    print("83. Muéstrame un gráfico de líneas de actividades por año")
    print("84. Muéstrame un mapa de calor de rendimiento")
    print("85. Muéstrame un gráfico de dispersión de valor vs tiempo")
    print("86. Muéstrame un gráfico de radar de KPIs")
    print("87. Muéstrame un gráfico de área de tendencias")
    print("88. Muéstrame un gráfico de barras horizontales de costos")
    print("89. Muéstrame un gráfico de dona de distribución")
    print("90. Muéstrame un gráfico de burbujas de correlación")
    
    # Dashboards completos
    print(f"\n📊 DASHBOARDS COMPLETOS:")
    print("91. Muéstrame un dashboard ejecutivo completo")
    print("92. Muéstrame un dashboard operacional")
    print("93. Muéstrame un dashboard financiero")
    print("94. Muéstrame un dashboard de recursos humanos")
    print("95. Muéstrame un dashboard de operaciones")
    print("96. Muéstrame un dashboard de rendimiento")
    print("97. Muéstrame un dashboard de calidad")
    print("98. Muéstrame un dashboard de riesgos")
    print("99. Muéstrame un dashboard de crecimiento")
    print("100. Muéstrame un dashboard integral del sistema")
    
    print("\n" + "=" * 70)
    print("💡 CONSEJOS PARA USAR EL AGENTE:")
    print("=" * 70)
    print("• Puedes hacer preguntas en lenguaje natural")
    print("• El agente te sugerirá análisis automáticamente")
    print("• Puedes pedir visualizaciones específicas (barras, pastel, líneas, etc.)")
    print("• El agente conectará datos entre tablas automáticamente")
    print("• Puedes pedir dashboards completos")
    print("• El agente detectará patrones y anomalías automáticamente")
    print("• Con 125 registros, el agente puede hacer análisis más profundos")
    print("• Los datos incluyen empresas reales del sector hidrocarburos")
    print("• Los análisis serán más realistas y representativos")
    
    conn.close()

if __name__ == "__main__":
    generate_expanded_questions()
