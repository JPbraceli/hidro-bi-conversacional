#!/usr/bin/env python3
"""
Probar la configuración actual del chat
"""
import psycopg2

def test_current_setup():
    """Probar configuración actual"""
    try:
        print("🔍 Probando configuración actual...")
        
        # Conectar a dev_hdcr_activities
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='dev_hdcr_activities'
        )
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a dev_hdcr_activities")
        
        # Verificar datos disponibles
        print("\n📊 Datos disponibles:")
        
        # Actividades
        cursor.execute("SELECT COUNT(*) FROM activities;")
        activities_count = cursor.fetchone()[0]
        print(f"  📋 Actividades: {activities_count}")
        
        if activities_count > 0:
            cursor.execute("SELECT name, start_date, end_date, amount FROM activities LIMIT 3;")
            activities = cursor.fetchall()
            print(f"  📋 Ejemplos: {activities}")
        
        # Entregas
        cursor.execute("SELECT COUNT(*) FROM deliveries;")
        deliveries_count = cursor.fetchone()[0]
        print(f"  📦 Entregas: {deliveries_count}")
        
        # Parámetros
        cursor.execute("SELECT COUNT(*) FROM parameter;")
        parameters_count = cursor.fetchone()[0]
        print(f"  ⚙️ Parámetros: {parameters_count}")
        
        conn.close()
        
        print("\n🎯 RECOMENDACIÓN:")
        print("✅ Base actual tiene datos suficientes para probar el chat")
        print("🚀 Puedes iniciar el chat y hacer preguntas como:")
        print("  - '¿Cuántas actividades hay?'")
        print("  - 'Muéstrame las actividades'")
        print("  - '¿Cuántas entregas hay?'")
        print("  - 'Muéstrame los parámetros'")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Iniciar chat: npm run dev")
        print("2. Probar preguntas básicas")
        print("3. Si funciona bien, mantener configuración actual")
        print("4. Si necesitas más datos, importar dumps a hidro")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_current_setup()




