'use client'

import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'
import { SyftObject } from '@/lib/types'

interface FileEditorModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  object: SyftObject | null
  fileType: 'private' | 'mock' | null
  onSave?: () => void
}

export function FileEditorModal({ 
  open, 
  onOpenChange, 
  object,
  fileType,
  onSave 
}: FileEditorModalProps) {
  const [filePath, setFilePath] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (open && object && fileType) {
      fetchFilePath()
    }
  }, [open, object, fileType])

  const fetchFilePath = async () => {
    if (!object || !fileType) return
    
    setLoading(true)
    setError('')
    setFilePath(null)
    
    try {
      // Fetch object metadata to get file paths
      const metadata = await api.getObjectMetadata(object.uid)
      const path = metadata.paths[fileType]
      
      if (!path) {
        setError(`No ${fileType} file path found`)
        return
      }
      
      setFilePath(path)
    } catch (err) {
      setError('Failed to load file path')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleIframeLoad = () => {
    // Optional: Handle iframe load event if needed
    // Could potentially listen for save events via postMessage
  }

  const fileName = object ? `${object.name} (${fileType})` : ''
  const editorUrl = filePath ? `http://localhost:8004/editor?path=${encodeURIComponent(filePath)}` : null

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-6xl h-[90vh] flex flex-col p-0" onClose={() => onOpenChange(false)}>
        <DialogHeader className="px-6 py-4 border-b">
          <DialogTitle className="flex items-center justify-between">
            <span>Edit File: {fileName}</span>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onOpenChange(false)}
              className="h-8 w-8 p-0"
            >
              <X className="h-4 w-4" />
            </Button>
          </DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-hidden">
          {error && (
            <div className="m-4 rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {loading ? (
            <div className="h-full flex items-center justify-center">
              <p className="text-gray-500">Loading file editor...</p>
            </div>
          ) : editorUrl ? (
            <iframe
              src={editorUrl}
              className="w-full h-full border-0"
              onLoad={handleIframeLoad}
              title={`File Editor - ${fileName}`}
            />
          ) : (
            <div className="h-full flex items-center justify-center">
              <p className="text-gray-500">No file to edit</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}