import React from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

function HeatmapComponent({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">No hay datos para mostrar</p>
      </div>
    )
  }

  // Obtener las columnas numéricas para el mapa de calor
  const numericColumns = Object.keys(data[0]).filter(key => {
    const value = data[0][key]
    return typeof value === 'number' || !isNaN(parseFloat(value))
  })

  if (numericColumns.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">No hay columnas numéricas para el mapa de calor</p>
      </div>
    )
  }

  // Calcular valores min/max para normalización
  const allValues = data.flatMap(row => 
    numericColumns.map(col => parseFloat(row[col]) || 0)
  )
  const minValue = Math.min(...allValues)
  const maxValue = Math.max(...allValues)
  const range = maxValue - minValue

  // Función para obtener el color basado en el valor
  const getHeatColor = (value) => {
    if (range === 0) return 'bg-gray-200'
    
    const normalized = (value - minValue) / range
    if (normalized < 0.2) return 'bg-red-100'
    if (normalized < 0.4) return 'bg-orange-200'
    if (normalized < 0.6) return 'bg-yellow-200'
    if (normalized < 0.8) return 'bg-green-200'
    return 'bg-green-300'
  }

  // Función para obtener la intensidad del color
  const getIntensity = (value) => {
    if (range === 0) return 'opacity-50'
    
    const normalized = (value - minValue) / range
    if (normalized < 0.2) return 'opacity-60'
    if (normalized < 0.4) return 'opacity-70'
    if (normalized < 0.6) return 'opacity-80'
    if (normalized < 0.8) return 'opacity-90'
    return 'opacity-100'
  }

  return (
    <div className="w-full">
      {/* Header con información */}
      <div className="mb-4 p-3 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">Mapa de Calor</h3>
            <p className="text-sm text-gray-600">
              {data.length} filas × {numericColumns.length} columnas numéricas
            </p>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-600">
              <span className="font-medium">Rango:</span> {minValue.toFixed(2)} - {maxValue.toFixed(2)}
            </div>
          </div>
        </div>
      </div>

      {/* Tabla de mapa de calor */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">
                #
              </th>
              {numericColumns.map((column, index) => (
                <th 
                  key={index}
                  className="border border-gray-300 px-3 py-2 text-center text-sm font-medium text-gray-700 min-w-[100px]"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 20).map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-3 py-2 text-sm font-medium text-gray-600">
                  {rowIndex + 1}
                </td>
                {numericColumns.map((column, colIndex) => {
                  const value = parseFloat(row[column]) || 0
                  const isHigh = value > (minValue + range * 0.7)
                  const isLow = value < (minValue + range * 0.3)
                  
                  return (
                    <td 
                      key={colIndex}
                      className={`border border-gray-300 px-3 py-2 text-center text-sm font-medium ${getHeatColor(value)} ${getIntensity(value)}`}
                    >
                      <div className="flex items-center justify-center">
                        <span className={`${isHigh ? 'text-green-800' : isLow ? 'text-red-800' : 'text-gray-800'}`}>
                          {value.toFixed(2)}
                        </span>
                        {isHigh && <TrendingUp className="w-3 h-3 ml-1 text-green-600" />}
                        {isLow && <TrendingDown className="w-3 h-3 ml-1 text-red-600" />}
                      </div>
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Leyenda */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Leyenda:</span>
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-red-100 rounded mr-2"></div>
              <span className="text-xs text-gray-600">Bajo</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-yellow-200 rounded mr-2"></div>
              <span className="text-xs text-gray-600">Medio</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-300 rounded mr-2"></div>
              <span className="text-xs text-gray-600">Alto</span>
            </div>
          </div>
        </div>
      </div>

      {data.length > 20 && (
        <div className="mt-2 text-center text-sm text-gray-500">
          Mostrando las primeras 20 filas de {data.length} total
        </div>
      )}
    </div>
  )
}

export default HeatmapComponent
