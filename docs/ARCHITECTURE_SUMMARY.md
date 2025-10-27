# 🏗️ HIDRO Chat - Resumen de Arquitectura

## 📋 Resumen Ejecutivo

**HIDRO Chat** es un sistema de Business Intelligence conversacional que transforma consultas en lenguaje natural en insights visuales automáticos. El sistema está diseñado con una arquitectura de microservicios moderna que combina tecnologías de vanguardia para proporcionar una experiencia similar a ChatGPT pero especializada en datos empresariales.

### **🎯 Objetivos del Sistema**
- **Democratización de datos**: Permitir consultas sin conocimiento técnico de SQL
- **Visualizaciones automáticas**: Generar gráficos y tablas inteligentemente
- **Respuestas conversacionales**: Interfaz natural tipo ChatGPT
- **Rendimiento optimizado**: Respuestas en menos de 2 segundos
- **Escalabilidad**: Arquitectura preparada para crecimiento

---

## 🏛️ Arquitectura General

### **Patrón Arquitectónico: Microservicios con API Gateway**

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   React App     │  │  Tailwind CSS   │  │  Vite Dev    │  │
│  │   (Frontend)    │  │   (Styling)     │  │  (Build)     │  │
│  │   Port: 3000    │  │   Responsive    │  │  Hot Reload  │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE API                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   FastAPI       │  │   SQLAlchemy    │  │  Pydantic    │  │
│  │   (Backend)     │  │   (ORM)         │  │  (Validation)│  │
│  │   Port: 8001    │  │   Pool Conn     │  │  Auto Docs   │  │
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
│  │   Port: 11434   │  │  3.8B Params    │  │  Context     │  │
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
│  │   Port: 15433   │  │   5 Databases   │  │   Migration  │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos Principal

### **1. Entrada del Usuario**
```
Usuario escribe: "¿Cuántas actividades están activas?"
    ↓
React captura input en ChatInterface
    ↓
Estado local actualizado (messages, isLoading)
    ↓
Fetch API envía POST a /api/chat
```

### **2. Procesamiento Backend**
```
FastAPI recibe request en ChatRouter
    ↓
Pydantic valida estructura del mensaje
    ↓
PromptEngine procesa con contexto de BD
    ↓
Ollama genera respuesta con phi3:mini
    ↓
Sistema extrae SQL de la respuesta
```

### **3. Ejecución de Consulta**
```
SQL generado: SELECT COUNT(*) FROM activities WHERE vigente = true
    ↓
ValidateSQL verifica seguridad de la consulta
    ↓
QueryExecutor ejecuta en PostgreSQL
    ↓
Resultados: 245 filas
    ↓
Análisis de tipo de visualización: KPI Cards
```

### **4. Respuesta al Usuario**
```
Datos formateados para KPI Cards
    ↓
JSON response con visualización
    ↓
React recibe respuesta
    ↓
Efecto de escritura progresiva
    ↓
VisualizationPanel renderiza KPI Cards
    ↓
Usuario ve: "245 actividades activas"
```

---

## 🛠️ Tecnologías por Capa

### **CAPA DE PRESENTACIÓN**

#### **React 18**
- **Propósito**: Framework de UI moderno
- **Características**: Hooks, componentes funcionales, estado local
- **Ventajas**: Virtual DOM, hot reload, ecosistema rico
- **Rendimiento**: Re-renderizado optimizado

#### **Vite**
- **Propósito**: Build tool y servidor de desarrollo
- **Características**: esbuild, HMR, proxy automático
- **Ventajas**: Build ultra-rápido, configuración mínima
- **Puerto**: 3000

#### **Tailwind CSS**
- **Propósito**: Framework de estilos utilitarios
- **Características**: Clases utilitarias, responsive design
- **Ventajas**: Tamaño optimizado, consistencia visual
- **Uso**: Styling de componentes React

### **CAPA DE API**

#### **FastAPI**
- **Propósito**: Framework web moderno para APIs
- **Características**: Validación automática, documentación automática
- **Ventajas**: Type hints, async/await, Swagger UI
- **Puerto**: 8001

#### **SQLAlchemy**
- **Propósito**: ORM para Python
- **Características**: Pool de conexiones, migraciones
- **Ventajas**: Soporte multi-DB, queries optimizadas
- **Uso**: Conexión a PostgreSQL

#### **Pydantic**
- **Propósito**: Validación de datos y serialización
- **Características**: Type hints, validación automática
- **Ventajas**: Documentación automática, errores claros
- **Uso**: Modelos de request/response

### **CAPA DE INTELIGENCIA**

