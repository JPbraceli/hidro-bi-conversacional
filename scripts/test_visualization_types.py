#!/usr/bin/env python3
"""
Probar diferentes tipos de visualización
"""
import requests
import json
import time

def test_visualization_types():
    """Probar diferentes tipos de visualización"""
    print("🧪 PROBANDO DIFERENTES TIPOS DE VISUALIZACIÓN")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    # Verificar salud del backend
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print("✅ Backend conectado")
    except:
        print("❌ Backend no disponible")
        return
    
    # Casos de prueba para diferentes tipos de visualización
    test_cases = [
        {
            "name": "Gráfico de Pastel - Proporciones",
            "query": "¿Cuál es la proporción de actividades activas vs inactivas?",
            "expected": "pie_chart"
        },
        {
            "name": "Gráfico de Líneas - Tendencias",
            "query": "Muéstrame las tendencias de actividades por año",
            "expected": "line_chart"
        },
        {
            "name": "KPIs - Métricas",
            "query": "Muéstrame los KPIs principales del sistema",
            "expected": "kpi_cards"
        },
        {
            "name": "Gráfico de Barras - Comparaciones",
            "query": "Muéstrame las empresas por número de contratos",
            "expected": "bar_chart"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ {test_case['name']}")
        print(f"📝 Consulta: {test_case['query']}")
        print(f"🎯 Esperado: {test_case['expected']}")
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
                        viz_type = exec_data.get('data', {}).get('visualization_type', 'N/A')
                        print(f"📊 Tipo generado: {viz_type}")
                        
                        if viz_type == test_case['expected']:
                            print(f"🎉 ¡CORRECTO! Generó {viz_type}")
                        else:
                            print(f"⚠️ Esperado {test_case['expected']}, obtuvo {viz_type}")
                        
                        # Mostrar datos si es KPI
                        if viz_type == "kpi_cards":
                            cards = exec_data.get('data', {}).get('cards', [])
                            for card in cards:
                                print(f"   📊 {card.get('title', 'N/A')}: {card.get('value', 'N/A')}")
                    else:
                        print(f"❌ Error en ejecución: {exec_response.status_code}")
                else:
                    print("⚠️ No está listo para ejecutar")
            else:
                print(f"❌ Error en chat: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(2)  # Pausa entre pruebas
    
    print(f"\n🎉 PRUEBA DE VISUALIZACIONES COMPLETADA")

if __name__ == "__main__":
    test_visualization_types()
