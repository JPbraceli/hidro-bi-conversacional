import React, { useState, useRef, useEffect } from 'react'
import { Send, RotateCcw, Loader2 } from 'lucide-react'
import VisualizationPanel from './VisualizationPanel'

function ChatInterface({ onExecuteQuery, onReset }) {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isReadyToExecute, setIsReadyToExecute] = useState(false)
  const [currentQuerySummary, setCurrentQuerySummary] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const typeMessage = (text, callback) => {
    setIsTyping(true)
    let index = 0
    const typingSpeed = 25 // Velocidad de escritura en ms
    
    const typeInterval = setInterval(() => {
      if (index < text.length) {
        callback(text.substring(0, index + 1))
        index++
        
        // Scroll automático mientras escribe
        setTimeout(() => scrollToBottom(), 10)
      } else {
        clearInterval(typeInterval)
        setIsTyping(false)
        // Scroll final
        setTimeout(() => scrollToBottom(), 100)
      }
    }, typingSpeed)
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = inputMessage.trim()
    setInputMessage('')
    setIsLoading(true)

    // Agregar mensaje del usuario
    const newMessages = [...messages, { role: 'user', content: userMessage }]
    setMessages(newMessages)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage,
          conversation_id: conversationId
        })
      })

      if (!response.ok) {
        throw new Error(`Error del servidor: ${response.status}`)
      }

      const data = await response.json()

      // Actualizar conversation ID
      if (data.conversation_id) {
        setConversationId(data.conversation_id)
      }

      // Agregar mensaje del asistente vacío primero
      const assistantMessage = { 
        role: 'assistant', 
        content: '',
        suggestions: data.suggestions || [],
        isReady: data.is_ready || false,
        isTyping: true
      }
      const updatedMessages = [...newMessages, assistantMessage]
      setMessages(updatedMessages)

      // Escribir la respuesta progresivamente
      typeMessage(data.response, (partialText) => {
        setMessages(prev => {
          const newMessages = [...prev]
          const lastMessage = newMessages[newMessages.length - 1]
          if (lastMessage.role === 'assistant') {
            lastMessage.content = partialText
            lastMessage.isTyping = partialText.length < data.response.length
          }
          return newMessages
        })
      })

      // Si la IA está lista para ejecutar, ejecutar automáticamente
      if (data.is_ready) {
        setTimeout(() => {
          handleExecuteQuery()
        }, 1000) // Esperar 1 segundo antes de ejecutar
      }

    } catch (error) {
      const errorMessages = [...newMessages, { 
        role: 'assistant', 
        content: `Error: ${error.message}`,
        isError: true
      }]
      setMessages(errorMessages)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion)
  }

  const handleExecuteQuery = async () => {
    setIsLoading(true)
    
    // Agregar mensaje de "ejecutando consulta"
    const executingMessage = {
      role: 'assistant',
      content: 'Ejecutando consulta...',
      isExecuting: true
    }
    setMessages(prev => [...prev, executingMessage])
    
    try {
      const response = await fetch('/api/execute-chat-query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (!response.ok) {
        throw new Error(`Error del servidor: ${response.status}`)
      }

      const data = await response.json()

      if (data.error) {
        throw new Error(data.error)
      }

      // Reemplazar el mensaje de "ejecutando" con los resultados
      setMessages(prev => {
        const newMessages = [...prev]
        const lastMessage = newMessages[newMessages.length - 1]
        if (lastMessage.isExecuting) {
          lastMessage.content = 'Consulta ejecutada exitosamente'
          lastMessage.isExecuting = false
          lastMessage.visualizationData = data
        }
        return newMessages
      })

    } catch (error) {
      // Reemplazar el mensaje de "ejecutando" con el error
      setMessages(prev => {
        const newMessages = [...prev]
        const lastMessage = newMessages[newMessages.length - 1]
        if (lastMessage.isExecuting) {
          lastMessage.content = `Error ejecutando consulta: ${error.message}`
          lastMessage.isExecuting = false
          lastMessage.isError = true
        }
        return newMessages
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = async () => {
    try {
      await fetch('/api/reset-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      setMessages([])
      setIsReadyToExecute(false)
      setCurrentQuerySummary('')
      setConversationId(null)
      onReset()
    } catch (error) {
      console.error('Error reseteando chat:', error)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex flex-col flex-1 bg-white">
      {/* Header del chat */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg flex items-center justify-center mr-3">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900">
              Asistente de Consultas HIDRO
            </h2>
            <p className="text-sm text-gray-600">
              Conversa conmigo para formular tu consulta perfecta
            </p>
          </div>
        </div>
        <button
          onClick={handleReset}
          className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <RotateCcw className="w-4 h-4 mr-1 inline" />
          Reiniciar
        </button>
      </div>

      {/* Área de mensajes */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar min-h-0">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <p className="text-lg font-medium mb-2">¡Hola! Soy tu asistente HIDRO</p>
            <p className="text-sm">Pregúntame sobre actividades, contratos, usuarios, gateways o administración</p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} px-4`}>
                <div className={`chat-bubble ${
                  message.role === 'user' 
                    ? 'chat-bubble-user' 
                    : message.isError 
                      ? 'chat-bubble-error'
                      : 'chat-bubble-assistant'
                }`}>
                  <p className="text-sm whitespace-pre-wrap">
                    {message.content}
                  </p>
                  
                  {/* Sugerencias */}
                  {message.suggestions && message.suggestions.length > 0 && (
                    <div className="mt-3 space-y-2">
                      <p className="text-xs font-medium text-gray-600">Sugerencias:</p>
                      <div className="flex flex-wrap gap-2">
                        {message.suggestions.map((suggestion, idx) => (
                          <button
                            key={idx}
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="px-3 py-1 text-xs bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-colors"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Visualización de datos */}
                  {message.visualizationData && (
                    <div className="mt-4">
                      <VisualizationPanel 
                        data={message.visualizationData}
                        isLoading={false}
                        embedded={true}
                      />
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {/* Indicador de carga */}
            {isLoading && !isTyping && (
              <div className="flex justify-start">
                <div className="chat-bubble chat-bubble-assistant">
                  <div className="flex items-center">
                    <div className="flex space-x-1 mr-3">
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-sm">Pensando...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input de mensaje - Fijo en la parte inferior */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex space-x-3">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-200"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            {isLoading ? (
              <Loader2 className="animate-spin h-5 w-5" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>

    </div>
  )
}

export default ChatInterface
