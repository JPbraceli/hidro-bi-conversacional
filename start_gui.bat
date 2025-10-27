@echo off
echo 🚀 INICIANDO INTERFAZ GRÁFICA DE HIDRO
echo =====================================
echo.
echo 📊 Verificando base de datos...
if not exist "hidro_data.db" (
    echo ❌ Base de datos no encontrada: hidro_data.db
    echo 💡 Ejecuta primero: python scripts/fix_sqlite_database.py
    pause
    exit /b 1
)
echo ✅ Base de datos encontrada
echo.
echo 🌐 Iniciando interfaz gráfica...
echo 💡 La interfaz se abrirá en: http://localhost:8501
echo 💡 Presiona Ctrl+C para detener
echo.
streamlit run scripts/create_sqlite_viewer.py --server.port 8501 --server.address localhost
pause
