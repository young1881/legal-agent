'use client'

import { useState } from 'react'
import ChatInterface from '@/components/ChatInterface'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="w-full max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2">法学AI-Agent</h1>
          <p className="text-muted-foreground">基于RAG的智能法律助手</p>
        </div>
        <ChatInterface />
      </div>
    </main>
  )
}

