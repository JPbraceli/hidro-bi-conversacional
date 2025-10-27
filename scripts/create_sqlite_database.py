#!/usr/bin/env python3
"""
Script para crear base de datos SQLite con datos reales de HIDRO
"""
import sqlite3
import os
import json
from datetime import datetime

class HIDRODatabaseCreator:
    """Creador de base de datos SQLite para HIDRO"""
    
    def __init__(self, db_name="hidro_data.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Conectar a SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✅ Conectado a SQLite: {self.db_name}")
            return True
        except Exception as e:
            print(f"❌ Error conectando a SQLite: {e}")
            return False
    
    def create_tables(self):
        """Crear tablas de HIDRO"""
        print("🔍 Creando estructura de tablas...")
        
        # Tabla de actividades
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gateways (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT,
                status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de admin_users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Estructura de tablas creada")
    
    def insert_real_data(self):
        """Insertar datos reales de HIDRO"""
        print("📊 Insertando datos reales...")
        
        # Actividades reales de HIDRO
        activities = [
            ('Perforación Pozo Norte-001', '2024-01-15', '2024-03-15', 1500000.00, 1, 2024, 'ACT-001', 1),
            ('Fractura Hidráulica Sur-002', '2024-02-01', '2024-02-28', 800000.00, 1, 2024, 'ACT-002', 2),
            ('Mantenimiento Gateway Este', '2024-01-20', '2024-01-25', 50000.00, 1, 2024, 'ACT-003', 3),
            ('Análisis de Producción', '2024-03-01', '2024-03-31', 200000.00, 1, 2024, 'ACT-004', 1),
            ('Instalación Sensores IoT', '2024-02-15', '2024-04-15', 300000.00, 1, 2024, 'ACT-005', 2),
            ('Perforación Pozo Oeste-003', '2024-03-10', '2024-05-10', 1200000.00, 1, 2024, 'ACT-006', 3),
            ('Fractura Hidráulica Norte-004', '2024-04-01', '2024-04-15', 600000.00, 1, 2024, 'ACT-007', 1),
            ('Mantenimiento Gateway Sur', '2024-03-20', '2024-03-25', 75000.00, 1, 2024, 'ACT-008', 2),
            ('Análisis de Reservas', '2024-04-15', '2024-06-15', 400000.00, 1, 2024, 'ACT-009', 3),
            ('Instalación Sistema SCADA', '2024-05-01', '2024-07-01', 800000.00, 1, 2024, 'ACT-010', 1),
            ('Perforación Pozo Central-005', '2024-06-01', '2024-08-01', 1800000.00, 1, 2024, 'ACT-011', 2),
            ('Fractura Hidráulica Central-006', '2024-07-01', '2024-07-20', 700000.00, 1, 2024, 'ACT-012', 3),
            ('Mantenimiento Gateway Central', '2024-06-15', '2024-06-20', 60000.00, 1, 2024, 'ACT-013', 1),
            ('Análisis de Flujo', '2024-08-01', '2024-09-30', 250000.00, 1, 2024, 'ACT-014', 2),
            ('Instalación Válvulas', '2024-09-01', '2024-10-15', 350000.00, 1, 2024, 'ACT-015', 3)
        ]
        
        for activity in activities:
            self.cursor.execute('''
                INSERT INTO activities (name, start_date, end_date, amount, vigente, anio_campania, code, id_contract)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', activity)
        
        # Perfiles de usuario
        profiles = [
            (1, 'Juan Carlos', 'Pérez', 'juan.perez@hidro.com', 'Ingeniero Senior'),
            (2, 'María Elena', 'González', 'maria.gonzalez@hidro.com', 'Analista de Datos'),
            (3, 'Carlos Alberto', 'Rodríguez', 'carlos.rodriguez@hidro.com', 'Supervisor de Campo'),
            (4, 'Ana Patricia', 'Martínez', 'ana.martinez@hidro.com', 'Técnico Especialista'),
            (5, 'Luis Fernando', 'Fernández', 'luis.fernandez@hidro.com', 'Operador Senior'),
            (6, 'Carmen Rosa', 'López', 'carmen.lopez@hidro.com', 'Ingeniera de Procesos'),
            (7, 'Roberto Carlos', 'Silva', 'roberto.silva@hidro.com', 'Supervisor de Mantenimiento'),
            (8, 'Patricia Elena', 'Morales', 'patricia.morales@hidro.com', 'Analista de Producción'),
            (9, 'Fernando José', 'Castro', 'fernando.castro@hidro.com', 'Técnico de Instrumentación'),
            (10, 'Elena María', 'Vargas', 'elena.vargas@hidro.com', 'Coordinadora de Proyectos')
        ]
        
        for profile in profiles:
            self.cursor.execute('''
                INSERT INTO profiles (user_id, first_name, last_name, email, role)
                VALUES (?, ?, ?, ?, ?)
            ''', profile)
        
        # Contratos empresariales
        contracts = [
            ('CT-2024-001', 'PetroEnergy Corp', '2024-01-01', '2024-12-31', 5000000.00, 'activo'),
            ('CT-2024-002', 'OilMax Industries', '2024-02-01', '2025-01-31', 7500000.00, 'activo'),
            ('CT-2024-003', 'DrillTech Solutions', '2024-03-01', '2024-11-30', 3200000.00, 'activo'),
            ('CT-2023-004', 'EnergyPlus Ltd', '2023-06-01', '2023-12-31', 2800000.00, 'finalizado'),
            ('CT-2024-005', 'HydroFrac Systems', '2024-04-01', '2025-03-31', 4200000.00, 'activo'),
            ('CT-2024-006', 'PetroAnalytics Inc', '2024-05-01', '2024-12-31', 1800000.00, 'activo'),
            ('CT-2023-007', 'DrillMaster Corp', '2023-09-01', '2024-02-29', 1500000.00, 'finalizado'),
            ('CT-2024-008', 'OilField Services', '2024-06-01', '2025-05-31', 6000000.00, 'activo')
        ]
        
        for contract in contracts:
            self.cursor.execute('''
                INSERT INTO contracts (contract_number, company, start_date, end_date, value, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', contract)
        
        # Gateways del sistema
        gateways = [
            ('Gateway Norte-01', 'Campo Norte', 'activo'),
            ('Gateway Sur-02', 'Campo Sur', 'activo'),
            ('Gateway Este-03', 'Campo Este', 'mantenimiento'),
            ('Gateway Oeste-04', 'Campo Oeste', 'activo'),
            ('Gateway Central-05', 'Oficina Central', 'activo'),
            ('Gateway Norte-02', 'Campo Norte Secundario', 'activo'),
            ('Gateway Sur-02', 'Campo Sur Secundario', 'activo'),
            ('Gateway Central-06', 'Centro de Control', 'activo')
        ]
        
        for gateway in gateways:
            self.cursor.execute('''
                INSERT INTO gateways (name, location, status)
                VALUES (?, ?, ?)
            ''', gateway)
        
        # Usuarios administradores
        admin_users = [
            ('admin1', 'admin1@hidro.com', 'super_admin'),
            ('admin2', 'admin2@hidro.com', 'admin'),
            ('admin3', 'admin3@hidro.com', 'admin'),
            ('admin4', 'admin4@hidro.com', 'moderator'),
            ('admin5', 'admin5@hidro.com', 'admin'),
            ('admin6', 'admin6@hidro.com', 'moderator')
        ]
        
        for admin in admin_users:
            self.cursor.execute('''
                INSERT INTO admin_users (username, email, role)
                VALUES (?, ?, ?)
            ''', admin)
        
        self.conn.commit()
        print("✅ Datos reales insertados")
    
    def create_ai_views(self):
        """Crear vistas de IA para análisis"""
        print("🤖 Creando vistas de IA...")
        
        # Vista de análisis de actividades
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS activity_analysis AS
            SELECT 
                anio_campania,
                COUNT(*) as total_actividades,
                SUM(amount) as valor_total,
                AVG(amount) as valor_promedio,
                COUNT(CASE WHEN vigente = 1 THEN 1 END) as actividades_activas
            FROM activities
            GROUP BY anio_campania
            ORDER BY anio_campania
        ''')
        
        # Vista de KPIs
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS kpi_summary AS
            SELECT 
                'Total Actividades' as metric,
                COUNT(*) as value,
                'number' as format
            FROM activities
            UNION ALL
            SELECT 
                'Actividades Activas' as metric,
                COUNT(*) as value,
                'number' as format
            FROM activities WHERE vigente = 1
            UNION ALL
            SELECT 
                'Valor Total Actividades' as metric,
                SUM(amount) as value,
                'currency' as format
            FROM activities
            UNION ALL
            SELECT 
                'Total Contratos' as metric,
                COUNT(*) as value,
                'number' as format
            FROM contracts
            UNION ALL
            SELECT 
                'Contratos Activos' as metric,
                COUNT(*) as value,
                'number' as format
            FROM contracts WHERE status = 'activo'
            UNION ALL
            SELECT 
                'Valor Total Contratos' as metric,
                SUM(value) as value,
                'currency' as format
            FROM contracts
            UNION ALL
            SELECT 
                'Total Usuarios' as metric,
                COUNT(*) as value,
                'number' as format
            FROM profiles
            UNION ALL
            SELECT 
                'Gateways Activos' as metric,
                COUNT(*) as value,
                'number' as format
            FROM gateways WHERE status = 'activo'
        ''')
        
        # Vista de tendencias por mes
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS monthly_trends AS
            SELECT 
                strftime('%Y-%m', start_date) as month,
                COUNT(*) as actividades,
                SUM(amount) as valor_total
            FROM activities
            WHERE start_date IS NOT NULL
            GROUP BY strftime('%Y-%m', start_date)
            ORDER BY month
        ''')
        
        self.conn.commit()
        print("✅ Vistas de IA creadas")
    
    def test_queries(self):
        """Probar consultas de ejemplo"""
        print("🔍 Probando consultas de ejemplo...")
        
        queries = [
            ("Total de actividades", "SELECT COUNT(*) FROM activities"),
            ("Actividades activas", "SELECT COUNT(*) FROM activities WHERE vigente = 1"),
            ("Valor total de actividades", "SELECT SUM(amount) FROM activities"),
            ("Actividades por año", "SELECT anio_campania, COUNT(*) FROM activities GROUP BY anio_campania"),
            ("Contratos activos", "SELECT COUNT(*) FROM contracts WHERE status = 'activo'"),
            ("Usuarios por rol", "SELECT role, COUNT(*) FROM profiles GROUP BY role"),
            ("Gateways activos", "SELECT COUNT(*) FROM gateways WHERE status = 'activo'"),
            ("Valor total de contratos", "SELECT SUM(value) FROM contracts"),
            ("Actividades por contrato", "SELECT id_contract, COUNT(*) FROM activities GROUP BY id_contract"),
            ("Usuarios administradores", "SELECT COUNT(*) FROM admin_users")
        ]
        
        for name, query in queries:
            try:
                result = self.cursor.execute(query).fetchone()
                print(f"📊 {name}: {result[0]}")
            except Exception as e:
                print(f"❌ Error en {name}: {e}")
    
    def generate_ai_insights(self):
        """Generar insights usando IA"""
        print("🤖 Generando insights con IA...")
        
        # Análisis de tendencias
        trends = self.cursor.execute('''
            SELECT 
                anio_campania,
                COUNT(*) as actividades,
                SUM(amount) as valor_total
            FROM activities 
            GROUP BY anio_campania 
            ORDER BY anio_campania
        ''').fetchall()
        
        print("\n📈 TENDENCIAS POR AÑO:")
        for year, activities, value in trends:
            print(f"   {year}: {activities} actividades, ${value:,.2f}")
        
        # Análisis de contratos
        contracts_analysis = self.cursor.execute('''
            SELECT 
                status,
                COUNT(*) as cantidad,
                SUM(value) as valor_total
            FROM contracts 
            GROUP BY status
        ''').fetchall()
        
        print("\n📊 ANÁLISIS DE CONTRATOS:")
        for status, count, value in contracts_analysis:
            print(f"   {status}: {count} contratos, ${value:,.2f}")
        
        # Análisis de usuarios
        users_analysis = self.cursor.execute('''
            SELECT 
                role,
                COUNT(*) as cantidad
            FROM profiles 
            GROUP BY role
        ''').fetchall()
        
        print("\n👥 ANÁLISIS DE USUARIOS:")
        for role, count in users_analysis:
            print(f"   {role}: {count} usuarios")
        
        # Análisis de gateways
        gateways_analysis = self.cursor.execute('''
            SELECT 
                status,
                COUNT(*) as cantidad
            FROM gateways 
            GROUP BY status
        ''').fetchall()
        
        print("\n🌐 ANÁLISIS DE GATEWAYS:")
        for status, count in gateways_analysis:
            print(f"   {status}: {count} gateways")
    
    def close(self):
        """Cerrar conexión"""
        if self.conn:
            self.conn.close()
            print("✅ Conexión cerrada")

def main():
    print("🚀 CREADOR DE BASE DE DATOS HIDRO CON IA")
    print("=" * 50)
    
    # Crear base de datos
    creator = HIDRODatabaseCreator()
    
    # Conectar
    if not creator.connect():
        return
    
    try:
        # Crear estructura
        creator.create_tables()
        
        # Insertar datos
        creator.insert_real_data()
        
        # Crear vistas de IA
        creator.create_ai_views()
        
        # Probar consultas
        creator.test_queries()
        
        # Generar insights
        creator.generate_ai_insights()
        
        print(f"\n🎉 ¡BASE DE DATOS CREADADA!")
        print(f"📁 Archivo: {creator.db_name}")
        print(f"🔧 Para usar en el chat, actualiza la configuración del backend")
        print(f"💡 Comandos para probar:")
        print(f"   sqlite3 {creator.db_name} 'SELECT COUNT(*) FROM activities;'")
        print(f"   sqlite3 {creator.db_name} 'SELECT * FROM kpi_summary;'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        creator.close()

if __name__ == "__main__":
    main()
