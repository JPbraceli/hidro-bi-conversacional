#!/usr/bin/env python3
"""
Script para crear datos en la base hidro
"""
import psycopg2
import uuid

def create_hidro_data():
    """Crear datos en la base hidro"""
    try:
        print("🔍 Conectando a base 'hidro'...")
        
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=15433,
            user='hdcruser',
            password='localpass',
            dbname='hidro'
        )
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a hidro")
        
        # Crear tabla activities
        print("📦 Creando tabla activities...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id UUID PRIMARY KEY,
                name VARCHAR(255),
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                amount VARCHAR(255),
                vigente BOOLEAN,
                anio_campania INTEGER,
                code INTEGER,
                observations TEXT,
                operator VARCHAR(100),
                status VARCHAR(50)
            );
        """)
        
        # Crear tabla contracts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id UUID PRIMARY KEY,
                name VARCHAR(255),
                company VARCHAR(100),
                value DECIMAL(15,2),
                status VARCHAR(50),
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY,
                username VARCHAR(100),
                email VARCHAR(255),
                role VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insertar datos de prueba
        print("📊 Insertando datos de prueba...")
        
        # Actividades
        activities_data = []
        operators = ['Petrobras', 'Shell', 'Exxon', 'Chevron', 'BP', 'Total', 'Eni', 'Repsol']
        statuses = ['activo', 'inactivo', 'pendiente', 'completado']
        
        for i in range(20):
            activities_data.append((
                str(uuid.uuid4()),
                f'Pozo {i+1}-{2500+i}',
                f'2025-{(i%12)+1:02d}-01',
                f'2025-{(i%12)+1:02d}-15',
                f'{2.0 + i * 0.1:.6f}',
                i % 4 != 0,  # 3/4 vigentes
                2025,
                2500 + i,
                f'Observaciones del pozo {i+1}',
                operators[i % len(operators)],
                statuses[i % len(statuses)]
            ))
        
        cursor.executemany("""
            INSERT INTO activities (id, name, start_date, end_date, amount, vigente, anio_campania, code, observations, operator, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, activities_data)
        
        # Contratos
        contracts_data = []
        companies = ['Petrobras', 'Shell', 'Exxon', 'Chevron', 'BP', 'Total']
        
        for i in range(15):
            contracts_data.append((
                str(uuid.uuid4()),
                f'Contrato {i+1}',
                companies[i % len(companies)],
                1000000 + i * 100000,
                'activo' if i % 3 != 0 else 'inactivo',
                f'2025-{(i%12)+1:02d}-01',
                f'2025-{(i%12)+1:02d}-28'
            ))
        
        cursor.executemany("""
            INSERT INTO contracts (id, name, company, value, status, start_date, end_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, contracts_data)
        
        # Usuarios
        users_data = []
        roles = ['admin', 'operator', 'supervisor', 'technician', 'analyst']
        
        for i in range(10):
            users_data.append((
                str(uuid.uuid4()),
                f'user{i+1}',
                f'user{i+1}@hidro.com',
                roles[i % len(roles)]
            ))
        
        cursor.executemany("""
            INSERT INTO users (id, username, email, role) 
            VALUES (%s, %s, %s, %s)
        """, users_data)
        
        conn.commit()
        
        # Verificar datos
        cursor.execute("SELECT COUNT(*) FROM activities;")
        activities_count = cursor.fetchone()[0]
        print(f"📊 Actividades: {activities_count}")
        
        cursor.execute("SELECT COUNT(*) FROM contracts;")
        contracts_count = cursor.fetchone()[0]
        print(f"📊 Contratos: {contracts_count}")
        
        cursor.execute("SELECT COUNT(*) FROM users;")
        users_count = cursor.fetchone()[0]
        print(f"📊 Usuarios: {users_count}")
        
        # Mostrar algunas actividades
        cursor.execute("SELECT name, operator, status FROM activities LIMIT 5;")
        activities = cursor.fetchall()
        print(f"📋 Primeras actividades: {activities}")
        
        conn.close()
        
        print("🎉 ¡Datos creados en base 'hidro'!")
        print("🚀 Ahora reinicia el backend y prueba en el chat")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_hidro_data()




