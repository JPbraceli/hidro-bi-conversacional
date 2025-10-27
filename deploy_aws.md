# 🚀 DESPLIEGUE EN AWS

## 📋 PASOS PARA DESPLEGAR:

### 1. **Preparar el repositorio:**
```bash
# Subir a GitHub
git add .
git commit -m "Preparado para AWS"
git push origin main
```

### 2. **Crear cuenta en AWS:**
- Ir a: https://aws.amazon.com
- Crear cuenta
- Configurar AWS CLI

### 3. **Crear instancia EC2:**
```bash
# Crear instancia t3.micro (gratis)
# Ubuntu 22.04 LTS
# Security Group: HTTP (80), HTTPS (443), SSH (22)

# Conectar a instancia
ssh -i tu-key.pem ubuntu@tu-ip-ec2

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip nginx git

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
sudo cat > /etc/nginx/sites-available/hidro << EOF
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
sudo ln -s /etc/nginx/sites-available/hidro /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. **Configurar SSL:**
```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com
```

## 🔧 CONFIGURACIÓN ADICIONAL:

### **Para base de datos RDS:**
```bash
# Crear instancia RDS PostgreSQL
# Configurar Security Group
# Obtener endpoint de base de datos

# Variables de entorno
export DB_TYPE=postgresql
export DB_HOST=tu-rds-endpoint
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=tu-password
export DB_NAME=hidro_data
```

### **Para Ollama:**
```bash
# Ollama ya está instalado
# Configurar variables de entorno
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=phi3:mini
```

## 📊 MONITOREO:
- CloudWatch logs
- Métricas de rendimiento
- Health checks

## 💰 COSTOS:
- **EC2 t3.micro:** Gratis (12 meses)
- **RDS t3.micro:** Gratis (12 meses)
- **Route 53:** $0.50/mes
- **Total:** ~$1/mes después del primer año

## 🎯 VENTAJAS DE AWS:
- ✅ Control total del servidor
- ✅ Base de datos RDS PostgreSQL
- ✅ SSL automático
- ✅ Monitoreo avanzado
- ✅ Escalado automático
- ✅ Backup automático
- ✅ CDN con CloudFront

## 🚀 COMANDOS RÁPIDOS:

### **Deploy:**
```bash
git pull origin main
sudo systemctl restart hidro
```

### **Ver logs:**
```bash
sudo journalctl -u hidro -f
```

### **Restart:**
```bash
sudo systemctl restart hidro
```

### **Configurar servicio:**
```bash
# Crear servicio systemd
sudo cat > /etc/systemd/system/hidro.service << EOF
[Unit]
Description=Hidro App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/hidronuevo
ExecStart=/usr/bin/python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable hidro
sudo systemctl start hidro
```
