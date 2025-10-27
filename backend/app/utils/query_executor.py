"""
Ejecutor de consultas SQL con análisis de visualización
"""
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

def safe_float(value):
    """Convertir a float de forma segura"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def execute_query(sql_query: str, db: Session) -> Dict[str, Any]:
    """
    Ejecutar consulta SQL y determinar tipo de visualización
    
    Args:
        sql_query: Consulta SQL a ejecutar
        db: Sesión de base de datos
        
    Returns:
        Dict con datos y metadatos de visualización
    """
    try:
        print(f"🔍 Ejecutando consulta: {sql_query}")
        
        # Ejecutar consulta
        result = db.execute(text(sql_query))
        
        # Obtener datos y columnas
        rows = result.fetchall()
        columns = list(result.keys())
        
        print(f"📊 Resultado: {len(rows)} filas, {len(columns)} columnas")
        
        if not rows:
            return {
                "data": {"message": "No se encontraron resultados"},
                "visualization_type": "text"
            }
        
        # Analizar tipo de visualización
        viz_type = determine_visualization_type(rows, columns, sql_query)
        
        # Formatear datos según tipo de visualización
        formatted_data = format_data_for_visualization(rows, columns, viz_type)
        
        return {
            "data": formatted_data,
            "visualization_type": viz_type,
            "row_count": len(rows),
            "columns": columns
        }
        
    except Exception as e:
        raise Exception(f"Error ejecutando consulta: {str(e)}")

def determine_visualization_type(rows: List, columns: List[str], sql_query: str) -> str:
    """
    Determinar el tipo de visualización más apropiado basado en el contexto y datos
    
    Args:
        rows: Lista de filas de resultados
        columns: Lista de nombres de columnas
        sql_query: Consulta SQL original
        
    Returns:
        str: Tipo de visualización recomendado
    """
    num_rows = len(rows)
    num_cols = len(columns)
    
    # Buscar indicadores en la consulta SQL
    query_upper = sql_query.upper()
    
    # Análisis de columnas numéricas
    numeric_cols = 0
    if rows:
        for col_idx in range(len(columns)):
            if all(isinstance(row[col_idx], (int, float)) and row[col_idx] is not None for row in rows):
                numeric_cols += 1
    
    # 1. KPIs (una sola fila con números) - MÁS PRIORITARIO
    if num_rows == 1 and num_cols <= 4 and numeric_cols >= 1:
        return "kpi_cards"
    
    # 2. Proporciones y distribuciones -> gráfico de pastel
    if (num_rows <= 8 and num_rows >= 2 and 
        any(keyword in query_upper for keyword in ['COUNT(', 'SUM(', 'DISTINCT']) and
        'GROUP BY' in query_upper):
        return "pie_chart"
    
    # 3. Tendencias temporales -> gráfico de líneas
    if (any(keyword in query_upper for keyword in ['YEAR', 'MONTH', 'DAY', 'DATE']) and
        num_cols >= 2 and num_rows >= 3):
        return "line_chart"
    
    # 4. Comparaciones por categoría -> gráfico de barras
    if ('GROUP BY' in query_upper and 
        any(keyword in query_upper for keyword in ['COUNT(', 'SUM(', 'AVG(']) and
        num_rows >= 2 and num_rows <= 15):
        return "bar_chart"
    
    # 5. Mapa de calor para datos tabulares con múltiples columnas numéricas
    if num_rows >= 3 and num_cols >= 3 and numeric_cols >= 3:
        return "heatmap"
    
    # 6. Gráfico de dispersión para correlaciones
    if (num_rows >= 5 and numeric_cols >= 2 and 
        any(keyword in query_upper for keyword in ['CORRELATION', 'RELATION', 'SCATTER'])):
        return "scatter_chart"
    
    # 7. Gráfico de radar para comparaciones multidimensionales
    if num_rows >= 2 and num_cols >= 3 and numeric_cols >= 3:
        return "radar_chart"
    
    # 8. Gráfico de área para muchas series temporales
    if (any(keyword in query_upper for keyword in ['YEAR', 'MONTH', 'DAY']) and
        num_cols >= 4 and num_rows >= 3):
        return "area_chart"
    
    # 9. Tabla para datos simples
    if num_rows <= 10 and num_cols <= 5:
        return "table"
    
    # Por defecto, tabla
    return "table"

def format_data_for_visualization(rows: List, columns: List[str], viz_type: str) -> Dict[str, Any]:
    """
    Formatear datos según el tipo de visualización
    
    Args:
        rows: Lista de filas de resultados
        columns: Lista de nombres de columnas
        viz_type: Tipo de visualización
        
    Returns:
        Dict con datos formateados
    """
    if viz_type == "table":
        return {
            "type": "table",
            "columns": columns,
            "rows": [list(row) for row in rows]
        }
    
    elif viz_type == "line_chart":
        # Asumir primera columna es x-axis, resto son series
        x_col = columns[0]
        series_cols = columns[1:]
        
        return {
            "type": "line_chart",
            "x_axis": x_col,
            "series": [
                {
                    "name": col,
                    "data": [row[i] for row in rows for i, c in enumerate(columns) if c == col]
                } for col in series_cols
            ],
            "x_labels": [str(row[0]) for row in rows]
        }
    
    elif viz_type == "bar_chart":
        x_col = columns[0]
        y_col = columns[1] if len(columns) > 1 else columns[0]
        
        return {
            "type": "bar_chart",
            "x_axis": x_col,
            "y_axis": y_col,
            "data": [
                {"category": str(row[0]), "value": safe_float(row[1]) if len(row) > 1 else safe_float(row[0])}
                for row in rows
            ]
        }
    
    elif viz_type == "pie_chart":
        label_col = columns[0]
        value_col = columns[1] if len(columns) > 1 else columns[0]
        
        # Calcular total para porcentajes
        total = sum(safe_float(row[1]) if len(row) > 1 else safe_float(row[0]) for row in rows)
        
        return {
            "type": "pie_chart",
            "data": [
                {
                    "label": str(row[0]), 
                    "value": safe_float(row[1]) if len(row) > 1 else safe_float(row[0]),
                    "percentage": round((safe_float(row[1]) if len(row) > 1 else safe_float(row[0])) / total * 100, 1) if total > 0 else 0
                }
                for row in rows
            ]
        }
    
    elif viz_type == "kpi_cards":
        # Crear cards para valores numéricos
        cards = []
        for i, col in enumerate(columns):
            if rows and isinstance(rows[0][i], (int, float)):
                cards.append({
                    "title": col,
                    "value": float(rows[0][i]),
                    "format": "number"
                })
        
        return {
            "type": "kpi_cards",
            "cards": cards
        }
    
    elif viz_type == "heatmap":
        # Datos para mapa de calor
        return {
            "type": "heatmap",
            "data": [dict(zip(columns, row)) for row in rows]
        }
    
    elif viz_type == "area_chart":
        # Similar a line_chart pero con área
        x_col = columns[0]
        series_cols = columns[1:]
        
        return {
            "type": "area_chart",
            "x_axis": x_col,
            "series": [
                {
                    "name": col,
                    "data": [row[i] for row in rows for i, c in enumerate(columns) if c == col]
                } for col in series_cols
            ],
            "x_labels": [str(row[0]) for row in rows]
        }
    
    elif viz_type == "scatter_chart":
        # Datos para gráfico de dispersión
        return {
            "type": "scatter_chart",
            "data": [dict(zip(columns, row)) for row in rows]
        }
    
    elif viz_type == "radar_chart":
        # Datos para gráfico de radar
        return {
            "type": "radar_chart",
            "data": [dict(zip(columns, row)) for row in rows]
        }
    
    else:
        # Fallback a tabla
        return {
            "type": "table",
            "columns": columns,
            "rows": [list(row) for row in rows]
        }
