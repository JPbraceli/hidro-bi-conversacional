/**
 * Utilidades para comunicación con la API
 */

const API_BASE_URL = '/api'

export const api = {
  // Chat endpoints
  async sendMessage(message, conversationId = null) {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      })
    })
    
    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.status}`)
    }
    
    return response.json()
  },

  async executeQuery() {
    const response = await fetch(`${API_BASE_URL}/execute-chat-query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.status}`)
    }
    
    return response.json()
  },

  async resetChat() {
    const response = await fetch(`${API_BASE_URL}/reset-chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.status}`)
    }
    
    return response.json()
  },

  async getSuggestions() {
    const response = await fetch(`${API_BASE_URL}/suggestions`)
    
    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.status}`)
    }
    
    return response.json()
  }
}

export default api





