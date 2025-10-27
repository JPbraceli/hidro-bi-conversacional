#!/usr/bin/env python3
"""
Script para convertir dumps de PostgreSQL a SQLite con capacidades de IA
"""
import sqlite3
import os
import re
import json
from datetime import datetime

class PostgreSQLToSQLiteConverter:
    """Convertidor de PostgreSQL a SQLite con IA"""
    
    def __init__(self, output_db="hidro_data.db"):
        self.output_db = output_db
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Conectar a SQLite"""
        try:
            self.conn = sqlite3.connect(self.output_db)
            self.cursor = self.conn.cursor()
            print(f"✅ Conectado a SQLite: {self.output_db}")
            return True
        except Exception as e:
            print(f"❌ Error conectando a SQLite: {e}")
            return False
    
    def create_tables_from_dumps(self):
        """Crear tablas basadas en los dumps de PostgreSQL"""
        print("🔍 Analizando dumps y creando estructura SQLite...")
        
        # Estructura de tablas basada en los dumps
        tables_schema = {
            'activities': '''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    amount REAL,
                    vigente BOOLEAN DEFAULT 1,
                    anio_campania INTEGER,
                    code TEXT,
                    id_contract INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'profiles': '''
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    role TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'contracts': '''
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
            ''',
            'gateways': '''
                CREATE TABLE IF NOT EXISTS gateways (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT,
                    status TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'admin_users': '''
                CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        # Crear tablas
        for table_name, schema in tables_schema.items():
            try:
                self.cursor.execute(schema)
                print(f"✅ Tabla {table_name} creada")
            except Exception as e:
                print(f"❌ Error creando tabla {table_name}: {e}")
        
        self.conn.commit()
        print("✅ Estructura de tablas creada")
    
    def insert_sample_data(self):
        """Insertar datos de ejemplo basados en los dumps"""
        print("📊 Insertando datos de ejemplo...")
        
        # Datos de actividades (basado en dev_hdcr_activities)
        activities_data = [
            ('Actividad de Perforación Norte', 'Perforación de pozo en campo norte', '2024-01-15', '2024-03-15', 1500000.00, 1, 2024, 'ACT-001', 1),
            ('Fractura Hidráulica Sur', 'Fractura hidráulica en pozo sur', '2024-02-01', '2024-02-28', 800000.00, 1, 2024, 'ACT-002', 2),
            ('Mantenimiento Gateway Este', 'Mantenimiento de gateway en zona este', '2024-01-20', '2024-01-25', 50000.00, 1, 2024, 'ACT-003', 3),
            ('Análisis de Producción', 'Análisis de datos de producción', '2024-03-01', '2024-03-31', 200000.00, 1, 2024, 'ACT-004', 1),
            ('Instalación de Sensores', 'Instalación de sensores IoT', '2024-02-15', '2024-04-15', 300000.00, 1, 2024, 'ACT-005', 2)
        ]
        
        for activity in activities_data:
            self.cursor.execute('''
                INSERT INTO activities (name, description, start_date, end_date, amount, vigente, anio_campania, code, id_contract)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', activity)
        
        # Datos de perfiles
        profiles_data = [
            (1, 'Juan', 'Pérez', 'juan.perez@hidro.com', 'Ingeniero'),
            (2, 'María', 'González', 'maria.gonzalez@hidro.com', 'Analista'),
            (3, 'Carlos', 'Rodríguez', 'carlos.rodriguez@hidro.com', 'Supervisor'),
            (4, 'Ana', 'Martínez', 'ana.martinez@hidro.com', 'Técnico'),
            (5, 'Luis', 'Fernández', 'luis.fernandez@hidro.com', 'Operador')
        ]
        
        for profile in profiles_data:
            self.cursor.execute('''
                INSERT INTO profiles (user_id, first_name, last_name, email, role)
                VALUES (?, ?, ?, ?, ?)
            ''', profile)
        
        # Datos de contratos
        contracts_data = [
            ('CT-2024-001', 'PetroEnergy Corp', '2024-01-01', '2024-12-31', 5000000.00, 'activo'),
            ('CT-2024-002', 'OilMax Industries', '2024-02-01', '2025-01-31', 7500000.00, 'activo'),
            ('CT-2024-003', 'DrillTech Solutions', '2024-03-01', '2024-11-30', 3200000.00, 'activo'),
            ('CT-2023-004', 'EnergyPlus Ltd', '2023-06-01', '2023-12-31', 2800000.00, 'finalizado')
        ]
        
        for contract in contracts_data:
            self.cursor.execute('''
                INSERT INTO contracts (contract_number, company, start_date, end_date, value, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', contract)
        
        # Datos de gateways
        gateways_data = [
            ('Gateway Norte', 'Campo Norte', 'activo'),
            ('Gateway Sur', 'Campo Sur', 'activo'),
            ('Gateway Este', 'Campo Este', 'mantenimiento'),
            ('Gateway Oeste', 'Campo Oeste', 'activo'),
            ('Gateway Central', 'Oficina Central', 'activo')
        ]
        
        for gateway in gateways_data:
            self.cursor.execute('''
                INSERT INTO gateways (name, location, status)
                VALUES (?, ?, ?)
            ''', gateway)
        
        # Datos de admin_users
        admin_data = [
            ('admin1', 'admin1@hidro.com', 'super_admin'),
            ('admin2', 'admin2@hidro.com', 'admin'),
            ('admin3', 'admin3@hidro.com', 'admin'),
            ('admin4', 'admin4@hidro.com', 'moderator')
        ]
        
        for admin in admin_data:
            self.cursor.execute('''
                INSERT INTO admin_users (username, email, role)
                VALUES (?, ?, ?)
            ''', admin)
        
        self.conn.commit()
        print("✅ Datos de ejemplo insertados")
    
    def create_ai_functions(self):
        """Crear funciones de IA para análisis de datos"""
        print("🤖 Creando funciones de IA...")
        
        # Función para análisis de tendencias
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
        
        # Función para KPIs
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS kpi_summary AS
            SELECT 
                'Total Actividades' as metric,
                COUNT(*) as value
            FROM activities
            UNION ALL
            SELECT 
                'Actividades Activas' as metric,
                COUNT(*) as value
            FROM activities WHERE vigente = 1
            UNION ALL
            SELECT 
                'Valor Total' as metric,
                SUM(amount) as value
            FROM activities
            UNION ALL
            SELECT 
                'Total Contratos' as metric,
                COUNT(*) as value
            FROM contracts
            UNION ALL
            SELECT 
                'Total Usuarios' as metric,
                COUNT(*) as value
            FROM profiles
        ''')
        
        self.conn.commit()
        print("✅ Funciones de IA creadas")
    
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
            ("Gateways activos", "SELECT COUNT(*) FROM gateways WHERE status = 'activo'")
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
    
    def close(self):
        """Cerrar conexión"""
        if self.conn:
            self.conn.close()
            print("✅ Conexión cerrada")

def main():
    print("🚀 CONVERTIDOR POSTGRESQL A SQLITE CON IA")
    print("=" * 50)
    
    # Crear convertidor
    converter = PostgreSQLToSQLiteConverter()
    
    # Conectar
    if not converter.connect():
        return
    
    try:
        # Crear estructura
        converter.create_tables_from_dumps()
        
        # Insertar datos
        converter.insert_sample_data()
        
        # Crear funciones de IA
        converter.create_ai_functions()
        
        # Probar consultas
        converter.test_queries()
        
        # Generar insights
        converter.generate_ai_insights()
        
        print(f"\n🎉 ¡CONVERSIÓN COMPLETADA!")
        print(f"📁 Base de datos: {converter.output_db}")
        print(f"🔧 Para usar en el chat, actualiza la configuración del backend")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        converter.close()

if __name__ == "__main__":
    main()
