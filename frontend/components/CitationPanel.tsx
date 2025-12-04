'use client'

import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { X } from 'lucide-react'
import type { Citation } from './ChatInterface'

interface CitationPanelProps {
  citation: Citation
  onClose: () => void
}

export default function CitationPanel({ citation, onClose }: CitationPanelProps) {
  return (
    <Card className="w-80 p-4 flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold">引用来源</h3>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
      </div>
      <div className="flex-1 overflow-y-auto space-y-2">
        <div>
          <p className="text-sm font-medium text-muted-foreground">法律条文</p>
          <p className="font-semibold">{citation.article_name}</p>
          {citation.section && (
            <p className="text-sm text-muted-foreground">{citation.section}</p>
          )}
        </div>
        <div>
          <p className="text-sm font-medium text-muted-foreground mb-1">内容</p>
          <p className="text-sm whitespace-pre-wrap">{citation.content}</p>
        </div>
        {citation.url && (
          <div>
            <a
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-primary hover:underline"
            >
              查看原文 →
            </a>
          </div>
        )}
      </div>
    </Card>
  )
}

