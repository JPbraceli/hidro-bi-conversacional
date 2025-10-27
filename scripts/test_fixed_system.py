#!/usr/bin/env python3
"""
Probar el sistema corregido
"""
import requests
import json
import time

def test_system():
    """Probar el sistema corregido"""
    print("🧪 PROBANDO SISTEMA CORREGIDO")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Verificar salud del backend
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print("✅ Backend conectado")
    except:
        print("❌ Backend no disponible")
        return
    
    # Probar consulta simple
    print("\n1️⃣ Probando consulta simple...")
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "¿Cuántas actividades hay?"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat exitoso")
            print(f"📝 Respuesta: {data.get('response', '')[:100]}...")
            print(f"💡 Sugerencias: {len(data.get('suggestions', []))}")
            print(f"🎯 Listo para ejecutar: {data.get('is_ready', False)}")
            
            if data.get('is_ready'):
                print("\n2️⃣ Ejecutando consulta...")
                exec_response = requests.post(
                    f"{base_url}/api/execute-chat-query",
                    timeout=15
                )
                
                if exec_response.status_code == 200:
                    exec_data = exec_response.json()
                    print(f"✅ Consulta ejecutada")
                    print(f"📊 Tipo: {exec_data.get('data', {}).get('visualization_type', 'N/A')}")
                    print(f"📈 Datos: {exec_data.get('data', {}).get('data', [])}")
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
    test_system()
