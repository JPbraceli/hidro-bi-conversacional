# 🚀 DESPLIEGUE EN RENDER

## 📋 PASOS PARA DESPLEGAR:

### 1. **Preparar el repositorio:**
```bash
# Subir a GitHub
git add .
git commit -m "Preparado para Render"
git push origin main
```

### 2. **Crear cuenta en Render:**
- Ir a: https://render.com
- Conectar con GitHub
- Crear "Web Service"

### 3. **Configurar el servicio:**
```
Build Command: pip install -r requirements.txt
Start Command: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. **Variables de entorno:**
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3:mini
DB_TYPE=sqlite
DB_PATH=/opt/render/project/src/data/hidro_data.db
ENABLE_SSL=false
```

### 5. **Base de datos PostgreSQL:**
- Crear "PostgreSQL" service
- Usar las credenciales en variables de entorno

## 🔧 CONFIGURACIÓN ADICIONAL:

### **Para base de datos PostgreSQL:**
```bash
# Crear servicio PostgreSQL en Render
# Variables de entorno:
DB_TYPE=postgresql
DB_HOST=tu-host-postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=tu-password
DB_NAME=hidro_data
```

### **Para Ollama:**
```bash
# Usar servicio externo o instalar en Render
OLLAMA_HOST=https://tu-ollama-service.com
```

## 📊 MONITOREO:
- Logs en tiempo real
- Métricas de rendimiento
- Health checks

## 💰 COSTOS:
- **Gratis:** 750 horas/mes
- **Starter:** $7/mes
- **Standard:** $25/mes

## 🎯 VENTAJAS DE RENDER:
- ✅ Deploy en 3 minutos
- ✅ Base de datos PostgreSQL incluida
- ✅ SSL automático
- ✅ Monitoreo integrado
- ✅ Rollback fácil
