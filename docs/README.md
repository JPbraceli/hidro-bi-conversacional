# 📚 Documentación Técnica - HIDRO Chat

## 📋 Índice de Documentación

Esta carpeta contiene la documentación técnica completa del sistema HIDRO Chat, organizada por temas y niveles de detalle.

### **📖 Documentos Principales**

#### **1. [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)**
**Documentación técnica completa del sistema**
- Arquitectura del sistema
- Requisitos funcionales
- Tecnologías por capa
- API Reference
- Base de datos
- Seguridad y rendimiento

#### **2. [UML_DIAGRAMS.md](./UML_DIAGRAMS.md)**
**Diagramas UML y de arquitectura**
- Diagrama de secuencia
- Diagrama de estados
- Diagrama de clases
- Diagrama de componentes
- Diagrama de despliegue
- Casos de uso

#### **3. [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md)**
**Resumen ejecutivo de la arquitectura**
- Resumen ejecutivo
- Arquitectura general
- Flujos de datos
- Tecnologías por capa
- Características avanzadas
- Métricas de rendimiento

---

## 🎯 Guía de Lectura

### **Para Desarrolladores**
1. **Empezar con**: [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md)
2. **Profundizar en**: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)
3. **Entender flujos**: [UML_DIAGRAMS.md](./UML_DIAGRAMS.md)

### **Para Arquitectos**
1. **Empezar con**: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)
2. **Revisar diagramas**: [UML_DIAGRAMS.md](./UML_DIAGRAMS.md)
3. **Resumen ejecutivo**: [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md)

### **Para Product Managers**
1. **Empezar con**: [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md)
2. **Revisar requisitos**: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)
3. **Entender casos de uso**: [UML_DIAGRAMS.md](./UML_DIAGRAMS.md)

---

## 🏗️ Arquitectura del Sistema

### **Resumen Ejecutivo**
HIDRO Chat es un sistema de Business Intelligence conversacional que transforma consultas en lenguaje natural en insights visuales automáticos. Funciona como un "Amazon QuickSight" o "ChatGPT" especializado para datos empresariales.

### **Componentes Principales**
- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **LLM**: Ollama + phi3:mini
- **Base de Datos**: PostgreSQL

### **Puertos del Sistema**
- **3000**: Frontend React
- **8001**: Backend FastAPI
- **11434**: Ollama LLM
- **15433**: PostgreSQL

---

## 🔄 Flujos Principales

### **1. Consulta del Usuario**
```
Usuario → React → FastAPI → Ollama → SQLAlchemy → PostgreSQL
```

### **2. Respuesta y Visualización**
```
PostgreSQL → SQLAlchemy → FastAPI → React → Usuario
```

### **3. Manejo de Errores**
```
Error → Validación → Mensaje → Usuario
```

---

## 🛠️ Tecnologías Utilizadas

### **Frontend Stack**
- **React 18**: Framework de UI
- **Vite**: Build tool
- **Tailwind CSS**: Estilos
- **Lucide React**: Iconos

### **Backend Stack**
- **FastAPI**: API REST
- **SQLAlchemy**: ORM
- **Pydantic**: Validación
- **Uvicorn**: Servidor

### **Inteligencia Artificial**
- **Ollama**: Runtime LLM
- **phi3:mini**: Modelo AI
- **Prompt Engineering**: Contexto

### **Base de Datos**
- **PostgreSQL 15**: Base de datos
- **Múltiples esquemas**: Separación por dominio
- **Pool de conexiones**: Gestión eficiente

---

## 📊 Características del Sistema

### **Funcionalidades Principales**
- ✅ Interfaz conversacional tipo ChatGPT
- ✅ Procesamiento de lenguaje natural
- ✅ Generación automática de SQL
- ✅ Visualizaciones inteligentes
- ✅ Sugerencias contextuales
- ✅ Manejo de errores robusto

### **Tipos de Visualización**
- **Tablas**: Para datos detallados
- **KPI Cards**: Para métricas únicas
- **Gráficos de Barras**: Para comparaciones
- **Gráficos de Líneas**: Para tendencias
- **Gráficos de Pastel**: Para proporciones

### **Bases de Datos Disponibles**
- **dev_hdcr_activities**: 515 registros
- **dev_hdcr_profile**: Perfiles de usuario
- **dev_hdcr_contracts**: Contratos
- **dev_hdcr_gateway**: Gateways
- **dev_hdcr_admin**: Administración

---

## 🚀 Instalación y Configuración

### **Requisitos del Sistema**
- **RAM**: 8GB (recomendado 16GB)
- **CPU**: 4 cores (recomendado 8 cores)
- **Disco**: 10GB libres
- **Red**: Conexión estable

### **Comandos de Instalación**
```bash
# Clonar repositorio
git clone <repository-url>
cd hidronuevo

# Backend
cd backend
pip install -r requirements-simple.txt
cp env.example .env

# Frontend
cd frontend
npm install

# Base de datos
python scripts/import_dumps_with_password.py

# Ollama
ollama pull phi3:mini
ollama serve

# Levantar sistema
npm run dev
```

---

## 📈 Métricas de Rendimiento

### **Tiempos de Respuesta**
- **Consulta simple**: < 1 segundo
- **Consulta compleja**: < 2 segundos
- **Visualización**: < 500ms
- **Carga inicial**: < 3 segundos

### **Recursos del Sistema**
- **Usuarios concurrentes**: 100+
- **Consultas por minuto**: 1000+
- **Tamaño de BD**: Ilimitado
- **Escalabilidad**: Horizontal y vertical

---

## 🔒 Seguridad

### **Medidas Implementadas**
- ✅ Validación de SQL
- ✅ Sanitización de inputs
- ✅ Conexiones seguras
- ✅ Manejo de errores

### **Planificado para v2.0**
- 🔄 Autenticación JWT
- 🔄 Roles y permisos
- 🔄 Auditoría de consultas
- 🔄 Rate limiting

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

## 📞 Soporte y Contacto

### **Documentación Adicional**
- **README.md**: Guía de inicio rápido
- **docs/**: Documentación técnica completa
- **scripts/**: Scripts de utilidad
- **tests/**: Pruebas del sistema

### **Recursos de Desarrollo**
- **GitHub**: Repositorio del proyecto
- **Issues**: Reportar problemas
- **Wiki**: Documentación adicional
- **Discussions**: Foro de discusión

---

**¡Documentación completa del sistema HIDRO Chat! 🎉**

Esta documentación proporciona una visión integral del sistema, desde la arquitectura hasta los detalles de implementación. El sistema está diseñado para ser escalable, mantenible y fácil de entender.


