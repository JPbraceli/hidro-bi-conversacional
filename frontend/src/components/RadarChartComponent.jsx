import React from 'react'
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts'

function RadarChartComponent({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">No hay datos para mostrar</p>
      </div>
    )
  }

  // Preparar datos para el gráfico
  const chartData = data.map((item, index) => {
    const processedItem = { ...item }
    
    // Convertir valores numéricos
    Object.keys(processedItem).forEach(key => {
      const value = processedItem[key]
      if (typeof value === 'string' && !isNaN(parseFloat(value))) {
        processedItem[key] = parseFloat(value)
      }
    })
    
    return processedItem
  })

  // Obtener columnas numéricas
  const numericColumns = Object.keys(chartData[0]).filter(key => {
    const value = chartData[0][key]
    return typeof value === 'number' && !isNaN(value)
  })

  if (numericColumns.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">No hay columnas numéricas para el gráfico de radar</p>
      </div>
    )
  }

  // Colores para las series
  const colors = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
  ]

  // Si hay múltiples filas, crear una serie por fila
  // Si hay una sola fila, mostrar los valores como categorías
  const isMultipleSeries = chartData.length > 1

  let radarData = []
  let seriesData = []

  if (isMultipleSeries) {
    // Múltiples series (una por fila)
    seriesData = chartData.map((row, index) => ({
      name: `Serie ${index + 1}`,
      data: numericColumns.map(col => ({ category: col, value: row[col] }))
    }))
    
    // Crear datos para el radar chart
    radarData = numericColumns.map(category => {
      const dataPoint = { category }
      chartData.forEach((row, index) => {
        dataPoint[`Serie ${index + 1}`] = row[category]
      })
      return dataPoint
    })
  } else {
    // Una sola serie con categorías
    const row = chartData[0]
    seriesData = [{
      name: 'Valores',
      data: numericColumns.map(col => ({ category: col, value: row[col] }))
    }]
    
    radarData = numericColumns.map(category => ({
      category,
      'Valores': row[category]
    }))
  }

  return (
    <div className="w-full h-full">
      {/* Header */}
      <div className="mb-4 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800">Gráfico de Radar</h3>
        <p className="text-sm text-gray-600">
          {isMultipleSeries ? `${chartData.length} series` : '1 serie'} • {numericColumns.length} categorías
        </p>
      </div>

      {/* Gráfico */}
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={radarData} margin={{ top: 20, right: 80, bottom: 20, left: 20 }}>
            <PolarGrid stroke="#E5E7EB" />
            <PolarAngleAxis 
              dataKey="category" 
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <PolarRadiusAxis 
              angle={90} 
              domain={[0, 'dataMax']} 
              tick={{ fontSize: 10, fill: '#6B7280' }}
            />
            {seriesData.map((series, index) => (
              <Radar
                key={series.name}
                name={series.name}
                dataKey={series.name}
                stroke={colors[index % colors.length]}
                fill={colors[index % colors.length]}
                fillOpacity={0.3}
                strokeWidth={2}
              />
            ))}
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Información de las series */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {seriesData.map((series, index) => {
          const values = series.data.map(item => item.value).filter(val => !isNaN(val))
          const sum = values.reduce((a, b) => a + b, 0)
          const avg = sum / values.length
          const max = Math.max(...values)
          const min = Math.min(...values)
          
          return (
            <div key={series.name} className="bg-gray-50 rounded-lg p-3">
              <h4 className="font-medium text-gray-800 text-sm flex items-center">
                <div 
                  className="w-3 h-3 rounded-full mr-2" 
                  style={{ backgroundColor: colors[index % colors.length] }}
                ></div>
                {series.name}
              </h4>
              <div className="mt-2 space-y-1 text-xs text-gray-600">
                <div>Promedio: {avg.toFixed(2)}</div>
                <div>Máximo: {max.toFixed(2)}</div>
                <div>Mínimo: {min.toFixed(2)}</div>
                <div>Total: {sum.toFixed(2)}</div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Categorías */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-800 text-sm mb-2">Categorías Analizadas</h4>
        <div className="flex flex-wrap gap-2">
          {numericColumns.map((category, index) => (
            <span 
              key={category}
              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
            >
              {category}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

export default RadarChartComponent
