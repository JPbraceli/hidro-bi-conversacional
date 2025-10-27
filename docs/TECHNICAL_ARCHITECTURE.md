# 🏗️ HIDRO Chat - Documentación Técnica Completa

## 📋 Índice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Requisitos Funcionales](#requisitos-funcionales)
4. [Tecnologías por Capa](#tecnologías-por-capa)
5. [Diagramas UML](#diagramas-uml)
6. [Flujos de Datos](#flujos-de-datos)
7. [Configuración e Instalación](#configuración-e-instalación)
8. [API Reference](#api-reference)
9. [Base de Datos](#base-de-datos)
10. [Seguridad y Rendimiento](#seguridad-y-rendimiento)

---

## 🎯 Resumen Ejecutivo

**HIDRO Chat** es un sistema de Business Intelligence conversacional que transforma consultas en lenguaje natural en insights visuales automáticos. Funciona como un "Amazon QuickSight" o "ChatGPT" especializado para datos empresariales de HIDRO.

### **Objetivos Principales**
- Permitir consultas en lenguaje natural sobre bases de datos PostgreSQL
- Generar visualizaciones automáticas inteligentes
- Proporcionar respuestas conversacionales contextuales
- Mantener historial de conversaciones
- Ofrecer sugerencias inteligentes

### **Valor de Negocio**
- **Reducción de tiempo**: De horas a segundos para obtener insights
- **Democratización de datos**: Acceso sin conocimiento técnico de SQL
- **Visualizaciones automáticas**: Sin necesidad de configurar gráficos
- **Interfaz conversacional**: Experiencia similar a ChatGPT

---

## 🏛️ Arquitectura del Sistema

### **Patrón Arquitectónico: Microservicios con API Gateway**

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   React App     │  │  Tailwind CSS   │  │  Vite Dev    │  │
│  │   (Frontend)    │  │   (Styling)     │  │  (Build)     │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE API                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   FastAPI       │  │   SQLAlchemy    │  │  Pydantic    │  │
│  │   (Backend)     │  │   (ORM)         │  │  (Validation)│  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                CAPA DE INTELIGENCIA                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Ollama        │  │  phi3:mini      │  │  Prompt      │  │
│  │   (LLM Runtime) │  │  (AI Model)     │  │  Engine      │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Queries
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   PostgreSQL    │  │   Multiple      │  │   Schema     │  │
│  │   (Database)    │  │   Schemas       │  │   Manager    │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Componentes Principales**

#### **1. Frontend (React + Vite)**
- **Puerto**: 3000
- **Tecnología**: React 18, Vite, Tailwind CSS
- **Responsabilidades**: UI/UX, gestión de estado, visualizaciones

#### **2. Backend (FastAPI)**
- **Puerto**: 8001
- **Tecnología**: FastAPI, SQLAlchemy, Pydantic
- **Responsabilidades**: API REST, lógica de negocio, validación

#### **3. LLM (Ollama)**
- **Puerto**: 11434
- **Tecnología**: Ollama, phi3:mini
- **Responsabilidades**: Procesamiento de lenguaje natural, generación de SQL

#### **4. Base de Datos (PostgreSQL)**
- **Puerto**: 15433
- **Tecnología**: PostgreSQL 15
- **Responsabilidades**: Almacenamiento de datos, consultas SQL

---

## 📋 Requisitos Funcionales

### **RF-001: Interfaz Conversacional**
- **Descripción**: El sistema debe proporcionar una interfaz de chat similar a ChatGPT
- **Criterios de Aceptación**:
  - Usuario puede escribir mensajes en lenguaje natural
  - Sistema responde con escritura progresiva
  - Interfaz es responsive y moderna
  - Soporte para historial de conversación

### **RF-002: Procesamiento de Lenguaje Natural**
- **Descripción**: El sistema debe entender consultas en español
- **Criterios de Aceptación**:
  - Comprende preguntas sobre actividades, contratos, usuarios
  - Genera consultas SQL válidas
  - Maneja contexto conversacional
  - Proporciona sugerencias inteligentes

### **RF-003: Visualizaciones Automáticas**
- **Descripción**: El sistema debe generar visualizaciones apropiadas
- **Criterios de Aceptación**:
  - Detecta automáticamente el tipo de visualización
  - Soporta tablas, gráficos de barras, líneas, pastel, KPIs
  - Renderiza visualizaciones interactivas
  - Maneja datos vacíos o errores

### **RF-004: Gestión de Base de Datos**
- **Descripción**: El sistema debe conectarse a múltiples esquemas
- **Criterios de Aceptación**:
  - Conexión a PostgreSQL en puerto 15433
  - Acceso a 5 esquemas diferentes
  - Validación de consultas SQL
  - Manejo de errores de conexión

### **RF-005: Sugerencias Inteligentes**
- **Descripción**: El sistema debe ofrecer sugerencias contextuales
- **Criterios de Aceptación**:
  - Máximo 3 sugerencias por respuesta
  - Basadas en palabras clave del mensaje
  - Categorizadas por dominio
  - Clickables para ejecutar

---

## 🛠️ Tecnologías por Capa

### **CAPA DE PRESENTACIÓN**

#### **React 18**
```javascript
// Características principales
- Hooks modernos (useState, useEffect, useRef)
- Componentes funcionales
- Gestión de estado local
- Re-renderizado optimizado
```

**Ventajas:**
- Virtual DOM para rendimiento
- Ecosistema rico de librerías
- Desarrollo rápido con hot reload
- Componentes reutilizables

#### **Vite**
```javascript
// Configuración vite.config.js
export default {
  server: {
    proxy: {
      '/api': 'http://localhost:8001'
    }
  }
}
```

**Ventajas:**
- Build ultra-rápido con esbuild
- Hot Module Replacement (HMR)
- Proxy automático para desarrollo
- Soporte nativo para TypeScript

#### **Tailwind CSS**
```css
/* Ejemplo de clases utilitarias */
.chat-bubble {
  @apply px-4 py-3 rounded-2xl max-w-xs;
}
.chat-bubble-user {
  @apply bg-blue-600 text-white ml-auto;
}
.chat-bubble-assistant {
  @apply bg-gray-100 text-gray-900;
}
```

**Ventajas:**
- Estilos utilitarios
- Diseño responsive automático
- Tamaño de bundle optimizado
- Consistencia visual

### **CAPA DE API**

#### **FastAPI**
```python
# Ejemplo de endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """Endpoint principal del chat conversacional"""
    try:
        response = await prompt_engine.generate_response(
            message=chat_message.message,
            conversation_id=chat_message.conversation_id,
            db=db
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Ventajas:**
- Validación automática con Pydantic
- Documentación automática (Swagger)
- Soporte nativo para async/await
- Type hints completos

#### **SQLAlchemy**
```python
# Configuración de motor
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=True
)

# Ejecución de consultas
result = db.execute(text(sql_query))
rows = result.fetchall()
```

**Ventajas:**
- ORM potente y flexible
- Pool de conexiones automático
- Soporte para múltiples bases de datos
- Migraciones automáticas

### **CAPA DE INTELIGENCIA**

#### **Ollama**
```python
# Integración con Ollama
response = ollama.chat(
    model="phi3:mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)
```

**Ventajas:**
- Ejecución local (sin dependencias externas)
- Modelos optimizados para CPU
- API simple y directa
- Control total sobre el modelo

#### **phi3:mini**
- **Parámetros**: 3.8B
- **Contexto**: 128K tokens
- **Idioma**: Multilingüe (optimizado para español)
- **Velocidad**: ~20 tokens/segundo
- **Memoria**: ~2.5GB RAM

### **CAPA DE DATOS**

#### **PostgreSQL 15**
```sql
-- Ejemplo de esquema
CREATE SCHEMA dev_hdcr_activities;
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    vigente BOOLEAN DEFAULT true
);
```

**Ventajas:**
- ACID compliance
- Soporte para JSON
- Índices avanzados
- Replicación nativa

---

## 📊 Diagramas UML

### **Diagrama de Secuencia - Flujo Completo**

```
Usuario    Frontend    Backend    LLM      Database
   │           │          │        │         │
   │───1. Escribe consulta──→│        │         │
   │           │          │        │         │
   │           │───2. POST /api/chat──→│        │
   │           │          │        │         │
   │           │          │───3. Procesar con LLM──→│
   │           │          │        │         │
   │           │          │←──4. Respuesta del LLM──│
   │           │          │        │         │
   │           │          │───5. Generar SQL──→│
   │           │          │        │         │
   │           │          │───6. Ejecutar consulta──→│
   │           │          │        │         │
   │           │          │←──7. Resultados──│
   │           │          │        │         │
   │           │          │───8. Analizar visualización──→│
   │           │          │        │         │
   │           │          │←──9. Tipo de visualización──│
   │           │          │        │         │
   │           │←──10. JSON Response──│        │         │
   │           │          │        │         │
   │←──11. Mostrar resultado──│        │         │
   │           │          │        │         │
```

### **Diagrama de Estados - Conversación**

```
[Inicio] ──→ [Esperando Input]
    │              │
    │              │ Usuario escribe
    │              ▼
    │         [Procesando]
    │              │
    │              │ LLM responde
    │              ▼
    │         [Generando SQL]
    │              │
    │              │ SQL válido
    │              ▼
    │         [Ejecutando Query]
    │              │
    │              │ Resultados OK
    │              ▼
    │         [Analizando Visualización]
    │              │
    │              │ Tipo determinado
    │              ▼
    │         [Renderizando]
    │              │
    │              │ Visualización lista
    │              ▼
    │         [Mostrando Resultado]
    │              │
    │              │ Usuario continúa
    │              ▼
    └───────── [Esperando Input]
```

### **Diagrama de Clases - Arquitectura**

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   App       │  │ ChatInterface│  │ VisualizationPanel  │  │
│  │   +state    │  │ +messages    │  │ +renderVisualization│  │
│  │   +handlers │  │ +sendMessage │  │ +determineType      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Layer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ ChatRouter  │  │ PromptEngine│  │ QueryExecutor       │  │
│  │ +chat()    │  │ +generate() │  │ +execute()         │  │
│  │ +execute() │  │ +extract()  │  │ +analyze()         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SQL
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ PostgreSQL  │  │ Activities  │  │ Contracts           │  │
│  │ +connect()  │  │ +id         │  │ +id                 │  │
│  │ +query()    │  │ +name       │  │ +company            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujos de Datos

### **Flujo 1: Consulta Simple**

```mermaid
graph TD
    A[Usuario: "¿Cuántas actividades hay?"] --> B[React: Captura input]
    B --> C[Fetch: POST /api/chat]
    C --> D[FastAPI: Valida request]
    D --> E[PromptEngine: Procesa con LLM]
    E --> F[Ollama: Genera respuesta]
    F --> G[SQL: SELECT COUNT(*) FROM activities]
    G --> H[PostgreSQL: Ejecuta query]
    H --> I[QueryExecutor: Analiza resultados]
    I --> J[Visualización: KPI Card]
    J --> K[React: Renderiza resultado]
    K --> L[Usuario: Ve "515 actividades"]
```

### **Flujo 2: Consulta Compleja con Agregación**

```mermaid
graph TD
    A[Usuario: "Actividades por año"] --> B[React: Captura input]
    B --> C[Fetch: POST /api/chat]
    C --> D[FastAPI: Valida request]
    D --> E[PromptEngine: Procesa con LLM]
    E --> F[Ollama: Genera respuesta]
    F --> G[SQL: SELECT anio_campania, COUNT(*) FROM activities GROUP BY anio_campania]
    G --> H[PostgreSQL: Ejecuta query]
    H --> I[QueryExecutor: Analiza resultados]
    I --> J[Visualización: Bar Chart]
    J --> K[React: Renderiza gráfico]
    K --> L[Usuario: Ve gráfico de barras]
```

### **Flujo 3: Manejo de Errores**

```mermaid
graph TD
    A[Usuario: "Consulta inválida"] --> B[React: Captura input]
    B --> C[Fetch: POST /api/chat]
    C --> D[FastAPI: Valida request]
    D --> E[PromptEngine: Procesa con LLM]
    E --> F[Ollama: Genera SQL inválido]
    F --> G[SQL: SELECT * FROM tabla_inexistente]
    G --> H[PostgreSQL: Error de tabla]
    H --> I[QueryExecutor: Captura error]
    I --> J[FastAPI: Retorna error]
    J --> K[React: Muestra mensaje de error]
    K --> L[Usuario: Ve "Error: tabla no existe"]
```

---

## ⚙️ Configuración e Instalación

### **Requisitos del Sistema**

#### **Hardware Mínimo**
- **RAM**: 8GB (recomendado 16GB)
- **CPU**: 4 cores (recomendado 8 cores)
- **Disco**: 10GB libres
- **Red**: Conexión a internet para descargar modelos

#### **Software Requerido**
- **Node.js**: 16+ (para frontend)
- **Python**: 3.8+ (para backend)
- **PostgreSQL**: 13+ (base de datos)
- **Ollama**: Última versión (LLM)

### **Instalación Paso a Paso**

#### **1. Clonar Repositorio**
```bash
git clone <repository-url>
cd hidronuevo
```

#### **2. Configurar Backend**
```bash
cd backend
pip install -r requirements-simple.txt
cp env.example .env
# Editar .env con configuraciones
```

#### **3. Configurar Frontend**
```bash
cd frontend
npm install
```

#### **4. Configurar Base de Datos**
```bash
# Crear base de datos
createdb -h 127.0.0.1 -p 15433 -U hdcruser hidrodb

# Importar dumps
python scripts/import_dumps_with_password.py
```

#### **5. Configurar Ollama**
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo
ollama pull phi3:mini

# Iniciar servicio
ollama serve
```

#### **6. Levantar Sistema**
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Ollama (si no está como servicio)
ollama serve
```

---

## 📚 API Reference

### **Endpoints Principales**

#### **POST /api/chat**
```json
// Request
{
  "message": "¿Cuántas actividades hay?",
  "conversation_id": "uuid-123"
}

// Response
{
  "response": "Hay 515 actividades en total",
  "suggestions": ["Muéstrame por estado", "¿Cuántas están activas?"],
  "is_ready": true,
  "query_summary": "Consulta de conteo",
  "conversation_id": "uuid-123"
}
```

#### **POST /api/execute-chat-query**
```json
// Response
{
  "success": true,
  "data": {
    "type": "kpi_cards",
    "cards": [
      {
        "title": "Total Actividades",
        "value": 515,
        "format": "number"
      }
    ]
  },
  "visualization_type": "kpi_cards"
}
```

#### **POST /api/reset-chat**
```json
// Response
{
  "message": "Chat reiniciado exitosamente"
}
```

#### **GET /api/suggestions**
```json
// Response
{
  "suggestions": [
    "¿Cuántas actividades están activas?",
    "Muéstrame los contratos activos",
    "¿Cuántos usuarios hay registrados?"
  ]
}
```

---

## 🗄️ Base de Datos

### **Esquemas Disponibles**

#### **dev_hdcr_activities**
```sql
-- Tabla principal: activities
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    amount DECIMAL(15,2),
    vigente BOOLEAN DEFAULT true,
    anio_campania INTEGER,
    code VARCHAR(100),
    id_contract INTEGER
);

-- Estadísticas
SELECT COUNT(*) FROM activities; -- 515 registros
```

#### **dev_hdcr_profile**
```sql
-- Tabla de perfiles de usuario
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **dev_hdcr_contracts**
```sql
-- Tabla de contratos
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    contract_number VARCHAR(100) NOT NULL,
    company VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    value DECIMAL(15,2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Consultas de Ejemplo**

#### **KPIs Principales**
```sql
-- Total de actividades
SELECT COUNT(*) as total_actividades FROM activities;

-- Actividades activas
SELECT COUNT(*) as actividades_activas 
FROM activities WHERE vigente = true;

-- Valor total de contratos
SELECT SUM(value) as valor_total 
FROM contracts WHERE status = 'active';
```

#### **Agregaciones por Tiempo**
```sql
-- Actividades por año
SELECT anio_campania, COUNT(*) as cantidad
FROM activities 
GROUP BY anio_campania 
ORDER BY anio_campania;

-- Contratos por mes
SELECT 
    EXTRACT(YEAR FROM start_date) as año,
    EXTRACT(MONTH FROM start_date) as mes,
    COUNT(*) as cantidad
FROM contracts 
GROUP BY año, mes 
ORDER BY año, mes;
```

---

## 🔒 Seguridad y Rendimiento

### **Medidas de Seguridad**

#### **Validación de SQL**
```python
def validate_sql_query(sql_query: str) -> Tuple[bool, str]:
    """Validar consulta SQL para prevenir inyecciones"""
    # Solo permitir SELECT
    if not sql_query.strip().upper().startswith('SELECT'):
        return False, "Solo se permiten consultas SELECT"
    
    # Bloquear comandos peligrosos
    dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
    if any(keyword in sql_query.upper() for keyword in dangerous_keywords):
        return False, "Comando no permitido"
    
    return True, "Consulta válida"
```

#### **Autenticación (Futuro)**
```python
# Planificado para futuras versiones
@router.post("/chat")
async def chat_endpoint(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Implementar autenticación JWT
    pass
```

### **Optimizaciones de Rendimiento**

#### **Pool de Conexiones**
```python
engine = create_engine(
    database_url,
    pool_size=10,           # 10 conexiones simultáneas
    max_overflow=20,        # 20 conexiones adicionales
    pool_pre_ping=True,     # Verificar conexiones
    pool_recycle=300        # Reciclar cada 5 minutos
)
```

#### **Caché de Respuestas**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_database_schema(db):
    """Cachear esquema de base de datos"""
    # Implementación con caché
    pass
```

#### **Compresión de Respuestas**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### **Monitoreo y Logs**

#### **Logging Estructurado**
```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# En endpoints
logger.info(f"Consulta recibida: {message}")
logger.info(f"SQL generado: {sql_query}")
logger.info(f"Resultados: {len(rows)} filas")
```

#### **Métricas de Rendimiento**
```python
import time

@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    start_time = time.time()
    
    # Procesar consulta
    response = await process_query(chat_message.message)
    
    # Registrar métricas
    processing_time = time.time() - start_time
    logger.info(f"Tiempo de procesamiento: {processing_time:.2f}s")
    
    return response
```

---

## 🚀 Próximas Mejoras

### **Versión 2.0**
- [ ] Autenticación JWT
- [ ] Roles y permisos
- [ ] Exportación de datos (PDF, Excel)
- [ ] Dashboard de métricas
- [ ] Notificaciones en tiempo real

### **Versión 3.0**
- [ ] Múltiples bases de datos
- [ ] Cache distribuido (Redis)
- [ ] Microservicios independientes
- [ ] Kubernetes deployment
- [ ] Machine Learning para sugerencias

---

**¡Documentación técnica completa! 🎉**

Esta documentación proporciona una visión integral del sistema HIDRO Chat, desde la arquitectura hasta los detalles de implementación. ¿Te gustaría que profundice en alguna sección específica?


