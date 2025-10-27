import React from 'react'
import { BarChart3, LineChart, PieChart, Table, TrendingUp, Activity, Target, Radar, Grid3X3, Plus } from 'lucide-react'

function VisualizationSelector({ onSelectVisualization, currentType, availableTypes = [] }) {
  const visualizationTypes = [
    {
      id: 'table',
      name: 'Tabla',
      icon: Table,
      description: 'Datos en formato tabular',
      color: 'bg-gray-500'
    },
    {
      id: 'kpi_cards',
      name: 'KPI Cards',
      icon: TrendingUp,
      description: 'Indicadores clave',
      color: 'bg-green-500'
    },
    {
      id: 'bar_chart',
      name: 'Barras',
      icon: BarChart3,
      description: 'Comparaciones categóricas',
      color: 'bg-blue-500'
    },
    {
      id: 'line_chart',
      name: 'Líneas',
      icon: LineChart,
      description: 'Tendencias temporales',
      color: 'bg-purple-500'
    },
    {
      id: 'area_chart',
      name: 'Área',
      icon: Activity,
      description: 'Series temporales apiladas',
      color: 'bg-indigo-500'
    },
    {
      id: 'pie_chart',
      name: 'Pastel',
      icon: PieChart,
      description: 'Proporciones y porcentajes',
      color: 'bg-pink-500'
    },
    {
      id: 'scatter_chart',
      name: 'Dispersión',
      icon: Target,
      description: 'Correlaciones entre variables',
      color: 'bg-orange-500'
    },
    {
      id: 'radar_chart',
      name: 'Radar',
      icon: Radar,
      description: 'Comparaciones multidimensionales',
      color: 'bg-cyan-500'
    },
    {
      id: 'heatmap',
      name: 'Mapa de Calor',
      icon: Grid3X3,
      description: 'Patrones en datos tabulares',
      color: 'bg-red-500'
    }
  ]

  // Filtrar tipos disponibles si se especifica
  const typesToShow = availableTypes.length > 0 
    ? visualizationTypes.filter(type => availableTypes.includes(type.id))
    : visualizationTypes

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Seleccionar Visualización</h3>
        <div className="text-sm text-gray-500">
          {typesToShow.length} tipos disponibles
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {typesToShow.map((type) => {
          const Icon = type.icon
          const isSelected = currentType === type.id
          
          return (
            <button
              key={type.id}
              onClick={() => onSelectVisualization(type.id)}
              className={`
                relative p-3 rounded-lg border-2 transition-all duration-200 hover:shadow-md
                ${isSelected 
                  ? 'border-blue-500 bg-blue-50 shadow-md' 
                  : 'border-gray-200 hover:border-gray-300 bg-white'
                }
              `}
            >
              <div className="flex flex-col items-center text-center">
                <div className={`
                  w-8 h-8 rounded-lg flex items-center justify-center mb-2
                  ${isSelected ? type.color : 'bg-gray-100'}
                `}>
                  <Icon className={`w-4 h-4 ${isSelected ? 'text-white' : 'text-gray-600'}`} />
                </div>
                
                <div className="text-xs font-medium text-gray-800 mb-1">
                  {type.name}
                </div>
                
                <div className="text-xs text-gray-500 leading-tight">
                  {type.description}
                </div>
              </div>

              {isSelected && (
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                </div>
              )}
            </button>
          )
        })}
      </div>

      {/* Información adicional */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-start">
          <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center mr-2 mt-0.5">
            <Plus className="w-3 h-3 text-blue-600" />
          </div>
          <div>
            <div className="text-sm font-medium text-gray-800">Tipos de Visualización</div>
            <div className="text-xs text-gray-600 mt-1">
              Selecciona el tipo de gráfico más apropiado para tus datos. 
              El sistema puede sugerir automáticamente el mejor tipo basado en la estructura de los datos.
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VisualizationSelector
