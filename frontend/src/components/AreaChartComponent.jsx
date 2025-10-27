import React from 'react'
import { Area, AreaChart, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

function AreaChartComponent({ data }) {
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
        <p className="text-gray-500">No hay columnas numéricas para el gráfico de área</p>
      </div>
    )
  }

  // Colores para las áreas
  const colors = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
  ]

  return (
    <div className="w-full h-full">
      {/* Header */}
      <div className="mb-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800">Gráfico de Área</h3>
        <p className="text-sm text-gray-600">
          {data.length} puntos de datos, {numericColumns.length} series
        </p>
      </div>

      {/* Gráfico */}
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              {numericColumns.map((column, index) => (
                <linearGradient key={column} id={`color${index}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={colors[index % colors.length]} stopOpacity={0.8}/>
                  <stop offset="95%" stopColor={colors[index % colors.length]} stopOpacity={0.1}/>
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis 
              dataKey={Object.keys(chartData[0])[0]} 
              stroke="#6B7280"
              fontSize={12}
            />
            <YAxis stroke="#6B7280" fontSize={12} />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #E5E7EB',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Legend />
            {numericColumns.map((column, index) => (
              <Area
                key={column}
                type="monotone"
                dataKey={column}
                stroke={colors[index % colors.length]}
                fill={`url(#color${index})`}
                strokeWidth={2}
                name={column}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Información adicional */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        {numericColumns.slice(0, 3).map((column, index) => {
          const values = chartData.map(item => item[column]).filter(val => !isNaN(val))
          const sum = values.reduce((a, b) => a + b, 0)
          const avg = sum / values.length
          const max = Math.max(...values)
          const min = Math.min(...values)
          
          return (
            <div key={column} className="bg-gray-50 rounded-lg p-3">
              <h4 className="font-medium text-gray-800 text-sm">{column}</h4>
              <div className="mt-2 space-y-1 text-xs text-gray-600">
                <div>Promedio: {avg.toFixed(2)}</div>
                <div>Máximo: {max.toFixed(2)}</div>
                <div>Mínimo: {min.toFixed(2)}</div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default AreaChartComponent
