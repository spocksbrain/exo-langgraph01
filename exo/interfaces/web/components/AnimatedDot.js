import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'

// Animation states for the dot
const dotStates = {
  idle: {
    scale: [1, 1.1, 1],
    opacity: 0.8,
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: "easeInOut"
    }
  },
  listening: {
    scale: [1, 1.2, 1],
    opacity: 1,
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: "easeInOut"
    }
  },
  processing: {
    rotate: [0, 360],
    scale: 1,
    opacity: 0.9,
    transition: {
      rotate: {
        duration: 1.5,
        repeat: Infinity,
        ease: "linear"
      }
    }
  },
  speaking: {
    scale: [1, 1.15, 0.9, 1.15, 1],
    opacity: 1,
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: "easeInOut"
    }
  },
  error: {
    scale: [1, 1.2, 0.9, 1.2, 1],
    opacity: 0.9,
    transition: {
      duration: 0.5,
      repeat: 3,
      ease: "easeInOut"
    }
  }
}

const AnimatedDot = ({ state = 'idle', size = 60, color = '#0ea5e9' }) => {
  const [currentState, setCurrentState] = useState(state)
  const prevStateRef = useRef(state)
  
  // Update state with animation
  useEffect(() => {
    if (state !== prevStateRef.current) {
      setCurrentState(state)
      prevStateRef.current = state
    }
  }, [state])
  
  return (
    <div className="flex items-center justify-center">
      <motion.div
        className="rounded-full"
        style={{
          width: size,
          height: size,
          backgroundColor: color,
          boxShadow: `0 0 15px ${color}`
        }}
        animate={dotStates[currentState]}
        initial={{ scale: 0 }}
        whileHover={{ scale: 1.2 }}
      />
    </div>
  )
}

export default AnimatedDot
