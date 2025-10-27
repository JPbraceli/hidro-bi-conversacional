#!/usr/bin/env python3
"""
Análisis simple de los archivos dump
"""
import os

def analyze_dumps():
    """Analizar archivos dump"""
    print("🔍 Analizando archivos dump...")
    
    dumps = [
        'dev_hdcr_activities.dump',
        'dev_hdcr_admin.dump',
        'dev_hdcr_contracts.dump',
        'dev_hdcr_gateway.dump',
        'dev_hdcr_profile.dump'
    ]
    
    total_size = 0
    
    for dump_file in dumps:
        if os.path.exists(dump_file):
            size = os.path.getsize(dump_file)
            total_size += size
            print(f"📄 {dump_file}: {size:,} bytes ({size/1024/1024:.2f} MB)")
            
            # Intentar leer primeras líneas
            try:
                with open(dump_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[:10]
                    print(f"  📋 Primeras líneas:")
                    for i, line in enumerate(lines):
                        if line.strip():
                            print(f"    {i+1}: {line.strip()[:80]}...")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        else:
            print(f"❌ {dump_file} no encontrado")
    
    print(f"\n📊 Total: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
    analyze_dumps()




