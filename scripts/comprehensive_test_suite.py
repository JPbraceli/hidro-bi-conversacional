#!/usr/bin/env python3
"""
Suite completa de pruebas y logging para HIDRO Chat
Trackea todo el flujo desde entrada hasta respuesta
"""
import sys
import os
import time
import json
import requests
import sqlite3
from datetime import datetime
from typing import Dict, List, Any
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HIDROTestSuite:
    """Suite completa de pruebas para HIDRO Chat"""
    
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.db_path = "hidro_data.db"
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_step(self, step: str, details: str = ""):
        """Loggear un paso del proceso"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        logger.info(f"[{timestamp}] {step}")
        if details:
            logger.info(f"    {details}")
    
    def test_database_layer(self) -> Dict[str, Any]:
        """Probar capa de base de datos"""
        self.log_step("🔍 TESTING DATABASE LAYER", "Verificando conexión SQLite")
        
        result = {
            "layer": "Database",
            "status": "unknown",
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Verificar archivo de base de datos
            if not os.path.exists(self.db_path):
                result["status"] = "error"
                result["details"]["error"] = f"Database file not found: {self.db_path}"
                return result
            
            # Conectar a SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
            tables = [row[0] for row in cursor.fetchall()]
            result["details"]["tables"] = tables
            
            # Verificar datos
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                result["details"][f"{table}_count"] = count
            
            # Probar consulta específica
            cursor.execute("SELECT COUNT(*) FROM activities")
            activities = cursor.fetchone()[0]
            result["details"]["activities_count"] = activities
            
            cursor.execute("SELECT SUM(amount) FROM activities")
            total_value = cursor.fetchone()[0]
            result["details"]["total_activities_value"] = total_value
            
            conn.close()
            
            result["status"] = "success"
            result["details"]["message"] = "Database layer working correctly"
            
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
        
        return result
    
    def test_backend_layer(self) -> Dict[str, Any]:
        """Probar capa de backend"""
        self.log_step("🔧 TESTING BACKEND LAYER", "Verificando API endpoints")
        
        result = {
            "layer": "Backend",
            "status": "unknown",
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Probar conexión al servidor
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code != 200:
                result["status"] = "error"
                result["details"]["error"] = f"Server not responding: {response.status_code}"
                return result
            
            # Probar endpoints disponibles
            response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
            if response.status_code == 200:
                api_spec = response.json()
                endpoints = list(api_spec.get("paths", {}).keys())
                result["details"]["endpoints"] = endpoints
            
            # Probar endpoint de sugerencias
            response = requests.get(f"{self.base_url}/api/suggestions", timeout=5)
            if response.status_code == 200:
                suggestions = response.json()
                result["details"]["suggestions"] = suggestions.get("suggestions", [])
            else:
                result["details"]["suggestions_error"] = f"Status: {response.status_code}"
            
            result["status"] = "success"
            result["details"]["message"] = "Backend layer working correctly"
            
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
        
        return result
    
    def test_chat_layer(self, test_message: str) -> Dict[str, Any]:
        """Probar capa de chat con mensaje específico"""
        self.log_step("🤖 TESTING CHAT LAYER", f"Mensaje: '{test_message}'")
        
        result = {
            "layer": "Chat",
            "status": "unknown",
            "details": {},
            "timestamp": datetime.now().isoformat(),
            "input": test_message
        }
        
        try:
            # Preparar datos de entrada
            chat_data = {
                "message": test_message,
                "conversation_history": []
            }
            
            result["details"]["input_data"] = chat_data
            
            # Enviar consulta al chat
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=chat_data,
                timeout=15
            )
            
            result["details"]["http_status"] = response.status_code
            result["details"]["response_time_ms"] = response.elapsed.total_seconds() * 1000
            
            if response.status_code == 200:
                chat_response = response.json()
                result["details"]["output"] = chat_response
                
                # Analizar respuesta
                if "response" in chat_response:
                    result["details"]["ai_response"] = chat_response["response"]
                
                if "sql_query" in chat_response:
                    result["details"]["generated_sql"] = chat_response["sql_query"]
                
                if "visualization_type" in chat_response:
                    result["details"]["visualization"] = chat_response["visualization_type"]
                
                result["status"] = "success"
                result["details"]["message"] = "Chat layer working correctly"
            else:
                result["status"] = "error"
                result["details"]["error"] = f"HTTP {response.status_code}: {response.text}"
        
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
        
        return result
    
    def test_sql_execution(self, sql_query: str) -> Dict[str, Any]:
        """Probar ejecución de SQL"""
        self.log_step("📊 TESTING SQL EXECUTION", f"Query: {sql_query}")
        
        result = {
            "layer": "SQL Execution",
            "status": "unknown",
            "details": {},
            "timestamp": datetime.now().isoformat(),
            "sql_query": sql_query
        }
        
        try:
            # Ejecutar SQL directamente
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_time = time.time()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            execution_time = (time.time() - start_time) * 1000
            
            result["details"]["execution_time_ms"] = execution_time
            result["details"]["row_count"] = len(rows)
            result["details"]["results"] = rows
            
            conn.close()
            
            result["status"] = "success"
            result["details"]["message"] = "SQL executed successfully"
            
        except Exception as e:
            result["status"] = "error"
            result["details"]["error"] = str(e)
        
        return result
    
    def test_complete_flow(self, test_message: str) -> Dict[str, Any]:
        """Probar flujo completo desde entrada hasta respuesta"""
        self.log_step("🔄 TESTING COMPLETE FLOW", f"Iniciando prueba completa con: '{test_message}'")
        
        flow_result = {
            "test_message": test_message,
            "start_time": datetime.now().isoformat(),
            "layers": [],
            "overall_status": "unknown"
        }
        
        # 1. Probar capa de base de datos
        db_result = self.test_database_layer()
        flow_result["layers"].append(db_result)
        
        if db_result["status"] != "success":
            flow_result["overall_status"] = "failed"
            flow_result["failure_point"] = "database"
            return flow_result
        
        # 2. Probar capa de backend
        backend_result = self.test_backend_layer()
        flow_result["layers"].append(backend_result)
        
        if backend_result["status"] != "success":
            flow_result["overall_status"] = "failed"
            flow_result["failure_point"] = "backend"
            return flow_result
        
        # 3. Probar capa de chat
        chat_result = self.test_chat_layer(test_message)
        flow_result["layers"].append(chat_result)
        
        if chat_result["status"] != "success":
            flow_result["overall_status"] = "failed"
            flow_result["failure_point"] = "chat"
            return flow_result
        
        # 4. Si hay SQL generado, probarlo
        if "generated_sql" in chat_result["details"]:
            sql_query = chat_result["details"]["generated_sql"]
            sql_result = self.test_sql_execution(sql_query)
            flow_result["layers"].append(sql_result)
            
            if sql_result["status"] != "success":
                flow_result["overall_status"] = "failed"
                flow_result["failure_point"] = "sql_execution"
                return flow_result
        
        flow_result["overall_status"] = "success"
        flow_result["end_time"] = datetime.now().isoformat()
        
        return flow_result
    
    def run_test_suite(self):
        """Ejecutar suite completa de pruebas"""
        self.log_step("🚀 STARTING COMPREHENSIVE TEST SUITE", "Iniciando pruebas completas")
        
        # Lista de pruebas
        test_cases = [
            "¿Cuántas actividades hay?",
            "¿Cuántas actividades están activas?",
            "¿Cuál es el valor total de los contratos?",
            "¿Cuántos usuarios hay por rol?",
            "Muéstrame los gateways activos"
        ]
        
        suite_results = {
            "start_time": self.start_time.isoformat(),
            "test_cases": [],
            "summary": {}
        }
        
        for i, test_message in enumerate(test_cases, 1):
            self.log_step(f"🧪 TEST CASE {i}/{len(test_cases)}", f"Probando: '{test_message}'")
            
            flow_result = self.test_complete_flow(test_message)
            suite_results["test_cases"].append(flow_result)
            
            # Loggear resultado
            status = flow_result["overall_status"]
            if status == "success":
                self.log_step(f"✅ TEST {i} PASSED", f"Mensaje: '{test_message}'")
            else:
                self.log_step(f"❌ TEST {i} FAILED", f"Error en: {flow_result.get('failure_point', 'unknown')}")
        
        # Generar resumen
        total_tests = len(test_cases)
        passed_tests = sum(1 for test in suite_results["test_cases"] if test["overall_status"] == "success")
        failed_tests = total_tests - passed_tests
        
        suite_results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
        }
        
        # Guardar resultados
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(suite_results, f, indent=2, ensure_ascii=False)
        
        # Loggear resumen
        self.log_step("📊 TEST SUITE SUMMARY", f"Total: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}")
        self.log_step("📁 RESULTS SAVED", "test_results.json y test_logs.log")
        
        return suite_results

def main():
    """Función principal"""
    print("🔬 HIDRO CHAT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("📝 Logs: test_logs.log")
    print("📊 Results: test_results.json")
    print("=" * 60)
    
    # Crear suite de pruebas
    test_suite = HIDROTestSuite()
    
    # Ejecutar pruebas
    results = test_suite.run_test_suite()
    
    # Mostrar resumen final
    summary = results["summary"]
    print(f"\n🎯 RESUMEN FINAL:")
    print(f"   Total pruebas: {summary['total_tests']}")
    print(f"   Exitosas: {summary['passed']}")
    print(f"   Fallidas: {summary['failed']}")
    print(f"   Tasa de éxito: {summary['success_rate']}")
    
    if summary['failed'] == 0:
        print(f"\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print(f"\n⚠️ {summary['failed']} pruebas fallaron. Revisa los logs.")

if __name__ == "__main__":
    main()
