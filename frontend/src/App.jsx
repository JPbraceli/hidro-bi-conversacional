import React, { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import VisualizationPanel from './components/VisualizationPanel'
import Header from './components/Header'

function App() {
  const [queryData, setQueryData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleExecuteQuery = (data) => {
    setQueryData(data)
  }

  const handleReset = () => {
    setQueryData(null)
  }

  return (
    <div className="h-screen flex flex-col bg-white">
      <Header />
      <ChatInterface 
        onExecuteQuery={handleExecuteQuery}
        onReset={handleReset}
      />
    </div>
  )
}

export default App
