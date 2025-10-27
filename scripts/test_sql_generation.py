#!/usr/bin/env python3
"""
Probar la generación de SQL correcta
"""
import requests
import json
import time

def test_sql_generation():
    """Probar que el SQL se genera correctamente"""
    print("🧪 PROBANDO GENERACIÓN DE SQL CORRECTA")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Verificar salud del backend
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print("✅ Backend conectado")
    except:
        print("❌ Backend no disponible")
        return
    
    # Casos de prueba para SQL problemático
    test_cases = [
        {
            "name": "Tendencias por año",
            "query": "Muéstrame las tendencias de actividades por año",
            "expected_sql": "SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania"
        },
        {
            "name": "Evolución por año", 
            "query": "Muéstrame la evolución de actividades por año",
            "expected_sql": "SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania"
        },
        {
            "name": "Proporción activas vs inactivas",
            "query": "¿Cuál es la proporción de actividades activas vs inactivas?",
            "expected_sql": "SELECT vigente, COUNT(*) as total FROM activities GROUP BY vigente"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ {test_case['name']}")
        print(f"📝 Consulta: {test_case['query']}")
        print(f"🎯 SQL esperado: {test_case['expected_sql']}")
        print("-" * 50)
        
        try:
            # Chat
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": test_case['query']},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat exitoso")
                print(f"📝 Respuesta: {data.get('response', '')[:100]}...")
                print(f"🎯 Listo para ejecutar: {data.get('is_ready', False)}")
                
                if data.get('is_ready'):
                    # Ejecutar consulta
                    exec_response = requests.post(
                        f"{base_url}/api/execute-chat-query",
                        timeout=15
                    )
                    
                    if exec_response.status_code == 200:
                        exec_data = exec_response.json()
                        print(f"✅ Consulta ejecutada exitosamente")
                        print(f"📊 Tipo: {exec_data.get('data', {}).get('visualization_type', 'N/A')}")
                        print(f"📈 Registros: {exec_data.get('data', {}).get('row_count', 0)}")
                    else:
                        print(f"❌ Error en ejecución: {exec_response.status_code}")
                        print(f"📝 Error: {exec_response.text}")
                else:
                    print("⚠️ No está listo para ejecutar")
            else:
                print(f"❌ Error en chat: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(2)  # Pausa entre pruebas
    
    print(f"\n🎉 PRUEBA DE SQL COMPLETADA")

if __name__ == "__main__":
    test_sql_generation()
