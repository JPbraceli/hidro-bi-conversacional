# 🚀 DESPLIEGUE EN DIGITALOCEAN

## 📋 PASOS PARA DESPLEGAR:

### 1. **Preparar el repositorio:**
```bash
# Subir a GitHub
git add .
git commit -m "Preparado para DigitalOcean"
git push origin main
```

### 2. **Crear cuenta en DigitalOcean:**
- Ir a: https://digitalocean.com
- Crear cuenta
- Crear Droplet (Ubuntu 22.04)

### 3. **Configurar servidor:**
```bash
# Conectar al servidor
ssh root@tu-ip-servidor

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3 python3-pip nginx git

# Clonar repositorio
git clone https://github.com/tu-usuario/hidronuevo.git
cd hidronuevo

# Instalar dependencias Python
pip3 install -r requirements.txt

# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull phi3:mini
```

### 4. **Configurar Nginx:**
```bash
# Crear configuración Nginx
cat > /etc/nginx/sites-available/hidro << EOF
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Habilitar sitio
ln -s /etc/nginx/sites-available/hidro /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 5. **Configurar SSL:**
```bash
# Instalar Certbot
apt install -y certbot python3-certbot-nginx

# Obtener certificado SSL
certbot --nginx -d tu-dominio.com
```

## 🔧 CONFIGURACIÓN ADICIONAL:

### **Para base de datos PostgreSQL:**
```bash
# Instalar PostgreSQL
apt install -y postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb hidro_data
sudo -u postgres psql -c "CREATE USER hidro_user WITH PASSWORD 'tu-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE hidro_data TO hidro_user;"
```

### **Para Ollama:**
```bash
# Ollama ya está instalado
# Configurar variables de entorno
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=phi3:mini
```

## 📊 MONITOREO:
- Logs del sistema
- Métricas de rendimiento
- Health checks

## 💰 COSTOS:
- **Basic:** $6/mes (1GB RAM)
- **Standard:** $12/mes (2GB RAM)
- **Professional:** $24/mes (4GB RAM)

## 🎯 VENTAJAS DE DIGITALOCEAN:
- ✅ Control total del servidor
- ✅ Base de datos PostgreSQL
- ✅ SSL automático
- ✅ Monitoreo avanzado
- ✅ Escalado manual
- ✅ Backup automático

## 🚀 COMANDOS RÁPIDOS:

### **Deploy:**
```bash
git pull origin main
systemctl restart hidro
```

### **Ver logs:**
```bash
journalctl -u hidro -f
```

### **Restart:**
```bash
systemctl restart hidro
```

### **Configurar servicio:**
```bash
# Crear servicio systemd
cat > /etc/systemd/system/hidro.service << EOF
[Unit]
Description=Hidro App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/hidronuevo
ExecStart=/usr/bin/python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable hidro
systemctl start hidro
```
