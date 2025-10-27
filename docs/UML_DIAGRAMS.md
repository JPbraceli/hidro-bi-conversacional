# 📊 Diagramas UML - HIDRO Chat

## 📋 Índice

1. [Diagrama de Secuencia - Flujo Completo](#diagrama-de-secuencia---flujo-completo)
2. [Diagrama de Estados - Conversación](#diagrama-de-estados---conversación)
3. [Diagrama de Clases - Arquitectura](#diagrama-de-clases---arquitectura)
4. [Diagrama de Componentes](#diagrama-de-componentes)
5. [Diagrama de Despliegue](#diagrama-de-despliegue)
6. [Diagrama de Casos de Uso](#diagrama-de-casos-de-uso)

---

## 🔄 Diagrama de Secuencia - Flujo Completo

### **Escenario: Consulta "¿Cuántas actividades hay?"**

```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Usuario │  │Frontend │  │ Backend │  │   LLM   │  │Database │
└─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
     │           │           │           │           │
     │──1. Escribe consulta─→│           │           │
     │           │           │           │           │
     │           │──2. POST /api/chat───→│           │
     │           │           │           │           │
     │           │           │──3. Procesar con LLM──→│
     │           │           │           │           │
     │           │           │←──4. Respuesta del LLM─│
     │           │           │           │           │
     │           │           │──5. Generar SQL──────→│
     │           │           │           │           │
     │           │           │──6. Ejecutar consulta─→│
     │           │           │           │           │
     │           │           │←──7. Resultados───────│
     │           │           │           │           │
     │           │           │──8. Analizar visualización─→│
     │           │           │           │           │
     │           │           │←──9. Tipo de visualización─│
     │           │           │           │           │
     │           │←──10. JSON Response──│           │
     │           │           │           │           │
     │←──11. Mostrar resultado─│           │           │
     │           │           │           │           │
```

### **Escenario: Error en Consulta**

```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Usuario │  │Frontend │  │ Backend │  │   LLM   │  │Database │
└─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
     │           │           │           │           │
     │──1. Consulta inválida─→│           │           │
     │           │           │           │           │
     │           │──2. POST /api/chat───→│           │
     │           │           │           │           │
     │           │           │──3. Procesar con LLM──→│
     │           │           │           │           │
     │           │           │←──4. SQL inválido─────│
     │           │           │           │           │
     │           │           │──5. Validar SQL──────→│
     │           │           │           │           │
     │           │           │←──6. Error de validación─│
     │           │           │           │           │
     │           │←──7. Error Response───│           │
     │           │           │           │           │
     │←──8. Mostrar error────│           │           │
     │           │           │           │           │
```

---

## 🔄 Diagrama de Estados - Conversación

### **Estados del Sistema**

```
┌─────────────────────────────────────────────────────────────┐
│                    Estados del Sistema                     │
└─────────────────────────────────────────────────────────────┘

[Inicio] ──────────────────────────────────────────────────────┐
    │                                                          │
    │ Usuario abre aplicación                                  │
    ▼                                                          │
[Esperando Input] ─────────────────────────────────────────────┘
    │                                                          │
    │ Usuario escribe mensaje                                  │
    ▼                                                          │
[Procesando] ──────────────────────────────────────────────────┐
    │                                                          │
    │ LLM procesa mensaje                                      │
    ▼                                                          │
[Generando SQL] ───────────────────────────────────────────────┐
    │                                                          │
    │ SQL generado exitosamente                                │
    ▼                                                          │
[Ejecutando Query] ────────────────────────────────────────────┐
    │                                                          │
    │ Query ejecutado exitosamente                             │
    ▼                                                          │
[Analizando Visualización] ────────────────────────────────────┐
    │                                                          │
    │ Tipo de visualización determinado                        │
    ▼                                                          │
[Renderizando] ────────────────────────────────────────────────┐
    │                                                          │
    │ Visualización renderizada                                │
    ▼                                                          │
[Mostrando Resultado] ─────────────────────────────────────────┘
    │                                                          │
    │ Usuario continúa conversación                            │
    ▼                                                          │
[Esperando Input] ─────────────────────────────────────────────┘
```

### **Estados de Error**

```
[Procesando] ──────────────────────────────────────────────────┐
    │                                                          │
    │ Error en LLM                                             │
    ▼                                                          │
[Error LLM] ────────────────────────────────────────────────────┐
    │                                                          │
    │ Mostrar mensaje de error                                 │
    ▼                                                          │
[Esperando Input] ─────────────────────────────────────────────┘

[Generando SQL] ───────────────────────────────────────────────┐
    │                                                          │
    │ SQL inválido generado                                    │
    ▼                                                          │
[Error SQL] ───────────────────────────────────────────────────┐
    │                                                          │
    │ Mostrar error de SQL                                     │
    ▼                                                          │
[Esperando Input] ─────────────────────────────────────────────┘

[Ejecutando Query] ───────────────────────────────────────────┐
    │                                                          │
    │ Error en base de datos                                   │
    ▼                                                          │
[Error Database] ───────────────────────────────────────────────┐
    │                                                          │
    │ Mostrar error de base de datos                           │
    ▼                                                          │
[Esperando Input] ─────────────────────────────────────────────┘
```

---

## 🏗️ Diagrama de Clases - Arquitectura

### **Frontend Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │      App        │    │ ChatInterface   │                │
│  │                 │    │                 │                │
│  │ +queryData      │◄──►│ +messages       │                │
│  │ +isLoading      │    │ +inputMessage   │                │
│  │ +handleExecute  │    │ +isLoading      │                │
│  │ +handleReset    │    │ +sendMessage()  │                │
│  └─────────────────┘    │ +handleKeyPress │                │
│                         └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │VisualizationPanel│    │   DataTable     │                │
│  │                 │    │                 │                │
│  │ +data           │◄──►│ +columns        │                │
│  │ +isLoading      │    │ +rows           │                │
│  │ +renderViz()    │    │ +renderTable()  │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │  BarChartComp  │    │  LineChartComp  │                │
│  │                 │    │                 │                │
│  │ +data           │    │ +data           │                │
│  │ +renderChart()  │    │ +renderChart()  │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### **Backend Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                    Backend Layer                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   ChatRouter    │    │  PromptEngine    │                │
│  │                 │    │                 │                │
│  │ +chat()         │◄──►│ +generate()     │                │
│  │ +execute()      │    │ +extractSQL()   │                │
│  │ +reset()        │    │ +buildPrompt()  │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ QueryExecutor   │    │  ValidateSQL    │                │
│  │                 │    │                 │                │
│  │ +execute()      │◄──►│ +validate()     │                │
│  │ +analyze()      │    │ +checkSafety()  │                │
│  │ +formatData()   │    └─────────────────┘                │
│  └─────────────────┘                                       │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Settings      │    │   Database      │                │
│  │                 │    │                 │                │
│  │ +db_host        │◄──►│ +engine         │                │
│  │ +db_port        │    │ +session        │                │
│  │ +ollama_host    │    │ +connect()      │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### **Data Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   PostgreSQL    │    │   Activities     │                │
│  │                 │    │                 │                │
│  │ +connect()      │◄──►│ +id              │                │
│  │ +query()        │    │ +name            │                │
│  │ +execute()      │    │ +start_date      │                │
│  └─────────────────┘    │ +end_date        │                │
│                         │ +vigente         │                │
│  ┌─────────────────┐    └─────────────────┘                │
│  │   Contracts     │                                       │
│  │                 │    ┌─────────────────┐                │
│  │ +id             │    │    Profiles     │                │
│  │ +company        │    │                 │                │
│  │ +start_date     │◄──►│ +id              │                │
│  │ +value          │    │ +first_name      │                │
│  │ +status         │    │ +last_name       │                │
│  └─────────────────┘    │ +email           │                │
│                         └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Diagrama de Componentes

### **Arquitectura de Componentes**

```
┌─────────────────────────────────────────────────────────────┐
│                    HIDRO Chat System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Frontend      │    │    Backend      │                │
│  │                 │    │                 │                │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │                │
│  │ │React App    │ │    │ │FastAPI      │ │                │
│  │ │             │ │    │ │             │ │                │
│  │ │- Components │ │◄──►│ │- Routers    │ │                │
│  │ │- State      │ │    │ │- Services   │ │                │
│  │ │- Utils      │ │    │ │- Models     │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   LLM Service   │    │   Database      │                │
│  │                 │    │                 │                │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │                │
│  │ │Ollama       │ │    │ │PostgreSQL   │ │                │
│  │ │             │ │    │ │             │ │                │
│  │ │- phi3:mini  │ │◄──►│ │- Activities │ │                │
│  │ │- Prompts    │ │    │ │- Contracts  │ │                │
│  │ │- Context    │ │    │ │- Profiles   │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### **Interacciones entre Componentes**

```
┌─────────────────────────────────────────────────────────────┐
│                Component Interactions                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend ◄─── HTTP/JSON ───► Backend                      │
│     │                              │                        │
│     │                              │                        │
│     │                              ▼                        │
│     │                         ┌─────────┐                   │
│     │                         │   LLM   │                   │
│     │                         │ Service │                   │
│     │                         └─────────┘                   │
│     │                              │                        │
│     │                              │                        │
│     │                              ▼                        │
│     │                         ┌─────────┐                   │
│     │                         │Database │                   │
│     │                         │ Service │                   │
│     │                         └─────────┘                   │
│     │                              │                        │
│     │                              │                        │
│     │                              ▼                        │
│     │                         ┌─────────┐                   │
│     │                         │PostgreSQL│                  │
│     │                         │Database │                   │
│     │                         └─────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Diagrama de Despliegue

### **Arquitectura de Despliegue**

```
┌─────────────────────────────────────────────────────────────┐
│                    Deployment Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Client        │    │   Server        │                │
│  │                 │    │                 │                │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │                │
│  │ │Web Browser  │ │    │ │Frontend      │ │                │
│  │ │             │ │    │ │(Port 3000)   │ │                │
│  │ │- React App  │ │◄──►│ │- Vite Dev    │ │                │
│  │ │- Tailwind   │ │    │ │- Hot Reload  │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    │                 │                │
│                         │ ┌─────────────┐ │                │
│                         │ │Backend      │ │                │
│                         │ │(Port 8001)   │ │                │
│                         │ │- FastAPI    │ │                │
│                         │ │- Uvicorn    │ │                │
│                         │ └─────────────┘ │                │
│                         │                 │                │
│                         │ ┌─────────────┐ │                │
│                         │ │LLM Service  │ │                │
│                         │ │(Port 11434) │ │                │
│                         │ │- Ollama     │ │                │
│                         │ │- phi3:mini  │ │                │
│                         │ └─────────────┘ │                │
│                         │                 │                │
│                         │ ┌─────────────┐ │                │
│                         │ │Database     │ │                │
│                         │ │(Port 15433) │ │                │
│                         │ │- PostgreSQL │ │                │
│                         │ │- Multiple   │ │                │
│                         │ │  Schemas    │ │                │
│                         │ └─────────────┘ │                │
│                         └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### **Docker Deployment (Opcional)**

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Deployment                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Frontend      │    │    Backend      │                │
│  │   Container     │    │   Container     │                │
│  │                 │    │                 │                │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │                │
│  │ │React App    │ │    │ │FastAPI      │ │                │
│  │ │             │ │    │ │             │ │                │
│  │ │- Port 3000  │ │◄──►│ │- Port 8000  │ │                │
│  │ │- Vite Build │ │    │ │- Python 3.8 │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Database      │    │   Network       │                │
│  │   Container     │    │                 │                │
│  │                 │    │ ┌─────────────┐ │                │
│  │ ┌─────────────┐ │    │ │hidrochat-   │ │                │
│  │ │PostgreSQL    │ │◄──►│ │network      │ │                │
│  │ │             │ │    │ │             │ │                │
│  │ │- Port 15433 │ │    │ │- Bridge     │ │                │
│  │ │- Volume      │ │    │ │- Internal   │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 Diagrama de Casos de Uso

### **Actores y Casos de Uso**

```
┌─────────────────────────────────────────────────────────────┐
│                    Use Case Diagram                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │     Usuario     │    │   Administrador │                │
│  │                 │    │                 │                │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │                │
│  │ │Consultar    │ │    │ │Gestionar    │ │                │
│  │ │Datos        │ │    │ │Sistema      │ │                │
│  │ │             │ │    │ │             │ │                │
│  │ │- Actividades│ │    │ │- Configurar │ │                │
│  │ │- Contratos  │ │    │ │- Monitorear │ │                │
│  │ │- Usuarios   │ │    │ │- Mantener   │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Sistema       │    │   Base de      │                │
│  │   HIDRO Chat    │    │   Datos        │                │
│  │                 │    │                 │                │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │                │
│  │ │Procesar     │ │    │ │Almacenar    │ │                │
│  │ │Consultas    │ │    │ │Datos        │ │                │
│  │ │             │ │    │ │             │ │                │
│  │ │- Entender   │ │◄──►│ │- Activities │ │                │
│  │ │- Generar    │ │    │ │- Contracts  │ │                │
│  │ │- Ejecutar   │ │    │ │- Profiles   │ │                │
│  │ └─────────────┘ │    │ └─────────────┘ │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### **Casos de Uso Detallados**

#### **UC-001: Consultar Actividades**
```
Actor: Usuario
Precondición: Sistema funcionando
Flujo Principal:
1. Usuario escribe "¿Cuántas actividades hay?"
2. Sistema procesa consulta
3. Sistema genera SQL: SELECT COUNT(*) FROM activities
4. Sistema ejecuta consulta
5. Sistema muestra resultado: "515 actividades"
6. Sistema sugiere preguntas relacionadas
Postcondición: Usuario obtiene información
```

#### **UC-002: Visualizar Datos**
```
Actor: Usuario
Precondición: Consulta ejecutada exitosamente
Flujo Principal:
1. Sistema analiza resultados
2. Sistema determina tipo de visualización
3. Sistema formatea datos
4. Sistema renderiza visualización
5. Usuario ve gráfico/tabla/KPI
Postcondición: Datos visualizados
```

#### **UC-003: Manejar Errores**
```
Actor: Sistema
Precondición: Error en procesamiento
Flujo Principal:
1. Sistema detecta error
2. Sistema identifica tipo de error
3. Sistema genera mensaje de error
4. Sistema muestra error al usuario
5. Sistema sugiere acciones correctivas
Postcondición: Error manejado
```

---

## 📈 Diagrama de Actividad

### **Flujo de Procesamiento de Consulta**

```
┌─────────────────────────────────────────────────────────────┐
│                Activity Diagram - Query Processing          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Inicio] ──────────────────────────────────────────────────┐
│     │                                                       │
│     │ Usuario escribe consulta                              │
│     ▼                                                       │
│  [Capturar Input] ──────────────────────────────────────────┐
│     │                                                       │
│     │ Validar input                                         │
│     ▼                                                       │
│  [Validar Input] ───────────────────────────────────────────┐
│     │                                                       │
│     │ Input válido                                          │
│     ▼                                                       │
│  [Enviar a Backend] ────────────────────────────────────────┐
│     │                                                       │
│     │ Procesar con LLM                                      │
│     ▼                                                       │
│  [Procesar con LLM] ────────────────────────────────────────┐
│     │                                                       │
│     │ LLM responde exitosamente                             │
│     ▼                                                       │
│  [Generar SQL] ────────────────────────────────────────────┐
│     │                                                       │
│     │ SQL generado válido                                   │
│     ▼                                                       │
│  [Validar SQL] ────────────────────────────────────────────┐
│     │                                                       │
│     │ SQL válido                                            │
│     ▼                                                       │
│  [Ejecutar Query] ────────────────────────────────────────┐
│     │                                                       │
│     │ Query ejecutado exitosamente                         │
│     ▼                                                       │
│  [Analizar Resultados] ────────────────────────────────────┐
│     │                                                       │
│     │ Tipo de visualización determinado                    │
│     ▼                                                       │
│  [Formatear Datos] ────────────────────────────────────────┐
│     │                                                       │
│     │ Datos formateados                                     │
│     ▼                                                       │
│  [Renderizar Visualización] ────────────────────────────────┐
│     │                                                       │
│     │ Visualización renderizada                            │
│     ▼                                                       │
│  [Mostrar Resultado] ───────────────────────────────────────────┘
│     │                                                       │
│     │ Usuario continúa                                      │
│     ▼                                                       │
│  [Esperar Nueva Consulta] ─────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

---

**¡Diagramas UML completos! 🎉**

Estos diagramas proporcionan una visión completa de la arquitectura, flujos y componentes del sistema HIDRO Chat. ¿Te gustaría que profundice en algún diagrama específico o que agregue más detalles técnicos?


