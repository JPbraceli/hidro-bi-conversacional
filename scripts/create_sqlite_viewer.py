#!/usr/bin/env python3
"""
Script para crear una interfaz gráfica web para SQLite usando Streamlit
"""
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

def init_database():
    """Inicializar conexión a la base de datos"""
    db_path = "hidro_data.db"
    if not os.path.exists(db_path):
        st.error(f"❌ Base de datos no encontrada: {db_path}")
        st.info("💡 Ejecuta primero: python scripts/fix_sqlite_database.py")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        st.error(f"❌ Error conectando a la base: {e}")
        return None

def get_table_data(conn, table_name):
    """Obtener datos de una tabla"""
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ Error obteniendo datos de {table_name}: {e}")
        return pd.DataFrame()

def get_kpi_data(conn):
    """Obtener datos de KPIs"""
    kpis = {}
    
    # Total actividades
    result = conn.execute("SELECT COUNT(*) FROM activities").fetchone()
    kpis['Total Actividades'] = result[0]
    
    # Actividades activas
    result = conn.execute("SELECT COUNT(*) FROM activities WHERE vigente = 1").fetchone()
    kpis['Actividades Activas'] = result[0]
    
    # Valor total
    result = conn.execute("SELECT SUM(amount) FROM activities").fetchone()
    kpis['Valor Total'] = result[0] if result[0] else 0
    
    # Total contratos
    result = conn.execute("SELECT COUNT(*) FROM contracts").fetchone()
    kpis['Total Contratos'] = result[0]
    
    # Contratos activos
    result = conn.execute("SELECT COUNT(*) FROM contracts WHERE status = 'activo'").fetchone()
    kpis['Contratos Activos'] = result[0]
    
    # Total usuarios
    result = conn.execute("SELECT COUNT(*) FROM profiles").fetchone()
    kpis['Total Usuarios'] = result[0]
    
    # Gateways activos
    result = conn.execute("SELECT COUNT(*) FROM gateways WHERE status = 'activo'").fetchone()
    kpis['Gateways Activos'] = result[0]
    
    return kpis

def create_activity_chart(conn):
    """Crear gráfico de actividades por año"""
    try:
        query = "SELECT anio_campania, COUNT(*) as cantidad FROM activities GROUP BY anio_campania"
        df = pd.read_sql_query(query, conn)
        
        fig = px.bar(df, x='anio_campania', y='cantidad', 
                    title='Actividades por Año',
                    labels={'anio_campania': 'Año', 'cantidad': 'Cantidad'})
        return fig
    except Exception as e:
        st.error(f"❌ Error creando gráfico: {e}")
        return None

def create_contract_chart(conn):
    """Crear gráfico de contratos por estado"""
    try:
        query = "SELECT status, COUNT(*) as cantidad FROM contracts GROUP BY status"
        df = pd.read_sql_query(query, conn)
        
        fig = px.pie(df, values='cantidad', names='status', 
                    title='Contratos por Estado')
        return fig
    except Exception as e:
        st.error(f"❌ Error creando gráfico: {e}")
        return None

def create_user_chart(conn):
    """Crear gráfico de usuarios por rol"""
    try:
        query = "SELECT role, COUNT(*) as cantidad FROM profiles GROUP BY role"
        df = pd.read_sql_query(query, conn)
        
        fig = px.bar(df, x='role', y='cantidad', 
                    title='Usuarios por Rol',
                    labels={'role': 'Rol', 'cantidad': 'Cantidad'})
        fig.update_xaxis(tickangle=45)
        return fig
    except Exception as e:
        st.error(f"❌ Error creando gráfico: {e}")
        return None