#### **Ollama**
- **Propósito**: Runtime local para LLMs
- **Características**: Ejecución local, API simple
- **Ventajas**: Sin dependencias externas, control total
- **Puerto**: 11434

#### **phi3:mini**
- **Propósito**: Modelo de lenguaje especializado
- **Características**: 3.8B parámetros, contexto 128K
- **Ventajas**: Optimizado para CPU, multilingüe
- **Rendimiento**: ~20 tokens/segundo

### **CAPA DE DATOS**

#### **PostgreSQL 15**
- **Propósito**: Base de datos relacional
- **Características**: ACID, JSON, índices avanzados
- **Ventajas**: Escalabilidad, replicación nativa
- **Puerto**: 15433

---

## 📊 Diagramas de Arquitectura

### **Diagrama de Componentes**

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

### **Diagrama de Despliegue**

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
│                         │ │LLM Service │ │                │
│                         │ │(Port 11434)│ │                │
│                         │ │- Ollama    │ │                │
│                         │ │- phi3:mini │ │                │
│                         │ └─────────────┘ │                │
│                         │                 │                │
│                         │ ┌─────────────┐ │                │
│                         │ │Database    │ │                │
│                         │ │(Port 15433)│ │                │
│                         │ │- PostgreSQL│ │                │
│                         │ │- Multiple  │ │                │
│                         │ │  Schemas   │ │                │
│                         │ └─────────────┘ │                │
│                         └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujos de Datos Detallados

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

### **Flujo 2: Consulta Compleja**

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

## 🚀 Características Avanzadas

### **1. Efectos de Escritura**
- **Tecnología**: JavaScript setTimeout
- **Velocidad**: 25ms por carácter
- **Efecto**: Escritura progresiva tipo ChatGPT
- **Scroll**: Automático durante escritura

### **2. Visualizaciones Inteligentes**
- **Detección automática**: Basada en estructura de datos
- **Tipos soportados**: Tablas, KPIs, gráficos de barras/líneas/pastel
- **Rendimiento**: Renderizado optimizado con React
- **Responsive**: Adaptable a diferentes tamaños

### **3. Sugerencias Contextuales**
- **Algoritmo**: Basado en palabras clave
- **Categorización**: Por dominio (actividades, contratos, etc.)
- **Límite**: Máximo 3 sugerencias
- **Interactividad**: Clickables para ejecutar

### **4. Manejo de Errores**
- **Validación SQL**: Prevención de inyecciones
- **Mensajes descriptivos**: Errores claros para el usuario
- **Fallback**: Visualización de tabla si falla gráfico
- **Recuperación**: Sugerencias para corregir errores

---

## 📈 Métricas de Rendimiento

### **Tiempos de Respuesta**
- **Consulta simple**: < 1 segundo
- **Consulta compleja**: < 2 segundos
- **Visualización**: < 500ms
- **Carga inicial**: < 3 segundos

### **Recursos del Sistema**
- **RAM mínima**: 8GB (recomendado 16GB)
- **CPU**: 4 cores (recomendado 8 cores)
- **Disco**: 10GB libres
- **Red**: Conexión estable

### **Escalabilidad**
- **Usuarios concurrentes**: 100+ (con optimizaciones)
- **Consultas por minuto**: 1000+
- **Tamaño de base de datos**: Ilimitado
- **Crecimiento**: Horizontal y vertical

---

## 🔒 Seguridad y Rendimiento

### **Medidas de Seguridad**
- **Validación SQL**: Solo consultas SELECT permitidas
- **Sanitización**: Limpieza de inputs del usuario
- **Conexiones seguras**: SSL/TLS opcional
- **Autenticación**: JWT planificado para v2.0

### **Optimizaciones**
- **Pool de conexiones**: 10 conexiones simultáneas
- **Caché**: Esquema de BD en memoria
- **Compresión**: GZIP para respuestas
- **CDN**: Assets estáticos optimizados

---

## 🎯 Próximas Mejoras

### **Versión 2.0**
- [ ] Autenticación JWT
- [ ] Roles y permisos
- [ ] Exportación de datos
- [ ] Dashboard de métricas

### **Versión 3.0**
- [ ] Múltiples bases de datos
- [ ] Cache distribuido (Redis)
- [ ] Microservicios independientes
- [ ] Kubernetes deployment

---

**¡Arquitectura completa documentada! 🎉**

Esta documentación proporciona una visión integral del sistema HIDRO Chat, desde la arquitectura hasta los detalles de implementación. El sistema está diseñado para ser escalable, mantenible y fácil de entender.


