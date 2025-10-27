"""
Explorador automático de datos para el agente HIDRO
Analiza la BD y sugiere análisis inteligentes
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

class DataExplorer:
    """Explorador inteligente de datos que analiza la BD y sugiere análisis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.analysis_cache = {}
        
    def explore_database(self) -> Dict[str, Any]:
        """
        Explora la BD completa y genera insights automáticos
        """
        try:
            # Obtener información de todas las tablas
            tables_info = self._get_tables_info()
            
            # Analizar relaciones entre tablas
            relationships = self._analyze_relationships()
            
            # Detectar patrones y anomalías
            patterns = self._detect_patterns()
            
            # Generar sugerencias de análisis
            suggestions = self._generate_analysis_suggestions(tables_info, patterns)
            
            return {
                "tables_info": tables_info,
                "relationships": relationships,
                "patterns": patterns,
                "suggestions": suggestions,
                "summary": self._generate_summary(tables_info, patterns)
            }
            
        except Exception as e:
            return {"error": f"Error explorando BD: {str(e)}"}
    
    def _get_tables_info(self) -> Dict[str, Any]:
        """Obtener información detallada de todas las tablas"""
        tables_info = {}
        
        # Lista de tablas principales
        main_tables = ['activities', 'contracts', 'profiles', 'gateways', 'admin_users']
        
        for table in main_tables:
            try:
                # Obtener conteo de registros
                count_result = self.db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = count_result.fetchone()[0]
                
                if count > 0:
                    # Obtener columnas y tipos
                    columns_result = self.db.execute(text(f"PRAGMA table_info({table})"))
                    columns = columns_result.fetchall()
                    
                    # Obtener muestra de datos
                    sample_result = self.db.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                    sample_data = sample_result.fetchall()
                    
                    # Analizar valores únicos en columnas clave
                    unique_analysis = self._analyze_unique_values(table, columns)
                    
                    tables_info[table] = {
                        "count": count,
                        "columns": [{"name": col[1], "type": col[2]} for col in columns],
                        "sample_data": [dict(zip([col[1] for col in columns], row)) for row in sample_data],
                        "unique_analysis": unique_analysis
                    }
                    
            except Exception as e:
                tables_info[table] = {"error": str(e)}
        
        return tables_info
    
    def _analyze_unique_values(self, table: str, columns: List) -> Dict[str, Any]:
        """Analizar valores únicos en columnas importantes"""
        analysis = {}
        
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            
            # Solo analizar columnas de texto o enteros
            if col_type in ['TEXT', 'INTEGER']:
                try:
                    # Obtener valores únicos
                    unique_result = self.db.execute(text(f"SELECT DISTINCT {col_name} FROM {table} WHERE {col_name} IS NOT NULL LIMIT 10"))
                    unique_values = [row[0] for row in unique_result.fetchall()]
                    
                    if unique_values:
                        analysis[col_name] = {
                            "unique_count": len(unique_values),
                            "sample_values": unique_values[:5],
                            "type": col_type
                        }
                except:
                    pass
        
        return analysis
    
    def _analyze_relationships(self) -> Dict[str, Any]:
        """Analizar relaciones entre tablas"""
        relationships = {}
        
        try:
            # Verificar relación activities -> contracts
            if self._table_exists('activities') and self._table_exists('contracts'):
                rel_result = self.db.execute(text("""
                    SELECT COUNT(*) as total_activities,
                           COUNT(DISTINCT id_contract) as unique_contracts
                    FROM activities 
                    WHERE id_contract IS NOT NULL
                """))
                rel_data = rel_result.fetchone()
                
                if rel_data and rel_data[0] > 0:
                    relationships['activities_contracts'] = {
                        "type": "foreign_key",
                        "description": "Actividades vinculadas a contratos",
                        "total_activities": rel_data[0],
                        "unique_contracts": rel_data[1],
                        "coverage": f"{(rel_data[1]/rel_data[0]*100):.1f}%"
                    }
        except:
            pass
        
        return relationships
    
    def _detect_patterns(self) -> Dict[str, Any]:
        """Detectar patrones y anomalías en los datos"""
        patterns = {}
        
        try:
            # Patrón temporal en activities
            if self._table_exists('activities'):
                temporal_result = self.db.execute(text("""
                    SELECT anio_campania, COUNT(*) as count
                    FROM activities 
                    WHERE anio_campania IS NOT NULL
                    GROUP BY anio_campania
                    ORDER BY anio_campania
                """))
                temporal_data = temporal_result.fetchall()
                
                if temporal_data:
                    years = [row[0] for row in temporal_data]
                    counts = [row[1] for row in temporal_data]
                    
                    patterns['temporal_activities'] = {
                        "years": years,
                        "counts": counts,
                        "trend": "increasing" if len(years) > 1 and counts[-1] > counts[0] else "stable",
                        "peak_year": years[counts.index(max(counts))] if counts else None
                    }
            
            # Patrón de valores en contracts
            if self._table_exists('contracts'):
                value_result = self.db.execute(text("""
                    SELECT company, COUNT(*) as contract_count, 
                           AVG(value) as avg_value, SUM(value) as total_value
                    FROM contracts 
                    WHERE value IS NOT NULL
                    GROUP BY company
                    ORDER BY total_value DESC
                """))
                value_data = value_result.fetchall()
                
                if value_data:
                    patterns['contract_values'] = {
                        "companies": [row[0] for row in value_data],
                        "contract_counts": [row[1] for row in value_data],
                        "avg_values": [row[2] for row in value_data],
                        "total_values": [row[3] for row in value_data],
                        "top_company": value_data[0][0] if value_data else None
                    }
                    
        except Exception as e:
            patterns['error'] = str(e)
        
        return patterns
    
    def _generate_analysis_suggestions(self, tables_info: Dict, patterns: Dict) -> List[str]:
        """Generar sugerencias inteligentes de análisis basadas en los datos"""
        suggestions = []
        
        # Sugerencias basadas en datos disponibles
        if 'activities' in tables_info and tables_info['activities'].get('count', 0) > 0:
            suggestions.extend([
                "Análisis de tendencias temporales de actividades",
                "Distribución de actividades por estado (activas/inactivas)",
                "Valor total de actividades por año"
            ])
        
        if 'contracts' in tables_info and tables_info['contracts'].get('count', 0) > 0:
            suggestions.extend([
                "Ranking de empresas por valor de contratos",
                "Análisis de contratos por período",
                "Comparación de valores promedio por empresa"
            ])
        
        if 'profiles' in tables_info and tables_info['profiles'].get('count', 0) > 0:
            suggestions.extend([
                "Distribución de usuarios por rol",
                "Análisis de perfiles de usuario",
                "Usuarios más activos"
            ])
        
        # Sugerencias basadas en patrones detectados
        if 'temporal_activities' in patterns:
            suggestions.append("Evolución histórica de actividades")
        
        if 'contract_values' in patterns:
            suggestions.append("Análisis de rentabilidad por empresa")
        
        # Sugerencias cruzadas
        if 'activities' in tables_info and 'contracts' in tables_info:
            suggestions.extend([
                "Correlación entre actividades y contratos",
                "Análisis de rendimiento por contrato",
                "Dashboard ejecutivo completo"
            ])
        
        return suggestions[:8]  # Máximo 8 sugerencias
    
    def _generate_summary(self, tables_info: Dict, patterns: Dict) -> str:
        """Generar resumen ejecutivo de los datos"""
        total_records = sum(info.get('count', 0) for info in tables_info.values() if isinstance(info, dict))
        active_tables = len([t for t in tables_info.values() if isinstance(t, dict) and t.get('count', 0) > 0])
        
        summary = f"Base de datos HIDRO: {active_tables} tablas activas con {total_records} registros totales. "
        
        if 'temporal_activities' in patterns:
            summary += f"Actividades distribuidas en {len(patterns['temporal_activities']['years'])} años. "
        
        if 'contract_values' in patterns:
            summary += f"Contratos con {len(patterns['contract_values']['companies'])} empresas diferentes. "
        
        summary += "Datos listos para análisis multivisual y business intelligence."
        
        return summary
    
    def _table_exists(self, table_name: str) -> bool:
        """Verificar si una tabla existe"""
        try:
            result = self.db.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"))
            return result.fetchone() is not None
        except:
            return False
    
    def get_smart_suggestions(self, user_message: str) -> List[str]:
        """Generar sugerencias inteligentes basadas en el mensaje del usuario"""
        suggestions = []
        message_lower = user_message.lower()
        
        # Explorar BD si no está en caché
        if not self.analysis_cache:
            self.analysis_cache = self.explore_database()
        
        # Sugerencias basadas en el contexto del mensaje
        if any(word in message_lower for word in ['actividad', 'actividades']):
            suggestions.extend([
                "Muéstrame la evolución de actividades por año",
                "¿Cuáles son las actividades más costosas?",
                "Análisis de actividades activas vs inactivas"
            ])
        
        if any(word in message_lower for word in ['contrato', 'contratos', 'empresa', 'empresas']):
            suggestions.extend([
                "Ranking de empresas por valor de contratos",
                "Análisis de contratos por período",
                "Comparación de rendimiento por empresa"
            ])
        
        if any(word in message_lower for word in ['usuario', 'usuarios', 'perfil', 'perfiles']):
            suggestions.extend([
                "Distribución de usuarios por rol",
                "Análisis de perfiles de usuario",
                "Usuarios más activos del sistema"
            ])
        
        # Sugerencias avanzadas basadas en datos disponibles
        if self.analysis_cache.get('patterns', {}).get('temporal_activities'):
            suggestions.append("Dashboard de tendencias temporales")
        
        if self.analysis_cache.get('patterns', {}).get('contract_values'):
            suggestions.append("Análisis de rentabilidad empresarial")
        
        return suggestions[:5]  # Máximo 5 sugerencias
