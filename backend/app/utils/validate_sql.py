"""
Validación de consultas SQL para seguridad
"""
import sqlparse
import re
from typing import Tuple

# Palabras clave prohibidas
FORBIDDEN_KEYWORDS = [
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE',
    'GRANT', 'REVOKE', 'EXEC', 'EXECUTE', 'CALL', 'MERGE', 'UPSERT'
]

# Patrones peligrosos
DANGEROUS_PATTERNS = [
    r';\s*--',  # Comentarios después de punto y coma
    r';\s*/\*',  # Comentarios de bloque después de punto y coma
    r'UNION\s+SELECT',  # Union attacks
    r'--',  # Comentarios SQL
    r'/\*.*?\*/',  # Comentarios de bloque
]

def validate_sql_query(query: str) -> Tuple[bool, str]:
    """
    Validar consulta SQL para asegurar que es segura
    
    Args:
        query: Consulta SQL a validar
        
    Returns:
        Tuple[bool, str]: (es_válida, mensaje_error)
    """
    if not query or not query.strip():
        return False, "Consulta vacía"
    
    # Limpiar la consulta
    clean_query = query.strip()
    
    # Verificar que no esté vacía después de limpiar
    if not clean_query:
        return False, "Consulta vacía después de limpiar"
    
    # Parsear la consulta
    try:
        parsed = sqlparse.parse(clean_query)
        if not parsed:
            return False, "No se pudo parsear la consulta SQL"
            
        statement = parsed[0]
        
        # Verificar que sea un SELECT
        if statement.get_type() != 'SELECT':
            return False, f"Tipo de consulta no permitido: {statement.get_type()}"
            
    except Exception as e:
        return False, f"Error parseando SQL: {str(e)}"
    
    # Verificar palabras clave prohibidas
    query_upper = clean_query.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False, f"Palabra clave prohibida encontrada: {keyword}"
    
    # Verificar patrones peligrosos
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, clean_query, re.IGNORECASE | re.DOTALL):
            return False, f"Patrón peligroso detectado: {pattern}"
    
    # Verificar múltiples declaraciones
    statements = sqlparse.split(clean_query)
    if len(statements) > 1:
        return False, "Múltiples declaraciones SQL no están permitidas"
    
    # Verificar que comience con SELECT
    if not query_upper.strip().startswith('SELECT'):
        return False, "La consulta debe comenzar con SELECT"
    
    # Verificar caracteres sospechosos (removido ';' que es válido en SQL)
    suspicious_chars = ['--', '/*', '*/', 'xp_', 'sp_']
    for char in suspicious_chars:
        if char in clean_query:
            return False, f"Carácter sospechoso encontrado: {char}"
    
    return True, "Consulta válida"

def sanitize_sql_query(query: str) -> str:
    """
    Sanitizar consulta SQL removiendo caracteres peligrosos
    
    Args:
        query: Consulta SQL a sanitizar
        
    Returns:
        str: Consulta sanitizada
    """
    # Remover comentarios
    query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
    query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
    
    # Remover punto y coma al final
    query = query.rstrip(';')
    
    # Limpiar espacios extra
    query = ' '.join(query.split())
    
    return query

def extract_tables_from_query(query: str) -> list:
    """
    Extraer nombres de tablas de una consulta SELECT
    
    Args:
        query: Consulta SQL
        
    Returns:
        list: Lista de nombres de tablas
    """
    try:
        parsed = sqlparse.parse(query)
        if not parsed:
            return []
            
        statement = parsed[0]
        tables = []
        
        # Buscar en FROM y JOIN clauses
        for token in statement.flatten():
            if token.ttype is sqlparse.tokens.Keyword and token.value.upper() in ['FROM', 'JOIN']:
                # El siguiente token debería ser el nombre de la tabla
                continue
            elif token.ttype is sqlparse.tokens.Name:
                tables.append(token.value)
        
        return list(set(tables))  # Remover duplicados
        
    except Exception:
        return []




