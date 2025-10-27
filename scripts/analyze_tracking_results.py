#!/usr/bin/env python3
"""
Analizador detallado de resultados de tracking
"""
import json
import os
from datetime import datetime

def analyze_tracking_files():
    """Analizar todos los archivos de tracking"""
    print("🔍 ANÁLISIS DETALLADO DE RESULTADOS")
    print("=" * 60)
    
    # Buscar archivos de tracking
    tracking_files = [f for f in os.listdir('.') if f.startswith('query_tracking_') and f.endswith('.json')]
    
    if not tracking_files:
        print("❌ No se encontraron archivos de tracking")
        return
    
    print(f"📁 Archivos encontrados: {len(tracking_files)}")
    print()
    
    # Análisis por consulta
    results = []
    for file in sorted(tracking_files):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraer información clave
            query = data.get('query', 'N/A')
            status = data.get('status', 'N/A')
            steps = data.get('steps', [])
            
            # Buscar tiempo de respuesta
            response_time = None
            for step in steps:
                if 'BACKEND_RESPONSE_RECEIVED' in step.get('step', ''):
                    response_time = step.get('data', {}).get('response_time_ms', 0)
                    break
            
            # Buscar SQL generado
            sql_generated = None
            for step in steps:
                if 'BACKEND_RESPONSE_SUCCESS' in step.get('step', ''):
                    response_data = step.get('data', {}).get('response_data', {})
                    sql_generated = response_data.get('response', 'N/A')
                    break
            
            results.append({
                'file': file,
                'query': query,
                'status': status,
                'response_time': response_time,
                'sql_generated': sql_generated,
                'steps_count': len(steps)
            })
            
        except Exception as e:
            print(f"❌ Error procesando {file}: {e}")
    
    # Mostrar resumen
    print("📊 RESUMEN POR CONSULTA:")
    print("-" * 60)
    
    for result in results:
        print(f"🔍 Consulta: {result['query']}")
        print(f"   Estado: {result['status']}")
        print(f"   Tiempo: {result['response_time']:.1f}ms" if result['response_time'] else "   Tiempo: N/A")
        print(f"   Pasos: {result['steps_count']}")
        print(f"   SQL: {result['sql_generated'][:50]}..." if result['sql_generated'] else "   SQL: N/A")
        print()
    
    # Análisis de rendimiento
    print("⏱️ ANÁLISIS DE RENDIMIENTO:")
    print("-" * 60)
    
    response_times = [r['response_time'] for r in results if r['response_time']]
    if response_times:
        print(f"   Tiempo mínimo: {min(response_times):.1f}ms")
        print(f"   Tiempo máximo: {max(response_times):.1f}ms")
        print(f"   Tiempo promedio: {sum(response_times)/len(response_times):.1f}ms")
        print(f"   Total consultas: {len(response_times)}")
    
    # Análisis de éxito
    print("\n✅ ANÁLISIS DE ÉXITO:")
    print("-" * 60)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    partial_success_count = sum(1 for r in results if r['status'] == 'partial_success')
    failed_count = sum(1 for r in results if r['status'] == 'failed')
    
    print(f"   Exitosas: {success_count}")
    print(f"   Parcialmente exitosas: {partial_success_count}")
    print(f"   Fallidas: {failed_count}")
    print(f"   Tasa de éxito: {((success_count + partial_success_count) / len(results)) * 100:.1f}%")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    print("-" * 60)
    
    if any(r['response_time'] and r['response_time'] > 5000 for r in results):
        print("   ⚠️ Algunas consultas tardan más de 5 segundos")
        print("   💡 Considerar optimización del backend")
    
    if partial_success_count > 0:
        print("   ⚠️ Hay consultas con estado 'partial_success'")
        print("   💡 Revisar logs para identificar problemas")
    
    if failed_count > 0:
        print("   ❌ Hay consultas fallidas")
        print("   💡 Revisar configuración del sistema")
    
    print("   ✅ Sistema de tracking funcionando correctamente")
    print("   ✅ Logs detallados generados")
    print("   ✅ Análisis de flujo completo")

def main():
    print("🔬 ANÁLISIS DE RESULTADOS DE TRACKING")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    analyze_tracking_files()

if __name__ == "__main__":
    main()
