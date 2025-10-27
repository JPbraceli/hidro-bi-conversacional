#!/usr/bin/env python3
"""
Prueba del flujo completo: Chat → Auto-ejecución → Visualización
"""
import requests
import json
import time

def test_complete_flow():
    """Probar el flujo completo del agente avanzado"""
    print("🔄 PRUEBA DEL FLUJO COMPLETO")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Paso 1: Enviar mensaje
    print("1️⃣ Enviando mensaje al chat...")
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "Cuantas operadoras existen? podrias ordenarlas de mayor a menor en un grafico de barras?"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat exitoso")
            print(f"📝 Respuesta: {data.get('response', '')[:100]}...")
            print(f"💡 Sugerencias: {len(data.get('suggestions', []))}")
            print(f"🎯 Listo para ejecutar: {data.get('is_ready', False)}")
            
            if data.get('is_ready'):
                print("\n2️⃣ Ejecutando consulta automáticamente...")
                
                # Paso 2: Ejecutar consulta
                exec_response = requests.post(
                    f"{base_url}/api/execute-chat-query",
                    timeout=30
                )
                
                if exec_response.status_code == 200:
                    exec_data = exec_response.json()
                    print(f"✅ Consulta ejecutada exitosamente")
                    print(f"📊 Tipo de visualización: {exec_data.get('data', {}).get('visualization_type', 'N/A')}")
                    print(f"📈 Datos: {exec_data.get('data', {}).get('data', [])}")
                    
                    # Verificar si es un gráfico de barras
                    if exec_data.get('data', {}).get('visualization_type') == 'bar_chart':
                        print("🎉 ¡Gráfico de barras generado correctamente!")
                        print("📊 Datos del gráfico:")
                        for item in exec_data.get('data', {}).get('data', []):
                            print(f"   - {item.get('category', 'N/A')}: {item.get('value', 0)}")
                    else:
                        print(f"⚠️ Tipo de visualización inesperado: {exec_data.get('data', {}).get('visualization_type')}")
                    
                else:
                    print(f"❌ Error en ejecución: {exec_response.status_code}")
                    print(f"📝 Respuesta: {exec_response.text}")
            else:
                print("⚠️ No está listo para ejecutar")
                
        else:
            print(f"❌ Error en chat: {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_different_queries():
    """Probar diferentes tipos de consultas"""
    print("\n🧪 PROBANDO DIFERENTES CONSULTAS")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    queries = [
        "¿Cuántas actividades hay en total?",
        "Muéstrame las empresas por número de contratos",
        "¿Cuáles son las actividades más costosas?",
        "Muéstrame un dashboard completo"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Probando: {query}")
        try:
            # Chat
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Chat: {data.get('is_ready', False)}")
                
                if data.get('is_ready'):
                    # Ejecutar
                    exec_response = requests.post(
                        f"{base_url}/api/execute-chat-query",
                        timeout=30
                    )
                    
                    if exec_response.status_code == 200:
                        exec_data = exec_response.json()
                        viz_type = exec_data.get('data', {}).get('visualization_type', 'N/A')
                        row_count = exec_data.get('data', {}).get('row_count', 0)
                        print(f"   ✅ Ejecución: {viz_type} ({row_count} registros)")
                    else:
                        print(f"   ❌ Error ejecución: {exec_response.status_code}")
                else:
                    print(f"   ⚠️ No listo para ejecutar")
            else:
                print(f"   ❌ Error chat: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DEL FLUJO COMPLETO")
    print("⏰ Timestamp:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Verificar backend
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        print("✅ Backend conectado")
    except:
        print("❌ Backend no disponible")
        exit(1)
    
    # Ejecutar pruebas
    test_complete_flow()
    test_different_queries()
    
    print("\n🎉 PRUEBA COMPLETA FINALIZADA")
