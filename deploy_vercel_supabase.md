# 🚀 DESPLIEGUE EN VERCEL + SUPABASE

## 📋 PASOS PARA DESPLEGAR:

### 1. **Preparar el repositorio:**
```bash
# Subir a GitHub
git add .
git commit -m "Preparado para Vercel + Supabase"
git push origin main
```

### 2. **Crear cuenta en Supabase:**
- Ir a: https://supabase.com
- Crear nuevo proyecto
- Obtener credenciales de base de datos

### 3. **Crear cuenta en Vercel:**
- Ir a: https://vercel.com
- Conectar con GitHub
- Importar proyecto

### 4. **Configurar variables de entorno en Vercel:**
```
OLLAMA_HOST=https://tu-ollama-service.com
OLLAMA_MODEL=phi3:mini
DB_TYPE=postgresql
DB_HOST=tu-host-supabase
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=tu-password
DB_NAME=postgres
ENABLE_SSL=true
```

### 5. **Configurar base de datos en Supabase:**
```sql
-- Crear tablas
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    amount DECIMAL(10,2),
    vigente BOOLEAN,
    anio_campania INTEGER,
    code VARCHAR(50),
    id_contract INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insertar datos de prueba
INSERT INTO activities (name, start_date, end_date, amount, vigente, anio_campania, code, id_contract) VALUES
('Proyecto A', '2023-01-01', '2023-12-31', 100000, true, 2023, 'PROJ-A', 1),
('Proyecto B', '2023-06-01', '2024-05-31', 150000, true, 2023, 'PROJ-B', 2);
```

## 🔧 CONFIGURACIÓN ADICIONAL:

### **Para Ollama en producción:**
```bash
# Opción 1: Usar servicio externo
OLLAMA_HOST=https://tu-ollama-service.com

# Opción 2: Usar Replicate API
OLLAMA_HOST=https://api.replicate.com
```

### **Para base de datos:**
```bash
# Usar Supabase PostgreSQL
# Configurar RLS (Row Level Security)
# Configurar políticas de acceso
```

## 📊 MONITOREO:
- Logs en Vercel
- Métricas en Supabase
- Health checks automáticos

## 💰 COSTOS:
- **Vercel:** Gratis (hobby) / $20/mes (pro)
- **Supabase:** Gratis (hobby) / $25/mes (pro)

## 🎯 VENTAJAS DE VERCEL + SUPABASE:
- ✅ Deploy en 1 minuto
- ✅ Base de datos PostgreSQL real
- ✅ SSL automático
- ✅ CDN global
- ✅ Escalado automático
- ✅ Monitoreo avanzado

## 🚀 COMANDOS RÁPIDOS:

### **Deploy a Vercel:**
```bash
npm install -g vercel
vercel --prod
```

### **Deploy a Supabase:**
```bash
npm install -g supabase
supabase db push
```
