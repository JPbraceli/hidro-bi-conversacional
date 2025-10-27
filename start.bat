@echo off
echo 🚀 Iniciando HidroChat...
echo.

echo 📦 Instalando dependencias del backend...
cd backend
pip install -r requirements-simple.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias del backend
    pause
    exit /b 1
)

echo.
echo 📦 Instalando dependencias del frontend...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ❌ Error instalando dependencias del frontend
    pause
    exit /b 1
)

echo.
echo 🎯 Iniciando ambos servicios...
cd ..
npm run dev





