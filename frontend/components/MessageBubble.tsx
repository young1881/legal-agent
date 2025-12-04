'use client'

import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { Citation } from './ChatInterface'

interface MessageBubbleProps {
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    citations?: Citation[]
    sources?: any[]
  }
  onCitationClick: (citation: Citation) => void
}

export default function MessageBubble({ message, onCitationClick }: MessageBubbleProps) {
  // 提取引用标记并渲染
  const renderContent = () => {
    if (message.role === 'user') {
      return <p>{message.content}</p>
    }

    // 匹配 [[source_id]] 格式
    const parts = message.content.split(/(\[\[[^\]]+\]\])/g)
    
    return (
      <div>
        {parts.map((part, index) => {
          if (part.match(/\[\[([^\]]+)\]\]/)) {
            const sourceId = part.match(/\[\[([^\]]+)\]\]/)?.[1]
            const citation = message.citations?.find(c => c.source_id === sourceId)
            
            if (citation) {
              return (
                <button
                  key={index}
                  onClick={() => onCitationClick(citation)}
                  className="text-primary hover:underline font-medium"
                >
                  {part}
                </button>
              )
            }
          }
          return <span key={index}>{part}</span>
        })}
      </div>
    )
  }

  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
      <Card className={`max-w-[80%] p-4 ${
        message.role === 'user' 
          ? 'bg-primary text-primary-foreground' 
          : 'bg-secondary'
      }`}>
        {renderContent()}
        {message.citations && message.citations.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {message.citations.map((citation) => (
              <Badge
                key={citation.source_id}
                variant="outline"
                className="cursor-pointer hover:bg-accent"
                onClick={() => onCitationClick(citation)}
              >
                {citation.article_name} {citation.section}
              </Badge>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}

