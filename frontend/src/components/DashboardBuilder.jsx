import React, { useState, useRef } from 'react'
import { 
  Plus, 
  Trash2, 
  Move, 
  Settings, 
  Download, 
  Save, 
  Eye,
  Grid3X3,
  Maximize2,
  Minimize2
} from 'lucide-react'
import VisualizationPanel from './VisualizationPanel'
import VisualizationSelector from './VisualizationSelector'

function DashboardBuilder({ data, onSave, onExport }) {
  const [widgets, setWidgets] = useState([])
  const [selectedWidget, setSelectedWidget] = useState(null)
  const [isAddingWidget, setIsAddingWidget] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const dashboardRef = useRef(null)

  const addWidget = (type) => {
    const newWidget = {
      id: Date.now(),
      type,
      title: `Widget ${widgets.length + 1}`,
      position: { x: 0, y: 0 },
      size: { width: 300, height: 200 },
      data: data,
      settings: {}
    }
    
    setWidgets([...widgets, newWidget])
    setSelectedWidget(newWidget.id)
    setIsAddingWidget(false)
  }

  const removeWidget = (id) => {
    setWidgets(widgets.filter(w => w.id !== id))
    if (selectedWidget === id) {
      setSelectedWidget(null)
    }
  }

  const updateWidget = (id, updates) => {
    setWidgets(widgets.map(w => 
      w.id === id ? { ...w, ...updates } : w
    ))
  }

  const duplicateWidget = (id) => {
    const widget = widgets.find(w => w.id === id)
    if (widget) {
      const newWidget = {
        ...widget,
        id: Date.now(),
        title: `${widget.title} (Copia)`,
        position: { 
          x: widget.position.x + 20, 
          y: widget.position.y + 20 
        }
      }
      setWidgets([...widgets, newWidget])
    }
  }

  const exportDashboard = () => {
    const dashboardData = {
      widgets,
      metadata: {
        created: new Date().toISOString(),
        version: '1.0'
      }
    }
    
    if (onExport) {
      onExport(dashboardData)
    } else {
      // Exportar como JSON
      const dataStr = JSON.stringify(dashboardData, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'dashboard.json'
      link.click()
      URL.revokeObjectURL(url)
    }
  }

  const saveDashboard = () => {
    if (onSave) {
      onSave(widgets)
    }
  }

  return (
    <div className={`${isFullscreen ? 'fixed inset-0 z-50 bg-white' : 'w-full h-full'} flex flex-col`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center space-x-4">
          <div className="flex items-center">
            <Grid3X3 className="w-5 h-5 text-blue-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-800">Dashboard Builder</h2>
          </div>
          <div className="text-sm text-gray-500">
            {widgets.length} widgets
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsAddingWidget(!isAddingWidget)}
            className="flex items-center px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4 mr-2" />
            Agregar Widget
          </button>

          <button
            onClick={saveDashboard}
            className="flex items-center px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Save className="w-4 h-4 mr-2" />
            Guardar
          </button>

          <button
            onClick={exportDashboard}
            className="flex items-center px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Download className="w-4 h-4 mr-2" />
            Exportar
          </button>

          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="flex items-center px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      <div className="flex-1 flex">
        {/* Sidebar - Selector de visualizaciones */}
        {isAddingWidget && (
          <div className="w-80 border-r border-gray-200 bg-gray-50 p-4 overflow-y-auto">
            <VisualizationSelector
              onSelectVisualization={addWidget}
              availableTypes={['table', 'kpi_cards', 'bar_chart', 'line_chart', 'area_chart', 'pie_chart', 'scatter_chart', 'radar_chart', 'heatmap']}
            />
          </div>
        )}

        {/* Canvas del dashboard */}
        <div className="flex-1 relative bg-gray-100 overflow-auto">
          <div 
            ref={dashboardRef}
            className="relative min-h-full p-4"
            style={{ minHeight: '600px' }}
          >
            {widgets.length === 0 ? (
              <div className="flex items-center justify-center h-96">
                <div className="text-center">
                  <Grid3X3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-600 mb-2">
                    Dashboard Vacío
                  </h3>
                  <p className="text-gray-500 mb-4">
                    Agrega widgets para comenzar a construir tu dashboard
                  </p>
                  <button
                    onClick={() => setIsAddingWidget(true)}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors mx-auto"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Agregar Primer Widget
                  </button>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {widgets.map((widget) => (
                  <div
                    key={widget.id}
                    className={`
                      relative bg-white rounded-lg border-2 shadow-lg transition-all duration-200
                      ${selectedWidget === widget.id 
                        ? 'border-blue-500 shadow-xl' 
                        : 'border-gray-200 hover:border-gray-300'
                      }
                    `}
                    style={{
                      minHeight: widget.size.height,
                      minWidth: widget.size.width
                    }}
                    onClick={() => setSelectedWidget(widget.id)}
                  >
                    {/* Header del widget */}
                    <div className="flex items-center justify-between p-3 border-b border-gray-200 bg-gray-50 rounded-t-lg">
                      <div className="flex items-center">
                        <h4 className="font-medium text-gray-800 text-sm">
                          {widget.title}
                        </h4>
                        <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                          {widget.type}
                        </span>
                      </div>
                      
                      <div className="flex items-center space-x-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            duplicateWidget(widget.id)
                          }}
                          className="p-1 text-gray-500 hover:text-gray-700 hover:bg-gray-200 rounded"
                          title="Duplicar"
                        >
                          <Plus className="w-3 h-3" />
                        </button>
                        
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            removeWidget(widget.id)
                          }}
                          className="p-1 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded"
                          title="Eliminar"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    </div>

                    {/* Contenido del widget */}
                    <div className="p-3">
                      <VisualizationPanel 
                        data={{
                          ...data,
                          visualization_type: widget.type
                        }}
                        embedded={true}
                      />
                    </div>

                    {/* Indicador de selección */}
                    {selectedWidget === widget.id && (
                      <div className="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer con información */}
      <div className="border-t border-gray-200 bg-white p-3">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div>
            Dashboard Builder v1.0 • {widgets.length} widgets
          </div>
          <div>
            Arrastra y organiza tus widgets para crear el dashboard perfecto
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardBuilder
