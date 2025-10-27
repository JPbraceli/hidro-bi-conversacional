#!/usr/bin/env python3
"""
Script para probar el chat API directamente
"""
import requests
import json
import time

def test_chat_api():
    """Probar el chat API"""
    print("🤖 PROBANDO CHAT API")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Esperar un poco para que el servidor se inicie
    print("⏳ Esperando que el servidor se inicie...")
    time.sleep(3)
    
    try:
        # Probar conexión al servidor
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor backend funcionando")
        else:
            print(f"❌ Servidor no responde: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de que el backend esté ejecutándose")
        return False
    
    # Probar endpoint de chat
    print("\n🔍 Probando endpoint de chat...")
    
    chat_data = {
        "message": "¿Cuántas actividades hay?",
        "conversation_history": []
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json=chat_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat API funcionando")
            print(f"📝 Respuesta: {result.get('response', 'Sin respuesta')}")
            
            # Probar consulta SQL
            if 'sql_query' in result:
                print(f"🔍 SQL generado: {result['sql_query']}")
            
            return True
        else:
            print(f"❌ Error en chat API: {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_suggestions():
    """Probar endpoint de sugerencias"""
    print("\n💡 Probando sugerencias...")
    
    base_url = "http://localhost:8001"
    
    try:
        response = requests.get(f"{base_url}/api/suggestions", timeout=5)
        
        if response.status_code == 200:
            suggestions = response.json()
            print("✅ Sugerencias funcionando")
            print(f"📋 Sugerencias: {suggestions}")
        else:
            print(f"❌ Error en sugerencias: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 PRUEBA COMPLETA DEL CHAT API")
    print("=" * 60)
    
    # Probar chat
    chat_ok = test_chat_api()
    
    # Probar sugerencias
    test_suggestions()
    
    if chat_ok:
        print(f"\n🎉 ¡CHAT FUNCIONANDO!")
        print(f"🌐 URL del chat: http://localhost:3000")
        print(f"📚 API Docs: http://localhost:8001/docs")
        print(f"💡 Para iniciar el frontend:")
        print(f"   cd frontend && npm run dev")
    else:
        print(f"\n❌ Hay problemas con el chat")
        print(f"💡 Verifica que el backend esté ejecutándose")

if __name__ == "__main__":
    main()
