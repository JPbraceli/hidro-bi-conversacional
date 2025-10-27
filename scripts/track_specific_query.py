#!/usr/bin/env python3
"""
Script para trackear una consulta específica con logging detallado
"""
import sys
import os
import time
import json
import requests
import sqlite3
from datetime import datetime
import logging

# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('query_tracking.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QueryTracker:
    """Tracker para una consulta específica"""
    
    def __init__(self, query: str):
        self.query = query
        self.base_url = "http://localhost:8001"
        self.db_path = "hidro_data.db"
        self.tracking_data = {
            "query": query,
            "start_time": datetime.now().isoformat(),
            "steps": []
        }
    
    def log_step(self, step_name: str, data: dict = None):
        """Loggear un paso del proceso"""
        step = {
            "step": step_name,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        self.tracking_data["steps"].append(step)
        logger.info(f"STEP: {step_name}")
        if data:
            logger.debug(f"DATA: {json.dumps(data, indent=2)}")
    
    def track_database_state(self):
        """Trackear estado inicial de la base de datos"""
        self.log_step("DATABASE_STATE_INITIAL", {
            "db_path": self.db_path,
            "db_exists": os.path.exists(self.db_path)
        })
        
        if not os.path.exists(self.db_path):
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener información de tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Obtener conteos
            table_counts = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                table_counts[table] = count
            
            # Obtener datos específicos de actividades
            cursor.execute("SELECT COUNT(*) FROM activities")
            activities_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(amount) FROM activities")
            total_value = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM activities WHERE vigente = 1")
            active_activities = cursor.fetchone()[0]
            
            self.log_step("DATABASE_STATE_DETAILS", {
                "tables": tables,
                "table_counts": table_counts,
                "activities_count": activities_count,
                "total_value": total_value,
                "active_activities": active_activities
            })
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_step("DATABASE_ERROR", {"error": str(e)})
            return False
    
    def track_backend_request(self):
        """Trackear request al backend"""
        self.log_step("BACKEND_REQUEST_START", {
            "url": f"{self.base_url}/api/chat",
            "method": "POST"
        })
        
        try:
            # Preparar datos
            request_data = {
                "message": self.query,
                "conversation_history": []
            }
            
            self.log_step("BACKEND_REQUEST_DATA", {
                "request_payload": request_data
            })
            
            # Enviar request
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=request_data,
                timeout=15
            )
            end_time = time.time()
            
            self.log_step("BACKEND_RESPONSE_RECEIVED", {
                "status_code": response.status_code,
                "response_time_ms": (end_time - start_time) * 1000,
                "response_size_bytes": len(response.content)
            })
            
            if response.status_code == 200:
                response_data = response.json()
                self.log_step("BACKEND_RESPONSE_SUCCESS", {
                    "response_data": response_data
                })
                return response_data
            else:
                self.log_step("BACKEND_RESPONSE_ERROR", {
                    "status_code": response.status_code,
                    "response_text": response.text
                })
                return None
                
        except Exception as e:
            self.log_step("BACKEND_REQUEST_ERROR", {"error": str(e)})
            return None
    
    def track_sql_execution(self, sql_query: str):
        """Trackear ejecución de SQL"""
        self.log_step("SQL_EXECUTION_START", {
            "sql_query": sql_query
        })
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_time = time.time()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000
            
            self.log_step("SQL_EXECUTION_SUCCESS", {
                "execution_time_ms": execution_time,
                "row_count": len(rows),
                "results": rows
            })
            
            conn.close()
            return rows
            
        except Exception as e:
            self.log_step("SQL_EXECUTION_ERROR", {"error": str(e)})
            return None
    
    def track_expected_result(self):
        """Trackear resultado esperado basado en la consulta"""
        expected_results = {
            "¿Cuántas actividades hay?": {
                "expected_sql": "SELECT COUNT(*) FROM activities",
                "expected_result": 5,
                "description": "Debería retornar 5 actividades"
            },
            "¿Cuántas actividades están activas?": {
                "expected_sql": "SELECT COUNT(*) FROM activities WHERE vigente = 1",
                "expected_result": 5,
                "description": "Debería retornar 5 actividades activas"
            },
            "¿Cuál es el valor total de los contratos?": {
                "expected_sql": "SELECT SUM(value) FROM contracts",
                "expected_result": 15700000.0,
                "description": "Debería retornar $15,700,000"
            }
        }
        
        if self.query in expected_results:
            expected = expected_results[self.query]
            self.log_step("EXPECTED_RESULT", expected)
            return expected
        else:
            self.log_step("EXPECTED_RESULT", {
                "message": "No hay resultado esperado definido para esta consulta"
            })
            return None
    
    def track_complete_flow(self):
        """Trackear flujo completo"""
        self.log_step("FLOW_START", {"query": self.query})
        
        # 1. Estado inicial de la base de datos
        if not self.track_database_state():
            self.tracking_data["status"] = "failed"
            self.tracking_data["failure_point"] = "database_state"
            return self.tracking_data
        
        # 2. Resultado esperado
        expected = self.track_expected_result()
        
        # 3. Request al backend
        response_data = self.track_backend_request()
        if not response_data:
            self.tracking_data["status"] = "failed"
            self.tracking_data["failure_point"] = "backend_request"
            return self.tracking_data
        
        # 4. Si hay SQL generado, ejecutarlo
        if "sql_query" in response_data:
            sql_query = response_data["sql_query"]
            sql_results = self.track_sql_execution(sql_query)
            
            if sql_results is not None and expected:
                # Verificar resultado
                if len(sql_results) > 0 and len(sql_results[0]) > 0:
                    actual_result = sql_results[0][0]
                    expected_result = expected["expected_result"]
                    
                    self.log_step("RESULT_VERIFICATION", {
                        "expected": expected_result,
                        "actual": actual_result,
                        "match": actual_result == expected_result
                    })
                    
                    if actual_result == expected_result:
                        self.tracking_data["status"] = "success"
                        self.tracking_data["verification"] = "passed"
                    else:
                        self.tracking_data["status"] = "partial_success"
                        self.tracking_data["verification"] = "failed"
                        self.tracking_data["verification_details"] = {
                            "expected": expected_result,
                            "actual": actual_result
                        }
                else:
                    self.tracking_data["status"] = "partial_success"
                    self.tracking_data["verification"] = "no_results"
            else:
                self.tracking_data["status"] = "partial_success"
                self.tracking_data["verification"] = "sql_execution_failed"
        else:
            self.tracking_data["status"] = "partial_success"
            self.tracking_data["verification"] = "no_sql_generated"
        
        self.tracking_data["end_time"] = datetime.now().isoformat()
        return self.tracking_data
    
    def save_tracking_data(self):
        """Guardar datos de tracking"""
        filename = f"query_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.tracking_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Tracking data saved to: {filename}")
        return filename

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python track_specific_query.py '<consulta>'")
        print("Ejemplo: python track_specific_query.py '¿Cuántas actividades hay?'")
        return
    
    query = sys.argv[1]
    
    print(f"🔍 TRACKING QUERY: '{query}'")
    print("=" * 60)
    print("📝 Logs: query_tracking.log")
    print("=" * 60)
    
    # Crear tracker
    tracker = QueryTracker(query)
    
    # Ejecutar tracking completo
    result = tracker.track_complete_flow()
    
    # Guardar datos
    filename = tracker.save_tracking_data()
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DEL TRACKING:")
    print(f"   Estado: {result['status']}")
    print(f"   Pasos: {len(result['steps'])}")
    print(f"   Archivo: {filename}")
    
    if result['status'] == 'success':
        print(f"   ✅ ¡Consulta procesada correctamente!")
    elif result['status'] == 'partial_success':
        print(f"   ⚠️ Consulta procesada con advertencias")
    else:
        print(f"   ❌ Error en: {result.get('failure_point', 'unknown')}")

if __name__ == "__main__":
    main()
