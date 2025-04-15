import { useState } from 'react'
import Head from 'next/head'
import AnimatedDot from '../components/AnimatedDot'
import Chat from '../components/Chat'

export default function Home() {
  const [dotState, setDotState] = useState('idle')

  return (
    <div className="flex flex-col min-h-screen">
      <Head>
        <title>exo - Multi-Agent System</title>
        <meta name="description" content="exo multi-agent AI system" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white dark:bg-gray-900 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              <span className="text-primary-600">exo</span> Multi-Agent System
            </h1>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {dotState === 'idle' && 'Ready'}
                {dotState === 'listening' && 'Listening'}
                {dotState === 'processing' && 'Processing'}
                {dotState === 'speaking' && 'Speaking'}
                {dotState === 'error' && 'Error'}
              </div>
              <AnimatedDot state={dotState} size={40} />
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white dark:bg-gray-900 shadow rounded-lg h-[calc(100vh-12rem)]">
          <Chat dotState={dotState} setDotState={setDotState} />
        </div>
      </main>

      <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500 dark:text-gray-400">
            <p>
              exo Multi-Agent System - Proof of Concept
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
