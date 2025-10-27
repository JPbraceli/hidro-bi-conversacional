#!/usr/bin/env python3
"""
Interfaz gráfica simple para SQLite usando tkinter (incluido en Python)
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os

class SQLiteViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 HIDRO Database Viewer")
        self.root.geometry("1000x700")
        
        # Variables
        self.conn = None
        self.db_path = "hidro_data.db"
        
        # Crear interfaz
        self.create_widgets()
        
        # Conectar a la base de datos
        self.connect_database()
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🔍 HIDRO Database Viewer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Frame de controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botón para listar tablas
        ttk.Button(controls_frame, text="📋 Listar Tablas", 
                  command=self.list_tables).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para KPIs
        ttk.Button(controls_frame, text="📊 Mostrar KPIs", 
                  command=self.show_kpis).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para consultas
        ttk.Button(controls_frame, text="🔍 Consultas SQL", 
                  command=self.show_queries).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para cerrar
        ttk.Button(controls_frame, text="❌ Cerrar", 
                  command=self.root.quit).pack(side=tk.RIGHT)
        
        # Área de texto para resultados
        self.text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                  width=80, height=30)
        self.text_area.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de entrada SQL
        sql_frame = ttk.Frame(main_frame)
        sql_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        sql_frame.columnconfigure(0, weight=1)
        
        ttk.Label(sql_frame, text="Consulta SQL:").pack(anchor=tk.W)
        
        self.sql_entry = ttk.Entry(sql_frame)
        self.sql_entry.pack(fill=tk.X, pady=(5, 0))
        self.sql_entry.bind('<Return>', self.execute_sql)
        
        ttk.Button(sql_frame, text="Ejecutar", 
                  command=self.execute_sql).pack(anchor=tk.E, pady=(5, 0))
    
    def connect_database(self):
        """Conectar a la base de datos"""
        if not os.path.exists(self.db_path):
            self.text_area.insert(tk.END, f"❌ Base de datos no encontrada: {self.db_path}\n")
            self.text_area.insert(tk.END, "💡 Ejecuta primero: python scripts/fix_sqlite_database.py\n")
            return False
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.text_area.insert(tk.END, f"✅ Conectado a: {self.db_path}\n")
            return True
        except Exception as e:
            self.text_area.insert(tk.END, f"❌ Error conectando: {e}\n")
            return False
    
    def list_tables(self):
        """Listar todas las tablas"""
        if not self.conn:
            return
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "📋 TABLAS EN LA BASE DE DATOS\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n\n")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
            tables = cursor.fetchall()
            
            for table_name, in tables:
                self.text_area.insert(tk.END, f"📊 Tabla: {table_name}\n")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                self.text_area.insert(tk.END, f"   Registros: {count}\n")
                
                # Mostrar columnas
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                self.text_area.insert(tk.END, f"   Columnas: {len(columns)}\n")
                
                # Mostrar primeras 3 columnas
                col_names = [col[1] for col in columns[:3]]
                if len(columns) > 3:
                    col_names.append("...")
                self.text_area.insert(tk.END, f"   {', '.join(col_names)}\n\n")
                
        except Exception as e:
            self.text_area.insert(tk.END, f"❌ Error: {e}\n")
    
    def show_kpis(self):
        """Mostrar KPIs principales"""
        if not self.conn:
            return
        
        self.text_area.delete(1.END, tk.END)
        self.text_area.insert(tk.END, "📊 KPIs PRINCIPALES\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n\n")
        
        try:
            cursor = self.conn.cursor()
            
            # KPIs
            kpis = [
                ("Total Actividades", "SELECT COUNT(*) FROM activities"),
                ("Actividades Activas", "SELECT COUNT(*) FROM activities WHERE vigente = 1"),
                ("Valor Total Actividades", "SELECT SUM(amount) FROM activities"),
                ("Total Contratos", "SELECT COUNT(*) FROM contracts"),
                ("Contratos Activos", "SELECT COUNT(*) FROM contracts WHERE status = 'activo'"),
                ("Total Usuarios", "SELECT COUNT(*) FROM profiles"),
                ("Gateways Activos", "SELECT COUNT(*) FROM gateways WHERE status = 'activo'"),
                ("Usuarios Admin", "SELECT COUNT(*) FROM admin_users")
            ]
            
            for name, query in kpis:
                cursor.execute(query)
                result = cursor.fetchone()[0]
                self.text_area.insert(tk.END, f"📈 {name}: {result}\n")
            
            self.text_area.insert(tk.END, "\n📊 ANÁLISIS DETALLADO\n")
            self.text_area.insert(tk.END, "-" * 30 + "\n")
            
            # Actividades por año
            cursor.execute("SELECT anio_campania, COUNT(*) FROM activities GROUP BY anio_campania")
            years = cursor.fetchall()
            self.text_area.insert(tk.END, "📈 Actividades por año:\n")
            for year, count in years:
                self.text_area.insert(tk.END, f"   {year}: {count} actividades\n")
            
            # Usuarios por rol
            cursor.execute("SELECT role, COUNT(*) FROM profiles GROUP BY role")
            roles = cursor.fetchall()
            self.text_area.insert(tk.END, "\n👥 Usuarios por rol:\n")
            for role, count in roles:
                self.text_area.insert(tk.END, f"   {role}: {count} usuarios\n")
            
            # Contratos por estado
            cursor.execute("SELECT status, COUNT(*) FROM contracts GROUP BY status")
            statuses = cursor.fetchall()
            self.text_area.insert(tk.END, "\n📋 Contratos por estado:\n")
            for status, count in statuses:
                self.text_area.insert(tk.END, f"   {status}: {count} contratos\n")
                
        except Exception as e:
            self.text_area.insert(tk.END, f"❌ Error: {e}\n")
    
    def show_queries(self):
        """Mostrar consultas predefinidas"""
        if not self.conn:
            return
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "🔍 CONSULTAS PREDEFINIDAS\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n\n")
        
        queries = [
            ("Total de actividades", "SELECT COUNT(*) as total FROM activities"),
            ("Actividades activas", "SELECT COUNT(*) as activas FROM activities WHERE vigente = 1"),
            ("Valor total de actividades", "SELECT SUM(amount) as valor_total FROM activities"),
            ("Actividades por año", "SELECT anio_campania, COUNT(*) as cantidad FROM activities GROUP BY anio_campania"),
            ("Contratos activos", "SELECT COUNT(*) as activos FROM contracts WHERE status = 'activo'"),
            ("Usuarios por rol", "SELECT role, COUNT(*) as cantidad FROM profiles GROUP BY role"),
            ("Gateways activos", "SELECT COUNT(*) as activos FROM gateways WHERE status = 'activo'"),
            ("Top 5 actividades por valor", "SELECT name, amount FROM activities ORDER BY amount DESC LIMIT 5")
        ]
        
        for name, query in queries:
            self.text_area.insert(tk.END, f"📋 {name}:\n")
            self.text_area.insert(tk.END, f"   SQL: {query}\n")
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                self.text_area.insert(tk.END, f"   Resultado: {results}\n\n")
            except Exception as e:
                self.text_area.insert(tk.END, f"   ❌ Error: {e}\n\n")
    
    def execute_sql(self, event=None):
        """Ejecutar consulta SQL personalizada"""
        if not self.conn:
            return
        
        query = self.sql_entry.get().strip()
        if not query:
            return
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"🔍 Ejecutando: {query}\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n\n")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                self.text_area.insert(tk.END, f"✅ Resultados ({len(results)} filas):\n")
                for row in results:
                    self.text_area.insert(tk.END, f"   {row}\n")
            else:
                self.text_area.insert(tk.END, "✅ Consulta ejecutada (sin resultados)\n")
                
        except Exception as e:
            self.text_area.insert(tk.END, f"❌ Error: {e}\n")
    
    def __del__(self):
        """Cerrar conexión al destruir"""
        if self.conn:
            self.conn.close()

def main():
    """Función principal"""
    root = tk.Tk()
    app = SQLiteViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