def main():
    """Función principal de Streamlit"""
    st.set_page_config(
        page_title="HIDRO Database Viewer",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 HIDRO Database Viewer")
    st.markdown("**Interfaz gráfica para la base de datos SQLite de HIDRO**")
    
    # Inicializar base de datos
    conn = init_database()
    if conn is None:
        return
    
    # Sidebar para navegación
    st.sidebar.title("📋 Navegación")
    
    # Obtener lista de tablas
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    tables = [row[0] for row in cursor.fetchall()]
    
    selected_table = st.sidebar.selectbox("Seleccionar tabla:", tables)
    
    # Pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Tablas", "📈 Gráficos", "🔍 Consultas"])
    
    with tab1:
        st.header("📊 Dashboard de HIDRO")
        
        # KPIs
        kpis = get_kpi_data(conn)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Actividades", kpis['Total Actividades'])
            st.metric("Actividades Activas", kpis['Actividades Activas'])
        
        with col2:
            st.metric("Valor Total", f"${kpis['Valor Total']:,.2f}")
            st.metric("Total Contratos", kpis['Total Contratos'])
        
        with col3:
            st.metric("Contratos Activos", kpis['Contratos Activos'])
            st.metric("Total Usuarios", kpis['Total Usuarios'])
        
        with col4:
            st.metric("Gateways Activos", kpis['Gateways Activos'])
        
        # Gráficos del dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_activity_chart(conn)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_contract_chart(conn)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header(f"📋 Tabla: {selected_table}")
        
        # Mostrar datos de la tabla seleccionada
        df = get_table_data(conn, selected_table)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Estadísticas de la tabla
            st.subheader("📊 Estadísticas")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Registros", len(df))
            
            with col2:
                st.metric("Columnas", len(df.columns))
            
            with col3:
                st.metric("Memoria", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        else:
            st.warning("No se pudieron cargar los datos")
    
    with tab3:
        st.header("📈 Gráficos y Análisis")
        
        # Gráfico de actividades por año
        st.subheader("Actividades por Año")
        fig1 = create_activity_chart(conn)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico de contratos por estado
        st.subheader("Contratos por Estado")
        fig2 = create_contract_chart(conn)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
        
        # Gráfico de usuarios por rol
        st.subheader("Usuarios por Rol")
        fig3 = create_user_chart(conn)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        st.header("🔍 Consultas SQL")
        
        # Editor de consultas
        query = st.text_area("Escribe tu consulta SQL:", 
                            value="SELECT * FROM activities LIMIT 10",
                            height=100)
        
        if st.button("Ejecutar Consulta"):
            try:
                df = pd.read_sql_query(query, conn)
                st.dataframe(df, use_container_width=True)
                
                # Mostrar información de la consulta
                st.info(f"✅ Consulta ejecutada exitosamente. {len(df)} filas encontradas.")
                
            except Exception as e:
                st.error(f"❌ Error en la consulta: {e}")
        
        # Consultas predefinidas
        st.subheader("📋 Consultas Predefinidas")
        
        predefined_queries = {
            "Total de actividades": "SELECT COUNT(*) as total FROM activities",
            "Actividades activas": "SELECT COUNT(*) as activas FROM activities WHERE vigente = 1",
            "Valor total de actividades": "SELECT SUM(amount) as valor_total FROM activities",
            "Actividades por año": "SELECT anio_campania, COUNT(*) as cantidad FROM activities GROUP BY anio_campania",
            "Contratos activos": "SELECT COUNT(*) as activos FROM contracts WHERE status = 'activo'",
            "Usuarios por rol": "SELECT role, COUNT(*) as cantidad FROM profiles GROUP BY role",
            "Gateways activos": "SELECT COUNT(*) as activos FROM gateways WHERE status = 'activo'"
        }
        
        selected_query = st.selectbox("Seleccionar consulta:", list(predefined_queries.keys()))
        
        if st.button("Ejecutar Consulta Predefinida"):
            try:
                query = predefined_queries[selected_query]
                df = pd.read_sql_query(query, conn)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Cerrar conexión
    conn.close()
    
    # Footer
    st.markdown("---")
    st.markdown("**🔧 HIDRO Database Viewer** - Interfaz gráfica para SQLite")
    st.markdown("**📁 Base de datos:** hidro_data.db")

if __name__ == "__main__":
    main()
