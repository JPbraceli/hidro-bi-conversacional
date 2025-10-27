import React from 'react'
import { BarChart3, LineChart, PieChart, Table, TrendingUp, AlertCircle, Activity, Target, Radar, Grid3X3 } from 'lucide-react'
import DataTable from './DataTable'
import LineChartComponent from './LineChartComponent'
import BarChartComponent from './BarChartComponent'
import PieChartComponent from './PieChartComponent'
import KPICards from './KPICards'
import HeatmapComponent from './HeatmapComponent'
import AreaChartComponent from './AreaChartComponent'
import ScatterChartComponent from './ScatterChartComponent'
import RadarChartComponent from './RadarChartComponent'

function VisualizationPanel({ data, isLoading, embedded = false }) {
  if (isLoading) {
    return (
      <div className={`${embedded ? 'bg-gray-50 rounded-lg p-4' : 'bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6'}`}>
        <div className="flex items-center justify-center h-32">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            <p className="text-gray-600 text-sm">Ejecutando consulta...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!data) {
    if (embedded) return null;
    
    return (
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
        <div className="text-center py-12">
          <BarChart3 className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Panel de Visualización
          </h3>
          <p className="text-gray-600">
            Ejecuta una consulta desde el chat para ver los resultados aquí
          </p>
        </div>
      </div>
    )
  }

  if (!data.success) {
    return (
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
        <div className="text-center py-12">
          <AlertCircle className="mx-auto h-16 w-16 text-red-400 mb-4" />
          <h3 className="text-lg font-semibold text-red-900 mb-2">
            Error en la Consulta
          </h3>
          <p className="text-red-600">
            {data.error || 'Ocurrió un error inesperado'}
          </p>
        </div>
      </div>
    )
  }

  const renderVisualization = () => {
    const vizType = data.visualization_type
    const vizData = data.data

    switch (vizType) {
      case 'table':
        return <DataTable data={vizData} />
      
      case 'line_chart':
        return <LineChartComponent data={vizData} />
      
      case 'bar_chart':
        return <BarChartComponent data={vizData} />
      
      case 'pie_chart':
        return <PieChartComponent data={vizData} />
      
      case 'area_chart':
        return <AreaChartComponent data={vizData} />
      
      case 'scatter_chart':
        return <ScatterChartComponent data={vizData} />
      
      case 'radar_chart':
        return <RadarChartComponent data={vizData} />
      
      case 'heatmap':
        return <HeatmapComponent data={vizData} />
      
      case 'kpi_cards':
        return <KPICards data={vizData} />
      
      default:
        return <DataTable data={vizData} />
    }
  }

  const getVisualizationIcon = () => {
    const vizType = data.visualization_type
    
    switch (vizType) {
      case 'line_chart':
        return <LineChart className="w-5 h-5" />
      case 'bar_chart':
        return <BarChart3 className="w-5 h-5" />
      case 'pie_chart':
        return <PieChart className="w-5 h-5" />
      case 'area_chart':
        return <Activity className="w-5 h-5" />
      case 'scatter_chart':
        return <Target className="w-5 h-5" />
      case 'radar_chart':
        return <Radar className="w-5 h-5" />
      case 'heatmap':
        return <Grid3X3 className="w-5 h-5" />
      case 'kpi_cards':
        return <TrendingUp className="w-5 h-5" />
      default:
        return <Table className="w-5 h-5" />
    }
  }

  const getVisualizationTitle = () => {
    const vizType = data.visualization_type
    
    switch (vizType) {
      case 'line_chart':
        return 'Gráfico de Líneas'
      case 'bar_chart':
        return 'Gráfico de Barras'
      case 'pie_chart':
        return 'Gráfico de Pastel'
      case 'area_chart':
        return 'Gráfico de Área'
      case 'scatter_chart':
        return 'Gráfico de Dispersión'
      case 'radar_chart':
        return 'Gráfico de Radar'
      case 'heatmap':
        return 'Mapa de Calor'
      case 'kpi_cards':
        return 'Indicadores KPI'
      default:
        return 'Tabla de Datos'
    }
  }

  return (
    <div className={`${embedded ? 'bg-gray-50 rounded-lg p-4' : 'bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6'}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <div className={`${embedded ? 'w-6 h-6' : 'w-10 h-10'} bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center mr-3`}>
            {getVisualizationIcon()}
          </div>
          <div>
            <h2 className={`${embedded ? 'text-sm' : 'text-xl'} font-bold text-gray-900`}>
              {getVisualizationTitle()}
            </h2>
            <p className="text-gray-600 text-xs">
              {data.row_count} registros encontrados
            </p>
          </div>
        </div>
      </div>

      {/* Contenido de visualización */}
      <div className={`${embedded ? 'h-64' : 'h-[calc(100vh-200px)] min-h-[300px]'} overflow-y-auto`}>
        {renderVisualization()}
      </div>
    </div>
  )
}

export default VisualizationPanel
