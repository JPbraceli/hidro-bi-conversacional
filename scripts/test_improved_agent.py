#!/usr/bin/env python3
"""
Probar el agente mejorado con sinónimos
"""
import requests
import json
import time

def test_improved_agent():
    """Probar el agente mejorado"""
    print("🧪 PROBANDO AGENTE MEJORADO")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Verificar salud del backend
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print("✅ Backend conectado")
    except:
        print("❌ Backend no disponible - iniciando...")
        return
    
    # Probar consulta sobre operadoras
    print("\n1️⃣ Probando: 'lista las operadoras que existan'")
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "lista las operadoras que existan"},
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat exitoso")
            print(f"📝 Respuesta: {data.get('response', '')[:200]}...")
            print(f"💡 Sugerencias: {len(data.get('suggestions', []))}")
            print(f"🎯 Listo para ejecutar: {data.get('is_ready', False)}")
            
            if data.get('is_ready'):
                print("\n2️⃣ Ejecutando consulta...")
                exec_response = requests.post(
                    f"{base_url}/api/execute-chat-query",
                    timeout=20
                )
                
                if exec_response.status_code == 200:
                    exec_data = exec_response.json()
                    print(f"✅ Consulta ejecutada")
                    print(f"📊 Tipo: {exec_data.get('data', {}).get('visualization_type', 'N/A')}")
                    print(f"📈 Datos: {exec_data.get('data', {}).get('data', [])}")
                    
                    # Verificar si tiene datos
                    if exec_data.get('data', {}).get('data'):
                        print("🎉 ¡El agente está funcionando correctamente!")
                        print("📊 Datos encontrados:")
                        for item in exec_data.get('data', {}).get('data', [])[:5]:
                            print(f"   - {item}")
                    else:
                        print("⚠️ No se encontraron datos")
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

if __name__ == "__main__":
    test_improved_agent()
