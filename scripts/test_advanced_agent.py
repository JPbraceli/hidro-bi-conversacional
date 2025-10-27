#!/usr/bin/env python3
"""
Prueba completa del Agente Avanzado HIDRO
Testea todas las capacidades del agente inteligente
"""
import requests
import json
import time
from datetime import datetime

def test_advanced_agent():
    """Prueba completa del agente avanzado"""
    print("🤖 PRUEBA COMPLETA DEL AGENTE AVANZADO HIDRO")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    # Lista de pruebas
    test_cases = [
        {
            "name": "1. Exploración inicial",
            "message": "hola, que análisis puedo hacer con estos datos?",
            "expected": "sugerencias inteligentes basadas en datos reales"
        },
        {
            "name": "2. Análisis de actividades",
            "message": "muéstrame las actividades por año",
            "expected": "gráfico de líneas + tabla con datos temporales"
        },
        {
            "name": "3. Análisis de contratos",
            "message": "muéstrame las empresas por valor de contratos",
            "expected": "gráfico de barras + ranking de empresas"
        },
        {
            "name": "4. Análisis cruzado",
            "message": "muéstrame la correlación entre actividades y contratos",
            "expected": "análisis multivisual conectando ambas tablas"
        },
        {
            "name": "5. Sugerencias inteligentes",
            "message": "que más puedo analizar?",
            "expected": "sugerencias basadas en datos disponibles"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 {test_case['name']}")
        print(f"📝 Mensaje: {test_case['message']}")
        print(f"🎯 Esperado: {test_case['expected']}")
        print("-" * 40)
        
        try:
            # Enviar mensaje
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": test_case['message']},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Analizar respuesta
                print(f"✅ Status: {response.status_code}")
                print(f"📊 Respuesta: {data.get('text', '')[:200]}...")
                print(f"💡 Sugerencias: {len(data.get('suggestions', []))}")
                print(f"🔍 Listo para ejecutar: {data.get('is_ready', False)}")
                
                # Verificar si hay visualización
                if data.get('is_ready'):
                    print("🎨 Generando visualización...")
                    
                    # Ejecutar consulta si está lista
                    exec_response = requests.post(
                        f"{base_url}/api/execute-chat-query",
                        timeout=30
                    )
                    
                    if exec_response.status_code == 200:
                        exec_data = exec_response.json()
                        print(f"📈 Tipo de visualización: {exec_data.get('data', {}).get('visualization_type', 'N/A')}")
                        print(f"📊 Registros: {exec_data.get('data', {}).get('row_count', 0)}")
                    else:
                        print(f"❌ Error en ejecución: {exec_response.status_code}")
                
                results.append({
                    "test": test_case['name'],
                    "status": "PASS",
                    "response_time": response.elapsed.total_seconds(),
                    "suggestions_count": len(data.get('suggestions', [])),
                    "is_ready": data.get('is_ready', False)
                })
                
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                results.append({
                    "test": test_case['name'],
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}"
                })
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {str(e)}")
            results.append({
                "test": test_case['name'],
                "status": "FAIL",
                "error": str(e)
            })
        
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            results.append({
                "test": test_case['name'],
                "status": "FAIL",
                "error": str(e)
            })
        
        # Pausa entre pruebas
        time.sleep(2)
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = len([r for r in results if r['status'] == 'PASS'])
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"📈 Tasa de éxito: {(passed/total*100):.1f}%")
    
    # Detalles por prueba
    for result in results:
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_icon} {result['test']}: {result['status']}")
        
        if result['status'] == 'PASS':
            print(f"   ⏱️  Tiempo: {result.get('response_time', 0):.2f}s")
            print(f"   💡 Sugerencias: {result.get('suggestions_count', 0)}")
            print(f"   🎨 Visualización: {'Sí' if result.get('is_ready', False) else 'No'}")
        else:
            print(f"   ❌ Error: {result.get('error', 'Desconocido')}")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results_advanced_agent_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "summary": {
                "total_tests": total,
                "passed": passed,
                "success_rate": f"{(passed/total*100):.1f}%"
            },
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {results_file}")
    
    return results

def test_agent_capabilities():
    """Prueba específica de capacidades del agente"""
    print("\n🧠 PRUEBA DE CAPACIDADES DEL AGENTE")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    # Prueba de exploración automática
    print("\n🔍 1. Exploración automática de datos")
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "explora los datos y dime qué puedes analizar"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get('suggestions', [])
            print(f"✅ Exploración exitosa")
            print(f"💡 Sugerencias generadas: {len(suggestions)}")
            for i, suggestion in enumerate(suggestions[:3], 1):
                print(f"   {i}. {suggestion}")
        else:
            print(f"❌ Error en exploración: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Prueba de detección de patrones
    print("\n📊 2. Detección de patrones")
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "muéstrame las tendencias temporales"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Análisis de tendencias exitoso")
            print(f"🎯 Respuesta: {data.get('text', '')[:100]}...")
        else:
            print(f"❌ Error en tendencias: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Prueba de análisis cruzado
    print("\n🔗 3. Análisis cruzado entre tablas")
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "muéstrame un dashboard completo con todas las métricas"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard completo generado")
            print(f"🎯 Respuesta: {data.get('text', '')[:100]}...")
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA COMPLETA DEL AGENTE AVANZADO")
    print("⏰ Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        print("✅ Backend conectado")
    except:
        print("❌ Backend no disponible. Iniciando...")
        print("💡 Asegúrate de que el backend esté corriendo en puerto 8001")
        exit(1)
    
    # Ejecutar pruebas
    results = test_advanced_agent()
    test_agent_capabilities()
    
    print("\n🎉 PRUEBA COMPLETA FINALIZADA")
    print("=" * 60)
