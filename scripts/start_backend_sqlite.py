#!/usr/bin/env python3
"""
Script para iniciar el backend con SQLite
"""
import subprocess
import sys
import os
import time

def check_sqlite_database():
    """Verificar que la base de datos SQLite exista"""
    db_path = "hidro_data.db"
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        print("💡 Ejecuta primero: python scripts/fix_sqlite_database.py")
        return False
    print(f"✅ Base de datos encontrada: {db_path}")
    return True

def check_ollama():
    """Verificar si Ollama está ejecutándose"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            print("✅ Ollama está ejecutándose")
            return True
    except:
        pass
    
    print("⚠️ Ollama no está ejecutándose")
    print("💡 Para iniciar Ollama:")
    print("   1. Descarga Ollama desde: https://ollama.ai/download")
    print("   2. Instala y ejecuta: ollama serve")
    print("   3. Descarga el modelo: ollama pull phi3:mini")
    return False

def start_backend():
    """Iniciar el backend"""
    print("🚀 INICIANDO BACKEND HIDRO CON SQLite")
    print("=" * 50)
    
    # Verificar base de datos
    if not check_sqlite_database():
        return False
    
    # Verificar Ollama
    ollama_ok = check_ollama()
    
    if not ollama_ok:
        print("\n⚠️ ADVERTENCIA: Ollama no está disponible")
        print("💡 El chat funcionará pero sin capacidades de IA")
        print("💡 Para habilitar IA, inicia Ollama primero")
        
        response = input("\n¿Continuar sin Ollama? (y/n): ").lower()
        if response != 'y':
            print("❌ Cancelado por el usuario")
            return False
    
    # Cambiar al directorio backend
    backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
    os.chdir(backend_dir)
    
    print(f"\n📁 Directorio backend: {os.getcwd()}")
    print("🚀 Iniciando servidor FastAPI...")
    print("🌐 URL: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("💡 Presiona Ctrl+C para detener")
    
    try:
        # Ejecutar uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Backend detenido")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔧 CONFIGURACIÓN DEL BACKEND HIDRO")
    print("=" * 60)
    
    start_backend()

if __name__ == "__main__":
    main()
