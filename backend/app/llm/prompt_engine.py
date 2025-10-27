"""
Motor de prompts para integración con Ollama
"""
import ollama
import uuid
from typing import Dict, List, Optional, Any
from app.dependencies import get_settings
from app.db.schema import get_database_schema
from app.llm.data_explorer import DataExplorer

class PromptEngine:
    """Motor para generar prompts y manejar conversaciones con LLM"""
    
    def __init__(self):
        self.settings = get_settings()
        self.conversations: Dict[str, List[Dict]] = {}
        self.pending_queries: Dict[str, str] = {}
        self.data_explorer = None
        
    async def generate_response(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        db = None
    ) -> Dict[str, Any]:
        """
        Generar respuesta del LLM basada en el mensaje del usuario
        """
        # Crear o obtener conversación
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            
        # Agregar mensaje del usuario
        self.conversations[conversation_id].append({
            "role": "user",
            "content": message
        })
        
        # Inicializar DataExplorer si no existe
        if not self.data_explorer and db:
            self.data_explorer = DataExplorer(db)
        
        # Construir prompt con contexto enriquecido
        system_prompt = self._build_enhanced_system_prompt(db, message)
        conversation_history = self._format_conversation_history(conversation_id)
        
        # Generar respuesta con Ollama
        try:
            response = ollama.chat(
                model=self.settings.ollama_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history
                ]
            )
            
            assistant_message = response['message']['content']
            
            # Agregar respuesta del asistente
            self.conversations[conversation_id].append({
                "role": "assistant", 
                "content": assistant_message
            })
            
            # Analizar si la respuesta contiene una consulta SQL
            sql_query = self._extract_sql_query(assistant_message)
            is_ready = sql_query is not None
            
            if sql_query:
                self.pending_queries[conversation_id] = sql_query
                # Ejecutar automáticamente la consulta
                try:
                    from app.utils.query_executor import execute_query
                    from app.dependencies import get_db
                    
                    # Obtener sesión de BD
                    db_gen = get_db()
                    db = next(db_gen)
                    
                    # Ejecutar consulta
                    result = execute_query(sql_query, db)
                    
                    # Limpiar la respuesta del LLM para quitar la consulta SQL
                    assistant_message = self._clean_response(assistant_message)
                    
                    # Agregar resultados a la respuesta
                    assistant_message += f"\n\n**Resultados:**\n"
                    if result.get("visualization_type") == "table":
                        assistant_message += f"Se encontraron {result.get('row_count', 0)} registros.\n"
                    else:
                        assistant_message += f"Datos procesados: {result.get('row_count', 0)} registros.\n"
                    
                    # Marcar como lista para mostrar visualización
                    is_ready = True
                    
                except Exception as e:
                    assistant_message += f"\n\n**Error ejecutando consulta:** {str(e)}"
                
            # Generar sugerencias inteligentes
            smart_suggestions = []
            if self.data_explorer:
                smart_suggestions = self.data_explorer.get_smart_suggestions(message)
            
            # Combinar con sugerencias básicas
            basic_suggestions = self._generate_suggestions(message)
            all_suggestions = smart_suggestions[:3] + basic_suggestions[:2]  # 3 inteligentes + 2 básicas
            
            return {
                "text": assistant_message,
                "suggestions": all_suggestions,
                "is_ready": is_ready,
                "query_summary": self._generate_query_summary(sql_query) if sql_query else None,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            return {
                "text": f"Lo siento, hubo un error procesando tu consulta: {str(e)}",
                "suggestions": [],
                "is_ready": False,
                "query_summary": None,
                "conversation_id": conversation_id
            }
    
    def _build_enhanced_system_prompt(self, db, user_message: str) -> str:
        """Construir prompt del sistema con análisis inteligente de datos"""
        # Obtener análisis de datos si el explorador está disponible
        data_insights = ""
        if self.data_explorer:
            try:
                analysis = self.data_explorer.explore_database()
                if 'summary' in analysis:
                    data_insights = f"\n\nANÁLISIS INTELIGENTE DE DATOS:\n{analysis['summary']}"
                
                if 'suggestions' in analysis and analysis['suggestions']:
                    data_insights += f"\n\nANÁLISIS SUGERIDOS DISPONIBLES:\n"
                    for i, suggestion in enumerate(analysis['suggestions'][:5], 1):
                        data_insights += f"{i}. {suggestion}\n"
            except Exception as e:
                data_insights = f"\n\nError en análisis de datos: {str(e)}"
        
        # Construir prompt base
        base_prompt = self._build_system_prompt(db)
        
        # Agregar insights inteligentes
        enhanced_prompt = base_prompt + data_insights
        
        return enhanced_prompt
    
    def _build_system_prompt(self, db) -> str:
        """Construir prompt del sistema con esquema de BD"""
        schema = get_database_schema(db) if db else "Esquema de base de datos no disponible"
        
        # Obtener conteos reales de las tablas principales
        table_counts = ""
        if db:
            try:
                from sqlalchemy import text
                tables = ['activities', 'contracts', 'profiles', 'gateways', 'admin_users']
                for table in tables:
                    try:
                        result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        table_counts += f"- {table} ({count} registros)\n"
                    except:
                        table_counts += f"- {table} (tabla no disponible)\n"
            except:
                table_counts = "- activities (5 registros)\n- contracts (3 registros)\n- profiles (5 registros)\n- gateways (5 registros)\n- admin_users (3 registros)\n"
        
        return f"""
Eres un asistente amigable para el sistema HIDRO.
Responde de forma natural, como si fueras un colega que conoce los datos.

DATOS DISPONIBLES:
{table_counts}

TABLAS Y COLUMNAS REALES:
- activities: id, name, start_date, end_date, amount, vigente, anio_campania, code, id_contract
- contracts: id, contract_number, company, start_date, end_date, value, status
- profiles: id, user_id, first_name, last_name, email, role
- gateways: id, name, location, status
- admin_users: id, username, email, role

INSTRUCCIONES:
1. Responde de forma natural y conversacional
2. SOLO usa las tablas y columnas que existen realmente
3. Si el usuario pregunta por datos que no existen, adapta la pregunta a datos similares disponibles
4. Genera consultas SQL simples y correctas
5. Responde directamente sin explicaciones técnicas

FORMATO DE RESPUESTA:
- Saluda de forma natural
- Responde la pregunta directamente
- Genera la consulta SQL correcta
- NO muestres la consulta SQL al usuario

EJEMPLOS:
Usuario: "¿Cuántas actividades hay?"
Tú: "¡Hola! Hay 50 actividades en total en el sistema." + SQL: SELECT COUNT(*) FROM activities;

Usuario: "Muéstrame las actividades por año"
Tú: "Te muestro las actividades organizadas por año:" + SQL: SELECT anio_campania, COUNT(*) FROM activities GROUP BY anio_campania ORDER BY anio_campania;

Usuario: "Pozos por operadoras" o "lista las operadoras" o "empresas contratistas"
Tú: "Te muestro las empresas contratistas (operadoras) del sistema:" + SQL: SELECT company, COUNT(*) as contratos, SUM(value) as valor_total FROM contracts GROUP BY company ORDER BY valor_total DESC;

Usuario: "¿Cuáles son las empresas más importantes?"
Tú: "Te muestro las empresas ordenadas por valor total de contratos:" + SQL: SELECT company, COUNT(*) as contratos, SUM(value) as valor_total FROM contracts GROUP BY company ORDER BY valor_total DESC;

Usuario: "operadores del sistema"
Tú: "Te muestro los operadores/empresas del sistema:" + SQL: SELECT DISTINCT company FROM contracts ORDER BY company;

Usuario: "¿Cuál es la proporción de actividades activas vs inactivas? gráfico de pastel"
Tú: "Te muestro la proporción de actividades activas vs inactivas:" + SQL: SELECT vigente, COUNT(*) as total FROM activities GROUP BY vigente;

Usuario: "Muéstrame las tendencias de actividades por año"
Tú: "Te muestro las tendencias temporales de actividades:" + SQL: SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania;

Usuario: "Muéstrame la evolución de actividades por año"
Tú: "Te muestro la evolución temporal de actividades:" + SQL: SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania;

Usuario: "tendencias de actividades por año"
Tú: "Te muestro las tendencias temporales:" + SQL: SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania;

Usuario: "Muéstrame los KPIs principales"
Tú: "Te muestro los indicadores clave del sistema:" + SQL: SELECT COUNT(*) as total_actividades, SUM(amount) as valor_total FROM activities;

SINÓNIMOS IMPORTANTES:
- "operadoras" = "empresas" = "contratistas" = "operadores" = "companies"
- "pozos" = "actividades" = "proyectos" = "trabajos"
- "usuarios" = "perfiles" = "personal" = "empleados"
- "gateways" = "puntos de acceso" = "nodos" = "estaciones"

TIPOS DE VISUALIZACIÓN DISPONIBLES:
- "gráfico de barras" o "barras" = bar_chart (comparaciones por categoría)
- "gráfico de pastel" o "pastel" = pie_chart (proporciones y distribuciones)
- "gráfico de líneas" o "líneas" = line_chart (tendencias temporales)
- "KPIs" o "tarjetas" = kpi_cards (métricas clave)
- "mapa de calor" o "heatmap" = heatmap (correlaciones)
- "dispersión" o "scatter" = scatter_chart (relaciones entre variables)
- "radar" = radar_chart (comparaciones multidimensionales)
- "área" = area_chart (series temporales múltiples)

IMPORTANTE:
- Responde de forma natural y amigable
- SOLO usa tablas que existen: activities, contracts, profiles, gateways, admin_users
- SOLO usa columnas que existen: vigente, anio_campania, start_date, end_date, company, etc.
- Si el usuario pregunta por datos que no existen, adapta a datos similares disponibles
- Genera consultas SQL simples y correctas
- NO muestres la consulta SQL al usuario
- Sé conciso y directo
- SIEMPRE incluye estadísticas útiles (conteos, sumas, promedios) cuando sea relevante

COLUMNAS EXACTAS DISPONIBLES:
- activities: id, name, start_date, end_date, amount, vigente, anio_campania, code, id_contract, created_at
- contracts: id, contract_number, company, start_date, end_date, value, status, created_at
- profiles: id, user_id, first_name, last_name, email, role, created_at
- gateways: id, name, location, status, created_at
- admin_users: id, username, email, role, created_at

REGLAS SQL CRÍTICAS - OBLIGATORIAS:
- SOLO genera SQL puro, NUNCA incluyas datos JSON o texto extraño
- SOLO usa nombres de columnas EXACTOS de la lista arriba
- NUNCA inventes nombres de columnas
- ORDER BY debe ser: ORDER BY anio_campania (NO anio09-12 ni nada extraño)
- GROUP BY debe ser: GROUP BY anio_campania (NO nada más)
- SQL debe ser SIMPLE y LIMPIO
- EJEMPLO CORRECTO: SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania;
- EJEMPLO INCORRECTO: SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio09-12

VALIDACIÓN OBLIGATORIA:
- El SQL debe terminar con punto y coma (;)
- NO incluyas datos JSON, arrays, o texto extraño
- NO incluyas datetime, dict, o estructuras de datos
- SOLO SQL puro y simple
- Si no estás seguro, usa: SELECT anio_campania, COUNT(*) as total FROM activities GROUP BY anio_campania ORDER BY anio_campania;
"""
    
    def _format_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Formatear historial de conversación para el LLM"""
        history = self.conversations.get(conversation_id, [])
        # Limitar historial a los últimos 10 mensajes para evitar tokens excesivos
        return history[-10:]
    
    def _clean_response(self, text: str) -> str:
        """Limpiar respuesta del LLM quitando consultas SQL y contenido técnico"""
        import re
        
        # Quitar bloques de código SQL
        text = re.sub(r'```sql\s*.*?\s*```', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Quitar SELECT statements directos
        text = re.sub(r'SELECT\s+.*?;', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Quitar explicaciones técnicas sobre SQL
        text = re.sub(r'Consulta SQL.*?\.', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'SQL Query.*?\.', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Quitar referencias a Business Intelligence
        text = re.sub(r'Como asistente de Business Intelligence.*?\.', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Limpiar espacios extra y saltos de línea
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def _extract_sql_query(self, text: str) -> Optional[str]:
        """Extraer consulta SQL del texto de respuesta"""
        import re
        
        # Buscar bloques de código SQL
        sql_pattern = r'```sql\s*(.*?)\s*```'
        matches = re.findall(sql_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if matches:
            return matches[0].strip()
            
        # Buscar SELECT statements directos (mejorado)
        select_pattern = r'(SELECT\s+.*?)(?=\s+El\s|\n\n|\n[A-Z]|$|;)'
        matches = re.findall(select_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if matches:
            query = matches[0].strip()
            # Asegurar que termine con punto y coma
            if not query.endswith(';'):
                query += ';'
            return query
            
        return None
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """Generar sugerencias inteligentes basadas en el contexto"""
        suggestions = []
        message_lower = message.lower()
        
        # Sugerencias contextuales más inteligentes
        if "cuántas" in message_lower or "cuántos" in message_lower:
            if "actividad" in message_lower:
                suggestions.extend([
                    "Muéstrame las actividades por año",
                    "¿Cuáles son las actividades más costosas?",
                    "Muéstrame la distribución de actividades por estado"
                ])
            elif "contrato" in message_lower:
                suggestions.extend([
                    "Muéstrame los contratos por empresa",
                    "¿Cuál es el valor promedio de los contratos?",
                    "Muéstrame los contratos por fecha de inicio"
                ])
            else:
                suggestions.extend([
                    "Muéstrame un resumen de todas las tablas",
                    "¿Cuáles son los datos más recientes?",
                    "Muéstrame las tendencias principales"
                ])
        
        elif "muéstrame" in message_lower or "mostrar" in message_lower:
            if "actividad" in message_lower:
                suggestions.extend([
                    "¿Cuántas actividades están activas?",
                    "Muéstrame las actividades por valor",
                    "¿Cuáles son las actividades más recientes?"
                ])
            elif "contrato" in message_lower:
                suggestions.extend([
                    "¿Cuántos contratos están activos?",
                    "Muéstrame los contratos por valor",
                    "¿Cuáles son los contratos más recientes?"
                ])
            else:
                suggestions.extend([
                    "Muéstrame un dashboard completo",
                    "¿Cuáles son los KPIs principales?",
                    "Muéstrame las métricas más importantes"
                ])
        
        elif "año" in message_lower or "tiempo" in message_lower:
            suggestions.extend([
                "Muéstrame las tendencias por mes",
                "¿Cuáles son los datos más recientes?",
                "Muéstrame la evolución histórica"
            ])
        
        elif "valor" in message_lower or "costo" in message_lower or "precio" in message_lower:
            suggestions.extend([
                "Muéstrame los valores más altos",
                "¿Cuál es el promedio de valores?",
                "Muéstrame la distribución de valores"
            ])
        
        else:
            # Sugerencias generales inteligentes
            suggestions.extend([
                "Muéstrame un resumen completo",
                "¿Cuáles son los datos más importantes?",
                "Muéstrame las métricas principales"
            ])
            
        return suggestions[:3]  # Máximo 3 sugerencias
    
    def _generate_query_summary(self, sql_query: Optional[str]) -> Optional[str]:
        """Generar resumen de la consulta SQL"""
        if not sql_query:
            return None
            
        # Extraer información básica de la consulta
        if "SUM(" in sql_query.upper():
            return "Consulta de agregación con sumas"
        elif "COUNT(" in sql_query.upper():
            return "Consulta de conteo de registros"
        elif "AVG(" in sql_query.upper():
            return "Consulta de promedios"
        elif "GROUP BY" in sql_query.upper():
            return "Consulta agrupada por categorías"
        else:
            return "Consulta de datos detallados"
    
    async def get_pending_query(self, conversation_id: Optional[str] = None) -> Optional[str]:
        """Obtener consulta SQL pendiente"""
        if conversation_id:
            return self.pending_queries.get(conversation_id)
        else:
            # Retornar la última consulta pendiente
            return list(self.pending_queries.values())[-1] if self.pending_queries else None
    
    async def reset_conversation(self, conversation_id: Optional[str] = None):
        """Reiniciar conversación"""
        if conversation_id:
            self.conversations.pop(conversation_id, None)
            self.pending_queries.pop(conversation_id, None)
        else:
            self.conversations.clear()
            self.pending_queries.clear()
