import React from 'react'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

function KPICards({ data }) {
  if (!data || !data.cards) {
    return (
      <div className="text-center py-8 text-gray-500">
        No hay datos para mostrar los KPIs
      </div>
    )
  }

  const formatValue = (value, format) => {
    if (format === 'number') {
      return new Intl.NumberFormat('es-ES').format(value)
    }
    if (format === 'currency') {
      return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'USD'
      }).format(value)
    }
    if (format === 'percentage') {
      return `${(value * 100).toFixed(1)}%`
    }
    return value
  }

  const getTrendIcon = (value) => {
    if (value > 0) return <TrendingUp className="w-4 h-4 text-green-500" />
    if (value < 0) return <TrendingDown className="w-4 h-4 text-red-500" />
    return <Minus className="w-4 h-4 text-gray-500" />
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {data.cards.map((card, index) => (
        <div
          key={index}
          className="bg-gradient-to-br from-white to-gray-50 rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-600 uppercase tracking-wide">
              {card.title}
            </h3>
            {getTrendIcon(card.value)}
          </div>
          
          <div className="text-3xl font-bold text-gray-900 mb-2">
            {formatValue(card.value, card.format)}
          </div>
          
          {card.subtitle && (
            <p className="text-sm text-gray-500">
              {card.subtitle}
            </p>
          )}
        </div>
      ))}
    </div>
  )
}

export default KPICards





