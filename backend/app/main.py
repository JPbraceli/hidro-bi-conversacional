"""
Aplicación principal FastAPI para solución local tipo "Amazon Q"
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.dependencies import get_settings

# Configuración
settings = get_settings()

# Crear aplicación FastAPI
app = FastAPI(
    title="HidroChat - Asistente de Consultas",
    description="Solución local tipo Amazon Q para consultas conversacionales a PostgreSQL",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "HidroChat API - Asistente de Consultas"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "hidrochat-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





