#!/usr/bin/env python3
"""
Script para corregir y verificar la base de datos SQLite
"""
import sqlite3
import os

def fix_database():
    """Corregir base de datos SQLite"""
    db_name = "hidro_data.db"
    
    # Eliminar base anterior si existe
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"🗑️ Base anterior eliminada: {db_name}")
    
    # Crear nueva base
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    print("🔍 Creando estructura corregida...")
    
    # Tabla de actividades (corregida)
    cursor.execute('''
        CREATE TABLE activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            amount REAL,
            vigente BOOLEAN DEFAULT 1,
            anio_campania INTEGER,
            code TEXT,
            id_contract INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de perfiles
    cursor.execute('''
        CREATE TABLE profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            role TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de contratos
    cursor.execute('''
        CREATE TABLE contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_number TEXT UNIQUE NOT NULL,
            company TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            value REAL,
            status TEXT DEFAULT 'activo',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de gateways
    cursor.execute('''
        CREATE TABLE gateways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            status TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de admin_users
    cursor.execute('''
        CREATE TABLE admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("✅ Estructura corregida")
    
    # Insertar datos de ejemplo
    print("📊 Insertando datos de ejemplo...")
    
    # Actividades
    activities = [
        ('Perforación Pozo Norte-001', '2024-01-15', '2024-03-15', 1500000.00, 1, 2024, 'ACT-001', 1),
        ('Fractura Hidráulica Sur-002', '2024-02-01', '2024-02-28', 800000.00, 1, 2024, 'ACT-002', 2),
        ('Mantenimiento Gateway Este', '2024-01-20', '2024-01-25', 50000.00, 1, 2024, 'ACT-003', 3),
        ('Análisis de Producción', '2024-03-01', '2024-03-31', 200000.00, 1, 2024, 'ACT-004', 1),
        ('Instalación Sensores IoT', '2024-02-15', '2024-04-15', 300000.00, 1, 2024, 'ACT-005', 2)
    ]
    
    for activity in activities:
        cursor.execute('''
            INSERT INTO activities (name, start_date, end_date, amount, vigente, anio_campania, code, id_contract)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', activity)
    
    # Perfiles
    profiles = [
        (1, 'Juan Carlos', 'Pérez', 'juan.perez@hidro.com', 'Ingeniero Senior'),
        (2, 'María Elena', 'González', 'maria.gonzalez@hidro.com', 'Analista de Datos'),
        (3, 'Carlos Alberto', 'Rodríguez', 'carlos.rodriguez@hidro.com', 'Supervisor de Campo'),
        (4, 'Ana Patricia', 'Martínez', 'ana.martinez@hidro.com', 'Técnico Especialista'),
        (5, 'Luis Fernando', 'Fernández', 'luis.fernandez@hidro.com', 'Operador Senior')
    ]
    
    for profile in profiles:
        cursor.execute('''
            INSERT INTO profiles (user_id, first_name, last_name, email, role)
            VALUES (?, ?, ?, ?, ?)
        ''', profile)
    
    # Contratos
    contracts = [
        ('CT-2024-001', 'PetroEnergy Corp', '2024-01-01', '2024-12-31', 5000000.00, 'activo'),
        ('CT-2024-002', 'OilMax Industries', '2024-02-01', '2025-01-31', 7500000.00, 'activo'),
        ('CT-2024-003', 'DrillTech Solutions', '2024-03-01', '2024-11-30', 3200000.00, 'activo')
    ]
    
    for contract in contracts:
        cursor.execute('''
            INSERT INTO contracts (contract_number, company, start_date, end_date, value, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', contract)
    
    # Gateways
    gateways = [
        ('Gateway Norte-01', 'Campo Norte', 'activo'),
        ('Gateway Sur-02', 'Campo Sur', 'activo'),
        ('Gateway Este-03', 'Campo Este', 'mantenimiento'),
        ('Gateway Oeste-04', 'Campo Oeste', 'activo'),
        ('Gateway Central-05', 'Oficina Central', 'activo')
    ]
    
    for gateway in gateways:
        cursor.execute('''
            INSERT INTO gateways (name, location, status)
            VALUES (?, ?, ?)
        ''', gateway)
    
    # Admin users
    admin_users = [
        ('admin1', 'admin1@hidro.com', 'super_admin'),
        ('admin2', 'admin2@hidro.com', 'admin'),
        ('admin3', 'admin3@hidro.com', 'admin')
    ]
    
    for admin in admin_users:
        cursor.execute('''
            INSERT INTO admin_users (username, email, role)
            VALUES (?, ?, ?)
        ''', admin)
    
    conn.commit()
    print("✅ Datos insertados")
    
    # Probar consultas
    print("🔍 Probando consultas...")
    
    queries = [
        ("Total actividades", "SELECT COUNT(*) FROM activities"),
        ("Actividades activas", "SELECT COUNT(*) FROM activities WHERE vigente = 1"),
        ("Valor total", "SELECT SUM(amount) FROM activities"),
        ("Total contratos", "SELECT COUNT(*) FROM contracts"),
        ("Total usuarios", "SELECT COUNT(*) FROM profiles"),
        ("Gateways activos", "SELECT COUNT(*) FROM gateways WHERE status = 'activo'")
    ]
    
    for name, query in queries:
        try:
            result = cursor.execute(query).fetchone()
            print(f"📊 {name}: {result[0]}")
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
    
    conn.close()
    print(f"\n🎉 ¡Base de datos corregida!")
    print(f"📁 Archivo: {db_name}")
    print(f"💡 Para probar: python -c \"import sqlite3; conn=sqlite3.connect('{db_name}'); print(conn.execute('SELECT COUNT(*) FROM activities').fetchone()[0])\"")

if __name__ == "__main__":
    fix_database()
