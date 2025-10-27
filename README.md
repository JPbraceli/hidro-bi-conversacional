# 🚀 HIDRO Chat - Asistente de Business Intelligence

Sistema de chat inteligente para consultas de base de datos con visualizaciones automáticas, similar a Amazon QuickSight o ChatGPT.

## 📋 Requisitos Previos

### 1. **PostgreSQL** (Base de datos)
- **Host:** 127.0.0.1
- **Puerto:** 15433
- **Usuario:** hdcruser
- **Contraseña:** localpass
- **Bases disponibles:** dev_hdcr_activities, dev_hdcr_profile, dev_hdcr_contracts, dev_hdcr_gateway, dev_hdcr_admin

### 2. **Ollama** (LLM Local)
- Descargar e instalar desde: https://ollama.ai/
- Modelo requerido: `phi3:mini`

### 3. **Python 3.8+**
- Para el backend FastAPI

### 4. **Node.js 16+**
- Para el frontend React

## 🛠️ Instalación y Configuración

### 1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd hidronuevo
```

### 2. **Instalar dependencias del backend**
```bash
cd backend
pip install -r requirements-simple.txt
```

### 3. **Instalar dependencias del frontend**
```bash
cd frontend
npm install
```

### 4. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp backend/env.example backend/.env

# Editar .env con tus configuraciones
# Las configuraciones por defecto ya están correctas para tu setup
```

## 🚀 Levantar el Sistema

### **Opción 1: Comando único (Recomendado)**
```bash
# Desde la raíz del proyecto
npm run dev
```

### **Opción 2: Comandos separados**

#### **Terminal 1: Backend**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### **Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```

#### **Terminal 3: Ollama (LLM)**
```bash
ollama serve
```

## 🔧 Configuración de Base de Datos

### **Importar dumps (Opcional)**
Si tienes archivos `.dump` para importar:

```bash
# Configurar contraseña automática
export PGPASSWORD=localpass

# Importar dumps
psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_activities.dump
psql -h 127.0.0.1 -p 15433 -U hdcruser -d hidro -f dev_hdcr_admin.dump
# ... repetir para cada dump
```

### **O usar el script automático:**
```bash
python scripts/import_dumps_with_password.py
```

## 🌐 URLs de Acceso

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **Ollama:** http://localhost:11434

## 🎯 Características

- **Chat inteligente** con respuestas automáticas
- **Visualizaciones automáticas** (tablas, gráficos, KPIs)
- **Ejecución automática de consultas SQL**
- **Interfaz full-screen** similar a ChatGPT
- **Sugerencias inteligentes** para consultas
- **Respuestas en español**

## 🔍 Verificar que Todo Funciona

### **1. Verificar Ollama:**
```bash
ollama list
# Debe mostrar: phi3:mini
```

### **2. Verificar Backend:**
```bash
curl http://localhost:8001/health
# Debe responder: {"status": "ok"}
```

### **3. Verificar Base de Datos:**
```bash
python scripts/check_current_setup.py
```

## 🐛 Solución de Problemas

### **Error: "ModuleNotFoundError: No module named 'ollama'"**
```bash
cd backend
pip install -r requirements-simple.txt
```

### **Error: "ollama: connection refused"**
```bash
# Asegúrate de que Ollama esté corriendo
ollama serve
```

### **Error: "password authentication failed"**
```bash
# Verificar credenciales en backend/app/dependencies.py
# Usuario: hdcruser
# Contraseña: localpass
```

### **Error: "Port 8000 already in use"**
```bash
# El sistema usa puerto 8001, no 8000
# Si hay conflicto, cambiar en vite.config.js
```

## 📁 Estructura del Proyecto

```
hidronuevo/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── dependencies.py  # Configuración BD y Ollama
│   │   ├── llm/           # Motor de LLM
│   │   ├── routers/       # Endpoints API
│   │   └── utils/         # Utilidades
│   └── requirements-simple.txt
├── frontend/               # React + Vite
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   └── App.jsx        # App principal
│   └── package.json
├── scripts/                # Scripts de utilidad
└── docs/                   # Documentación
```

## 🎨 Personalización

### **Cambiar modelo de LLM:**
Editar `backend/app/dependencies.py`:
```python
ollama_model: str = "phi3:mini"  # Cambiar por otro modelo
```

### **Cambiar base de datos:**
Editar `backend/app/dependencies.py`:
```python
db_name: str = "dev_hdcr_activities"  # Cambiar por otra base
```

## 📞 Soporte

Si tienes problemas:

1. **Verificar logs** en cada terminal
2. **Revisar configuración** en `backend/app/dependencies.py`
3. **Probar conexiones** con los scripts en `scripts/`
4. **Revisar documentación** en `docs/`

## 🚀 Comandos Rápidos

```bash
# Instalar todo
npm run install-all

# Levantar todo
npm run dev

# Solo backend
npm run backend

# Solo frontend
npm run frontend

# Probar conexión
npm run test-connection
```

---

**¡Listo! 🎉 Tu asistente de BI está funcionando.**



