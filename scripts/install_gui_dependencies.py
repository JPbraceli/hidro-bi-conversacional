#!/usr/bin/env python3
"""
Script para instalar dependencias de la interfaz gráfica
"""
import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def main():
    print("🚀 INSTALANDO DEPENDENCIAS PARA INTERFAZ GRÁFICA")
    print("=" * 60)
    
    # Lista de paquetes necesarios
    packages = [
        "streamlit",
        "plotly",
        "pandas",
        "sqlite3"  # Ya incluido en Python
    ]
    
    print("📦 Instalando paquetes necesarios...")
    
    success_count = 0
    for package in packages:
        if package == "sqlite3":
            print(f"✅ {package} ya incluido en Python")
            success_count += 1
        else:
            if install_package(package):
                success_count += 1
    
    print(f"\n📊 Resumen: {success_count}/{len(packages)} paquetes instalados")
    
    if success_count == len(packages):
        print("\n🎉 ¡Todas las dependencias instaladas correctamente!")
        print("\n🚀 Para ejecutar la interfaz gráfica:")
        print("   streamlit run scripts/create_sqlite_viewer.py")
        print("\n🌐 La interfaz se abrirá en: http://localhost:8501")
    else:
        print("\n⚠️ Algunas dependencias no se pudieron instalar")
        print("💡 Intenta instalar manualmente:")
        for package in packages:
            if package != "sqlite3":
                print(f"   pip install {package}")

if __name__ == "__main__":
    main()
