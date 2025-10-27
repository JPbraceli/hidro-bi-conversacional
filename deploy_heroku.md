# 🚀 DESPLIEGUE EN HEROKU

## 📋 PASOS PARA DESPLEGAR:

### 1. **Preparar el repositorio:**
```bash
# Subir a GitHub
git add .
git commit -m "Preparado para Heroku"
git push origin main
```

### 2. **Crear cuenta en Heroku:**
- Ir a: https://heroku.com
- Crear cuenta gratuita
- Instalar Heroku CLI

### 3. **Crear aplicación:**
```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create tu-app-hidro

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini
```

### 4. **Configurar variables de entorno:**
```bash
# Configurar variables
heroku config:set OLLAMA_HOST=https://tu-ollama-service.com
heroku config:set OLLAMA_MODEL=phi3:mini
heroku config:set DB_TYPE=postgresql
heroku config:set ENABLE_SSL=true
```

### 5. **Deploy:**
```bash
# Deploy
git push heroku main

# Ver logs
heroku logs --tail

# Abrir app
heroku open
```

## 🔧 CONFIGURACIÓN ADICIONAL:

### **Para base de datos PostgreSQL:**
```bash
# Heroku ya incluye PostgreSQL
# Obtener credenciales:
heroku config:get DATABASE_URL

# Conectar a base de datos:
heroku pg:psql
```

### **Para Ollama:**
```bash
# Usar servicio externo
heroku config:set OLLAMA_HOST=https://tu-ollama-service.com
```

## 📊 MONITOREO:
- Logs en tiempo real
- Métricas de rendimiento
- Health checks

## 💰 COSTOS:
- **Gratis:** 550 horas/mes
- **Basic:** $7/mes
- **Standard:** $25/mes

## 🎯 VENTAJAS DE HEROKU:
- ✅ Deploy en 2 minutos
- ✅ Base de datos PostgreSQL incluida
- ✅ SSL automático
- ✅ Monitoreo integrado
- ✅ Rollback fácil
- ✅ Add-ons disponibles

## 🚀 COMANDOS RÁPIDOS:

### **Deploy:**
```bash
git push heroku main
```

### **Ver logs:**
```bash
heroku logs --tail
```

### **Restart:**
```bash
heroku restart
```

### **Configurar variables:**
```bash
heroku config:set VARIABLE=valor
```
