#!/usr/bin/env python3
"""
Script para probar el flujo completo de BI: Chat → SQL → Reporte Multivisual
"""
import requests
import json
import time

def test_complete_bi_flow():
    """Probar flujo completo de BI"""
    print("🔍 PROBANDO FLUJO COMPLETO DE BI")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    # Paso 1: Enviar mensaje al chat
    print("1️⃣ ENVIANDO MENSAJE AL CHAT")
    print("-" * 40)
    
    chat_data = {
        "message": "¿Cuántas actividades hay?",
        "conversation_history": []
    }
    
    try:
        response = requests.post(f"{base_url}/api/chat", json=chat_data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            chat_result = response.json()
            print(f"✅ Chat respuesta recibida")
            print(f"Respuesta: {chat_result.get('response', 'N/A')[:100]}...")
            print(f"Conversation ID: {chat_result.get('conversation_id', 'N/A')}")
        else:
            print(f"❌ Error en chat: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return False
    
    # Paso 2: Ejecutar consulta para generar reporte
    print("\n2️⃣ EJECUTANDO CONSULTA PARA GENERAR REPORTE")
    print("-" * 40)
    
    try:
        response = requests.post(f"{base_url}/api/execute-chat-query", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            execute_result = response.json()
            print(f"✅ Ejecución completada")
            print(f"Success: {execute_result.get('success', False)}")
            
            if execute_result.get('success'):
                print(f"Visualization Type: {execute_result.get('visualization_type', 'N/A')}")
                print(f"Data Keys: {list(execute_result.get('data', {}).keys())}")
                
                # Mostrar datos del reporte
                data = execute_result.get('data', {})
                if data:
                    print(f"\n📊 REPORTE GENERADO:")
                    print(f"Tipo: {data.get('type', 'N/A')}")
                    
                    if data.get('type') == 'kpi_cards':
                        cards = data.get('cards', [])
                        for card in cards:
                            print(f"  - {card.get('title', 'N/A')}: {card.get('value', 'N/A')}")
                    
                    elif data.get('type') == 'table':
                        print(f"  Columnas: {data.get('columns', [])}")
                        print(f"  Filas: {len(data.get('rows', []))}")
                    
                    elif data.get('type') == 'bar_chart':
                        print(f"  Datos: {len(data.get('data', []))} elementos")
                    
                    else:
                        print(f"  Datos: {data}")
            else:
                print(f"❌ Error en ejecución: {execute_result.get('error', 'N/A')}")
        else:
            print(f"❌ Error en ejecución: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en ejecución: {e}")
    
    # Paso 3: Probar con consulta más compleja
    print("\n3️⃣ PROBANDO CONSULTA COMPLEJA")
    print("-" * 40)
    
    chat_data = {
        "message": "Muéstrame los usuarios por rol",
        "conversation_history": []
    }
    
    try:
        response = requests.post(f"{base_url}/api/chat", json=chat_data, timeout=10)
        
        if response.status_code == 200:
            chat_result = response.json()
            print(f"✅ Chat complejo: {chat_result.get('response', 'N/A')[:100]}...")
            
            # Intentar ejecutar
            response = requests.post(f"{base_url}/api/execute-chat-query", timeout=10)
            
            if response.status_code == 200:
                execute_result = response.json()
                print(f"✅ Ejecución compleja: {execute_result.get('success', False)}")
                
                if execute_result.get('success'):
                    viz_type = execute_result.get('visualization_type', 'N/A')
                    print(f"Tipo de visualización: {viz_type}")
                    
                    data = execute_result.get('data', {})
                    if data:
                        print(f"📊 REPORTE COMPLEJO GENERADO:")
                        print(f"Tipo: {data.get('type', 'N/A')}")
                        
                        if data.get('type') == 'bar_chart':
                            chart_data = data.get('data', [])
                            print(f"  Datos del gráfico: {len(chart_data)} elementos")
                            for item in chart_data[:3]:  # Mostrar primeros 3
                                print(f"    {item.get('category', 'N/A')}: {item.get('value', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error en consulta compleja: {e}")
    
    print(f"\n🎯 RESUMEN DEL FLUJO:")
    print(f"✅ Chat funcionando")
    print(f"❓ Ejecución de consultas (revisar logs)")
    print(f"❓ Generación de reportes (revisar logs)")

def main():
    print("🚀 PRUEBA COMPLETA DEL FLUJO DE BI")
    print("=" * 60)
    print("🎯 Objetivo: Verificar que se generen reportes multivisuales")
    print()
    
    test_complete_bi_flow()

if __name__ == "__main__":
    main()
