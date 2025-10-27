"""
Router para el chat conversacional
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import ollama
from app.dependencies import get_db, get_settings
from app.llm.prompt_engine import PromptEngine
from app.utils.validate_sql import validate_sql_query
from app.utils.query_executor import execute_query

router = APIRouter()

class ChatMessage(BaseModel):
    """Modelo para mensaje de chat"""
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Modelo para respuesta del chat"""
    response: str
    suggestions: List[str] = []
    is_ready: bool = False
    query_summary: Optional[str] = None
    conversation_id: str

class ExecuteQueryResponse(BaseModel):
    """Modelo para respuesta de ejecución de consulta"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    visualization_type: Optional[str] = None

# Instancia global del motor de prompts
prompt_engine = PromptEngine()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal del chat conversacional
    """
    try:
        settings = get_settings()
        
        # Generar respuesta usando el LLM
        response = await prompt_engine.generate_response(
            message=chat_message.message,
            conversation_id=chat_message.conversation_id,
            db=db
        )
        
        return ChatResponse(
            response=response["text"],
            suggestions=response.get("suggestions", []),
            is_ready=response.get("is_ready", False),
            query_summary=response.get("query_summary"),
            conversation_id=response["conversation_id"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")

@router.post("/execute-chat-query", response_model=ExecuteQueryResponse)
async def execute_chat_query(
    db: Session = Depends(get_db)
):
    """
    Ejecutar la consulta SQL generada en el chat
    """
    try:
        # Obtener la consulta SQL del contexto del chat
        sql_query = await prompt_engine.get_pending_query()
        
        if not sql_query:
            return ExecuteQueryResponse(
                success=False,
                error="No hay consulta pendiente para ejecutar"
            )
        
        # Validar la consulta SQL
        is_valid, validation_error = validate_sql_query(sql_query)
        if not is_valid:
            return ExecuteQueryResponse(
                success=False,
                error=f"Consulta SQL inválida: {validation_error}"
            )
        
        # Ejecutar la consulta
        result = execute_query(sql_query, db)
        
        return ExecuteQueryResponse(
            success=True,
            data=result["data"],
            visualization_type=result.get("visualization_type")
        )
        
    except Exception as e:
        return ExecuteQueryResponse(
            success=False,
            error=f"Error ejecutando consulta: {str(e)}"
        )

@router.post("/reset-chat")
async def reset_chat():
    """
    Reiniciar el contexto del chat
    """
    try:
        await prompt_engine.reset_conversation()
        return {"message": "Chat reiniciado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reiniciando chat: {str(e)}")

@router.get("/suggestions")
async def get_suggestions():
    """
    Obtener sugerencias de preguntas para el sistema HIDRO
    """
    suggestions = [
        "¿Cuántas actividades están activas?",
        "Muéstrame los contratos activos",
        "¿Cuántos usuarios hay registrados?",
        "¿Cuál es el estado de los gateways?",
        "Muéstrame las actividades por estado",
        "¿Cuántos administradores hay en el sistema?",
        "¿Cuál es el valor total de los contratos?",
        "Muéstrame los perfiles de usuario por rol",
        "¿Cuáles son las actividades más recientes?",
        "¿Cuántos gateways están activos?"
    ]
    
    return {"suggestions": suggestions}
