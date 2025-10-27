import React from 'react'
import { Scatter, ScatterChart, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

function ScatterChartComponent({ data }) {
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

  if (numericColumns.length < 2) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">Se necesitan al menos 2 columnas numéricas para el gráfico de dispersión</p>
      </div>
    )
  }

  // Usar las primeras dos columnas numéricas como X e Y
  const xColumn = numericColumns[0]
  const yColumn = numericColumns[1]
  const colorColumn = numericColumns[2] || numericColumns[0] // Tercera columna para color, o primera si no hay tercera

  // Colores para los puntos
  const colors = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
  ]

  // Función para obtener el color basado en el valor
  const getPointColor = (value) => {
    if (numericColumns.length < 3) return colors[0]
    
    const values = chartData.map(item => item[colorColumn]).filter(val => !isNaN(val))
    const minVal = Math.min(...values)
    const maxVal = Math.max(...values)
    const range = maxVal - minVal
    
    if (range === 0) return colors[0]
    
    const normalized = (value - minVal) / range
    const colorIndex = Math.floor(normalized * (colors.length - 1))
    return colors[colorIndex]
  }

  return (
    <div className="w-full h-full">
      {/* Header */}
      <div className="mb-4 p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800">Gráfico de Dispersión</h3>
        <p className="text-sm text-gray-600">
          {data.length} puntos • X: {xColumn} • Y: {yColumn}
          {numericColumns.length > 2 && ` • Color: ${colorColumn}`}
        </p>
      </div>

      {/* Gráfico */}
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis 
              type="number" 
              dataKey={xColumn} 
              name={xColumn}
              stroke="#6B7280"
              fontSize={12}
            />
            <YAxis 
              type="number" 
              dataKey={yColumn} 
              name={yColumn}
              stroke="#6B7280"
              fontSize={12}
            />
            <Tooltip 
              cursor={{ strokeDasharray: '3 3' }}
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #E5E7EB',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Scatter dataKey={yColumn} fill="#3B82F6">
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={getPointColor(entry[colorColumn])} 
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* Estadísticas */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-50 rounded-lg p-3">
          <h4 className="font-medium text-gray-800 text-sm">Eje X: {xColumn}</h4>
          <div className="mt-2 space-y-1 text-xs text-gray-600">
            {(() => {
              const values = chartData.map(item => item[xColumn]).filter(val => !isNaN(val))
              const sum = values.reduce((a, b) => a + b, 0)
              const avg = sum / values.length
              const max = Math.max(...values)
              const min = Math.min(...values)
              return (
                <>
                  <div>Promedio: {avg.toFixed(2)}</div>
                  <div>Rango: {min.toFixed(2)} - {max.toFixed(2)}</div>
                </>
              )
            })()}
          </div>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-3">
          <h4 className="font-medium text-gray-800 text-sm">Eje Y: {yColumn}</h4>
          <div className="mt-2 space-y-1 text-xs text-gray-600">
            {(() => {
              const values = chartData.map(item => item[yColumn]).filter(val => !isNaN(val))
              const sum = values.reduce((a, b) => a + b, 0)
              const avg = sum / values.length
              const max = Math.max(...values)
              const min = Math.min(...values)
              return (
                <>
                  <div>Promedio: {avg.toFixed(2)}</div>
                  <div>Rango: {min.toFixed(2)} - {max.toFixed(2)}</div>
                </>
              )
            })()}
          </div>
        </div>
      </div>

      {/* Leyenda de colores */}
      {numericColumns.length > 2 && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <h4 className="font-medium text-gray-800 text-sm mb-2">Leyenda de Colores</h4>
          <div className="text-xs text-gray-600">
            Los colores representan los valores de <strong>{colorColumn}</strong>
          </div>
        </div>
      )}
    </div>
  )
}

export default ScatterChartComponent
