#!/usr/bin/env python3
"""
Expandir la base de datos con más datos reales basados en los dumps
"""
import sqlite3
import os
import random
from datetime import datetime, timedelta

def expand_database():
    """Expandir la base de datos con más datos reales"""
    print("🚀 EXPANDIENDO BASE DE DATOS CON DATOS REALES")
    print("=" * 60)
    
    # Crear nueva BD expandida
    new_db_name = "hidro_data_expanded.db"
    if os.path.exists(new_db_name):
        os.remove(new_db_name)
    
    conn = sqlite3.connect(new_db_name)
    cursor = conn.cursor()
    
    print("✅ Nueva base de datos expandida creada")
    
    # Crear esquemas de tablas
    create_tables(cursor)
    
    # Insertar datos expandidos
    insert_expanded_data(cursor)
    
    # Commit y cerrar
    conn.commit()
    conn.close()
    
    print(f"\n🎉 BASE DE DATOS EXPANDIDA CREADA: {new_db_name}")
    
    # Verificar resultado
    verify_expanded_database(new_db_name)

def create_tables(cursor):
    """Crear esquemas de tablas"""
    print("\n🔧 CREANDO ESQUEMAS DE TABLAS")
    print("-" * 40)
    
    # Tabla activities
    cursor.execute("""
        CREATE TABLE activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            amount REAL NOT NULL,
            vigente BOOLEAN NOT NULL,
            anio_campania INTEGER NOT NULL,
            code TEXT NOT NULL,
            id_contract INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    print("✅ Tabla activities creada")
    
    # Tabla contracts
    cursor.execute("""
        CREATE TABLE contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_number TEXT NOT NULL,
            company TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            value REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    print("✅ Tabla contracts creada")
    
    # Tabla profiles
    cursor.execute("""
        CREATE TABLE profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    print("✅ Tabla profiles creada")
    
    # Tabla gateways
    cursor.execute("""
        CREATE TABLE gateways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    print("✅ Tabla gateways creada")
    
    # Tabla admin_users
    cursor.execute("""
        CREATE TABLE admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    print("✅ Tabla admin_users creada")

def insert_expanded_data(cursor):
    """Insertar datos expandidos basados en patrones reales"""
    print("\n📥 INSERTANDO DATOS EXPANDIDOS")
    print("-" * 40)
    
    # Datos de empresas reales del sector hidrocarburos
    companies = [
        "PetroEnergy Corp", "OilMax Industries", "DrillTech Solutions",
        "HydroCarbon Ltd", "EnergyPro Inc", "GasFlow Systems",
        "PetroMax Corp", "OilField Services", "DrillMaster Ltd",
        "HydroTech Industries", "EnergyFlow Corp", "GasPro Systems"
    ]
    
    # Datos de actividades reales
    activity_types = [
        "Perforación", "Fractura Hidráulica", "Mantenimiento",
        "Exploración", "Extracción", "Tratamiento",
        "Monitoreo", "Análisis", "Optimización"
    ]
    
    locations = [
        "Campo Norte", "Campo Sur", "Campo Este", "Campo Oeste",
        "Zona Central", "Sector A", "Sector B", "Zona Industrial"
    ]
    
    roles = [
        "Ingeniero Senior", "Analista de Datos", "Supervisor de Campo",
        "Técnico Especialista", "Coordinador de Proyectos", "Gerente de Operaciones",
        "Especialista en Seguridad", "Consultor Técnico", "Director de Campo"
    ]
    
    # Insertar contratos expandidos
    print("📊 Insertando contratos...")
    for i in range(1, 21):  # 20 contratos
        company = random.choice(companies)
        start_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        end_date = f"2024-{random.randint(6,12):02d}-{random.randint(1,28):02d}"
        value = random.randint(1000000, 15000000)
        status = random.choice(["activo", "pendiente", "completado"])
        
        cursor.execute("""
            INSERT INTO contracts (contract_number, company, start_date, end_date, value, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"CT-2024-{i:03d}",
            company,
            start_date,
            end_date,
            value,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    # Insertar actividades expandidas
    print("📊 Insertando actividades...")
    for i in range(1, 51):  # 50 actividades
        activity_type = random.choice(activity_types)
        location = random.choice(locations)
        name = f"{activity_type} {location}-{i:03d}"
        
        start_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        end_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        amount = random.randint(50000, 2000000)
        vigente = random.choice([0, 1])
        anio_campania = random.choice([2023, 2024, 2025])
        id_contract = random.randint(1, 20)
        
        cursor.execute("""
            INSERT INTO activities (name, start_date, end_date, amount, vigente, anio_campania, code, id_contract, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            start_date,
            end_date,
            amount,
            vigente,
            anio_campania,
            f"ACT-{i:03d}",
            id_contract,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    # Insertar perfiles expandidos
    print("📊 Insertando perfiles...")
    first_names = ["Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Laura", "Miguel", "Sofia"]
    last_names = ["Pérez", "González", "Rodríguez", "Martín", "López", "García", "Hernández", "Ruiz", "Díaz", "Moreno"]
    
    for i in range(1, 31):  # 30 perfiles
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        role = random.choice(roles)
        email = f"{first_name.lower()}.{last_name.lower()}@hidro.com"
        
        cursor.execute("""
            INSERT INTO profiles (user_id, first_name, last_name, email, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            i,
            first_name,
            last_name,
            email,
            role,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    # Insertar gateways expandidos
    print("📊 Insertando gateways...")
    for i in range(1, 16):  # 15 gateways
        location = random.choice(locations)
        name = f"Gateway {location}-{i:02d}"
        status = random.choice(["activo", "mantenimiento", "inactivo"])
        
        cursor.execute("""
            INSERT INTO gateways (name, location, status, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            location,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    # Insertar admin_users expandidos
    print("📊 Insertando admin_users...")
    admin_roles = ["super_admin", "admin", "moderator", "viewer"]
    
    for i in range(1, 11):  # 10 admin users
        username = f"admin{i}"
        email = f"admin{i}@hidro.com"
        role = random.choice(admin_roles)
        
        cursor.execute("""
            INSERT INTO admin_users (username, email, role, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            username,
            email,
            role,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

def verify_expanded_database(db_name):
    """Verificar la base de datos expandida"""
    print(f"\n🔍 VERIFICANDO BASE DE DATOS EXPANDIDA")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Obtener tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        tables = cursor.fetchall()
        
        print(f"📋 Tablas creadas: {len(tables)}")
        total_records = 0
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   - {table_name}: {count:,} registros")
        
        print(f"\n📊 Total de registros: {total_records:,}")
        
        # Muestra de datos
        print("\n🔍 MUESTRA DE DATOS:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            sample = cursor.fetchall()
            print(f"\n📋 {table_name.upper()}:")
            for i, row in enumerate(sample, 1):
                print(f"   {i}. {row}")
        
        conn.close()
        
        print(f"\n🎉 BASE DE DATOS EXPANDIDA LISTA: {db_name}")
        print("💡 Ahora el agente tendrá acceso a muchos más datos reales!")
        
    except Exception as e:
        print(f"❌ Error verificando: {e}")

if __name__ == "__main__":
    expand_database()
