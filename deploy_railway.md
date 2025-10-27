# 🚀 DESPLIEGUE EN RAILWAY

## 📋 PASOS PARA DESPLEGAR:

### 1. **Preparar el repositorio:**
```bash
# Subir a GitHub
git add .
git commit -m "Preparado para Railway"
git push origin main
```

### 2. **Crear cuenta en Railway:**
- Ir a: https://railway.app
- Conectar con GitHub
- Seleccionar el repositorio

### 3. **Configurar variables de entorno:**
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3:mini
DB_TYPE=sqlite
DB_PATH=/app/data/hidro_data.db
ENABLE_SSL=false
```

### 4. **Deploy automático:**
- Railway detectará el Dockerfile
- Desplegará automáticamente
- URL estará disponible en: https://tu-proyecto.railway.app

## 🔧 CONFIGURACIÓN ADICIONAL:

### **Para base de datos PostgreSQL:**
```bash
# En Railway, agregar servicio PostgreSQL
# Cambiar variables:
DB_TYPE=postgresql
DB_HOST=tu-host-postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=tu-password
DB_NAME=hidro_data
```

### **Para Ollama en producción:**
```bash
# Opción 1: Usar servicio externo
OLLAMA_HOST=https://tu-ollama-service.com

# Opción 2: Instalar Ollama en Railway (más complejo)
```

## 📊 MONITOREO:
- Logs en tiempo real
- Métricas de rendimiento
- Escalado automático

## 💰 COSTOS:
- **Gratis:** 500 horas/mes
- **Pro:** $5/mes por servicio
- **Team:** $20/mes por usuario

## 🎯 VENTAJAS DE RAILWAY:
- ✅ Deploy en 2 minutos
- ✅ Base de datos incluida
- ✅ SSL automático
- ✅ Escalado automático
- ✅ Monitoreo integrado
- ✅ Rollback fácil
