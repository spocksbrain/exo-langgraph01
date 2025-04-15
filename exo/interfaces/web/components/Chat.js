import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import { motion } from 'framer-motion'

// Message component for displaying individual messages
const Message = ({ message, isUser }) => {
  return (
    <motion.div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div
        className={`px-4 py-3 rounded-lg max-w-[80%] ${
          isUser
            ? 'bg-primary-600 text-white rounded-tr-none'
            : 'bg-gray-100 dark:bg-gray-800 rounded-tl-none'
        }`}
      >
        {isUser ? (
          <p className="text-sm">{message.content}</p>
        ) : (
          <div className="prose dark:prose-invert prose-sm max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-primary-200' : 'text-gray-500'
          }`}
        >
          {isUser ? 'You' : message.from_agent || 'exo'}
        </div>
      </div>
    </motion.div>
  )
}

// Main Chat component
const Chat = ({ onSendMessage, dotState, setDotState }) => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef(null)
  const wsRef = useRef(null)

  // Connect to WebSocket
  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket(`ws://${window.location.host}/ws`)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
        setDotState('idle')
      }
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        console.log('WebSocket message:', data)
        
        if (data.type === 'response') {
          setMessages((prev) => [
            ...prev,
            {
              id: Date.now(),
              content: data.data.response || data.data.content,
              from_agent: data.data.handled_by || data.data.from_agent,
              isUser: false,
            },
          ])
          setIsProcessing(false)
          setDotState('idle')
        } else if (data.type === 'error') {
          setMessages((prev) => [
            ...prev,
            {
              id: Date.now(),
              content: `Error: ${data.data.error}`,
              from_agent: 'system',
              isUser: false,
            },
          ])
          setIsProcessing(false)
          setDotState('error')
          
          // Reset to idle after error
          setTimeout(() => {
            setDotState('idle')
          }, 2000)
        }
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setIsConnected(false)
        setDotState('error')
        
        // Try to reconnect after 2 seconds
        setTimeout(() => {
          connectWebSocket()
        }, 2000)
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setDotState('error')
      }
      
      wsRef.current = ws
    }
    
    connectWebSocket()
    
    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [setDotState])

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!input.trim() || !isConnected || isProcessing) return
    
    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      content: input,
      isUser: true,
    }
    
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsProcessing(true)
    setDotState('processing')
    
    // Send message to WebSocket
    if (wsRef.current) {
      wsRef.current.send(
        JSON.stringify({
          type: 'user_input',
          data: {
            text: input,
            metadata: {
              timestamp: Date.now(),
            },
          },
        })
      )
    }
    
    // Also call the onSendMessage prop if provided
    if (onSendMessage) {
      onSendMessage(input)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Start a conversation with exo</p>
          </div>
        ) : (
          messages.map((message) => (
            <Message
              key={message.id}
              message={message}
              isUser={message.isUser}
            />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-200 dark:border-gray-800 p-4"
      >
        <div className="flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 px-4 py-2 rounded-l-lg border border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-800"
            disabled={!isConnected || isProcessing}
          />
          <button
            type="submit"
            className={`px-4 py-2 rounded-r-lg bg-primary-600 text-white ${
              !isConnected || isProcessing || !input.trim()
                ? 'opacity-50 cursor-not-allowed'
                : 'hover:bg-primary-700'
            }`}
            disabled={!isConnected || isProcessing || !input.trim()}
          >
            Send
          </button>
        </div>
        
        <div className="flex justify-between mt-2 text-xs text-gray-500">
          <span>
            {isConnected ? (
              <span className="text-green-500">Connected</span>
            ) : (
              <span className="text-red-500">Disconnected</span>
            )}
          </span>
          {isProcessing && <span>Processing...</span>}
        </div>
      </form>
    </div>
  )
}

export default Chat
