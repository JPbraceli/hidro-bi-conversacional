#!/usr/bin/env python3
"""
Script para analizar resultados de pruebas y generar reportes
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class TestAnalyzer:
    """Analizador de resultados de pruebas"""
    
    def __init__(self):
        self.results_file = "test_results.json"
        self.log_file = "test_logs.log"
    
    def load_results(self) -> Dict[str, Any]:
        """Cargar resultados de pruebas"""
        if not os.path.exists(self.results_file):
            return None
        
        with open(self.results_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def analyze_layer_performance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar rendimiento por capa"""
        layer_stats = {
            "database": {"total": 0, "success": 0, "errors": []},
            "backend": {"total": 0, "success": 0, "errors": []},
            "chat": {"total": 0, "success": 0, "errors": []},
            "sql_execution": {"total": 0, "success": 0, "errors": []}
        }
        
        for test_case in results.get("test_cases", []):
            for layer in test_case.get("layers", []):
                layer_name = layer.get("layer", "unknown")
                if layer_name in layer_stats:
                    layer_stats[layer_name]["total"] += 1
                    if layer["status"] == "success":
                        layer_stats[layer_name]["success"] += 1
                    else:
                        layer_stats[layer_name]["errors"].append({
                            "test": test_case.get("test_message", "unknown"),
                            "error": layer.get("details", {}).get("error", "unknown")
                        })
        
        # Calcular porcentajes
        for layer_name, stats in layer_stats.items():
            if stats["total"] > 0:
                stats["success_rate"] = (stats["success"] / stats["total"]) * 100
            else:
                stats["success_rate"] = 0
        
        return layer_stats
    
    def analyze_response_times(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar tiempos de respuesta"""
        response_times = {
            "chat_responses": [],
            "sql_executions": [],
            "overall": []
        }
        
        for test_case in results.get("test_cases", []):
            start_time = datetime.fromisoformat(test_case.get("start_time", ""))
            end_time = datetime.fromisoformat(test_case.get("end_time", ""))
            total_time = (end_time - start_time).total_seconds() * 1000
            
            response_times["overall"].append(total_time)
            
            for layer in test_case.get("layers", []):
                if layer.get("layer") == "Chat":
                    if "response_time_ms" in layer.get("details", {}):
                        response_times["chat_responses"].append(
                            layer["details"]["response_time_ms"]
                        )
                elif layer.get("layer") == "SQL Execution":
                    if "execution_time_ms" in layer.get("details", {}):
                        response_times["sql_executions"].append(
                            layer["details"]["execution_time_ms"]
                        )
        
        # Calcular estadísticas
        stats = {}
        for category, times in response_times.items():
            if times:
                stats[category] = {
                    "min": min(times),
                    "max": max(times),
                    "avg": sum(times) / len(times),
                    "count": len(times)
                }
            else:
                stats[category] = {"min": 0, "max": 0, "avg": 0, "count": 0}
        
        return stats
    
    def analyze_sql_queries(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar consultas SQL generadas"""
        sql_analysis = {
            "total_queries": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "query_types": {},
            "common_patterns": []
        }
        
        for test_case in results.get("test_cases", []):
            for layer in test_case.get("layers", []):
                if layer.get("layer") == "Chat":
                    details = layer.get("details", {})
                    if "generated_sql" in details:
                        sql_analysis["total_queries"] += 1
                        
                        sql_query = details["generated_sql"]
                        
                        # Analizar tipo de consulta
                        if "SELECT COUNT(*)" in sql_query:
                            query_type = "COUNT"
                        elif "SELECT SUM(" in sql_query:
                            query_type = "SUM"
                        elif "SELECT *" in sql_query:
                            query_type = "SELECT_ALL"
                        else:
                            query_type = "OTHER"
                        
                        if query_type not in sql_analysis["query_types"]:
                            sql_analysis["query_types"][query_type] = 0
                        sql_analysis["query_types"][query_type] += 1
                
                elif layer.get("layer") == "SQL Execution":
                    if layer.get("status") == "success":
                        sql_analysis["successful_executions"] += 1
                    else:
                        sql_analysis["failed_executions"] += 1
        
        return sql_analysis
    
    def generate_report(self) -> str:
        """Generar reporte completo"""
        results = self.load_results()
        if not results:
            return "❌ No se encontraron resultados de pruebas"
        
        report = []
        report.append("📊 REPORTE DE ANÁLISIS DE PRUEBAS HIDRO CHAT")
        report.append("=" * 60)
        report.append(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Resumen general
        summary = results.get("summary", {})
        report.append("📈 RESUMEN GENERAL:")
        report.append(f"   Total pruebas: {summary.get('total_tests', 0)}")
        report.append(f"   Exitosas: {summary.get('passed', 0)}")
        report.append(f"   Fallidas: {summary.get('failed', 0)}")
        report.append(f"   Tasa de éxito: {summary.get('success_rate', '0%')}")
        report.append("")
        
        # Análisis por capas
        layer_stats = self.analyze_layer_performance(results)
        report.append("🔧 ANÁLISIS POR CAPAS:")
        for layer_name, stats in layer_stats.items():
            report.append(f"   {layer_name.upper()}:")
            report.append(f"     Total: {stats['total']}")
            report.append(f"     Exitosas: {stats['success']}")
            report.append(f"     Tasa de éxito: {stats['success_rate']:.1f}%")
            if stats['errors']:
                report.append(f"     Errores: {len(stats['errors'])}")
        report.append("")
        
        # Análisis de tiempos
        time_stats = self.analyze_response_times(results)
        report.append("⏱️ ANÁLISIS DE TIEMPOS:")
        for category, stats in time_stats.items():
            if stats['count'] > 0:
                report.append(f"   {category.upper()}:")
                report.append(f"     Mínimo: {stats['min']:.2f}ms")
                report.append(f"     Máximo: {stats['max']:.2f}ms")
                report.append(f"     Promedio: {stats['avg']:.2f}ms")
                report.append(f"     Cantidad: {stats['count']}")
        report.append("")
        
        # Análisis de SQL
        sql_analysis = self.analyze_sql_queries(results)
        report.append("📊 ANÁLISIS DE CONSULTAS SQL:")
        report.append(f"   Total consultas: {sql_analysis['total_queries']}")
        report.append(f"   Ejecuciones exitosas: {sql_analysis['successful_executions']}")
        report.append(f"   Ejecuciones fallidas: {sql_analysis['failed_executions']}")
        report.append("   Tipos de consulta:")
        for query_type, count in sql_analysis['query_types'].items():
            report.append(f"     {query_type}: {count}")
        report.append("")
        
        # Recomendaciones
        report.append("💡 RECOMENDACIONES:")
        if summary.get('failed', 0) > 0:
            report.append("   - Revisar las pruebas fallidas")
            report.append("   - Verificar logs de error")
        
        if layer_stats['chat']['success_rate'] < 100:
            report.append("   - Revisar capa de chat")
        
        if layer_stats['sql_execution']['success_rate'] < 100:
            report.append("   - Revisar ejecución de SQL")
        
        if time_stats['overall']['avg'] > 5000:  # Más de 5 segundos
            report.append("   - Optimizar tiempos de respuesta")
        
        report.append("")
        report.append("📁 ARCHIVOS GENERADOS:")
        report.append("   - test_results.json: Resultados detallados")
        report.append("   - test_logs.log: Logs de ejecución")
        report.append("   - query_tracking_*.json: Tracking de consultas específicas")
        
        return "\n".join(report)
    
    def save_report(self, report: str):
        """Guardar reporte en archivo"""
        filename = f"test_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📁 Reporte guardado en: {filename}")

def main():
    """Función principal"""
    print("🔍 ANALIZANDO RESULTADOS DE PRUEBAS")
    print("=" * 50)
    
    analyzer = TestAnalyzer()
    report = analyzer.generate_report()
    
    print(report)
    analyzer.save_report(report)

if __name__ == "__main__":
    main()
