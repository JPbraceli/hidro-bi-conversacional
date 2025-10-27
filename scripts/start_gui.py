#!/usr/bin/env python3
"""
Script para iniciar la interfaz gráfica de SQLite
"""
import subprocess
import sys
import os

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    try:
        import streamlit
        import plotly
        import pandas
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        return False

def check_database():
    """Verificar que la base de datos exista"""
    if os.path.exists("hidro_data.db"):
        print("✅ Base de datos encontrada: hidro_data.db")
        return True
    else:
        print("❌ Base de datos no encontrada: hidro_data.db")
        print("💡 Ejecuta primero: python scripts/fix_sqlite_database.py")
        return False

def start_streamlit():
    """Iniciar la aplicación Streamlit"""
    try:
        print("🚀 Iniciando interfaz gráfica...")
        print("🌐 La interfaz se abrirá en: http://localhost:8501")
        print("💡 Presiona Ctrl+C para detener")
        
        # Ejecutar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "scripts/create_sqlite_viewer.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Interfaz gráfica detenida")
    except Exception as e:
        print(f"❌ Error iniciando interfaz: {e}")

def main():
    print("🔍 INICIANDO INTERFAZ GRÁFICA DE SQLite")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n💡 Instala las dependencias primero:")
        print("   python scripts/install_gui_dependencies.py")
        return
    
    # Verificar base de datos
    if not check_database():
        return
    
    # Iniciar interfaz
    start_streamlit()

if __name__ == "__main__":
    main()
