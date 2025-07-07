'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { X, Save, Copy, Check } from 'lucide-react'
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
  DialogFooter 
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'
import { SyftObject } from '@/lib/types'

// Dynamically import Monaco to avoid SSR issues
const MonacoEditor = dynamic(
  () => import('@monaco-editor/react'),
  { 
    ssr: false,
    loading: () => <div className="h-96 flex items-center justify-center">Loading editor...</div>
  }
)

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
  const [content, setContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (open && object && fileType) {
      fetchFileContent()
    }
  }, [open, object, fileType])

  const fetchFileContent = async () => {
    if (!object || !fileType) return
    
    setLoading(true)
    setError('')
    
    try {
      const fileInfo = object.files[fileType]
      if (fileInfo?.syft_url) {
        const content = await api.getFileContent(fileInfo.syft_url)
        setContent(content)
        setOriginalContent(content)
      }
    } catch (err) {
      setError('Failed to load file content')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!object || !fileType) return
    
    setSaving(true)
    setError('')
    
    try {
      await api.updateFile(object.uid, fileType, content)
      setOriginalContent(content)
      if (onSave) {
        onSave()
      }
      onOpenChange(false)
    } catch (err) {
      setError('Failed to save file')
      console.error(err)
    } finally {
      setSaving(false)
    }
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const hasChanges = content !== originalContent
  const fileName = object ? `${object.name} (${fileType})` : ''

  // Detect file type for syntax highlighting
  const getLanguage = () => {
    if (!object || !fileType) return 'plaintext'
    const fileInfo = object.files[fileType]
    const filename = fileInfo?.filename || ''
    
    if (filename.endsWith('.py')) return 'python'
    if (filename.endsWith('.js')) return 'javascript'
    if (filename.endsWith('.ts')) return 'typescript'
    if (filename.endsWith('.json')) return 'json'
    if (filename.endsWith('.yaml') || filename.endsWith('.yml')) return 'yaml'
    if (filename.endsWith('.md')) return 'markdown'
    if (filename.endsWith('.html')) return 'html'
    if (filename.endsWith('.css')) return 'css'
    
    return 'plaintext'
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl h-[80vh] flex flex-col" onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle className="flex items-center justify-between">
            <span>Edit File: {fileName}</span>
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={handleCopy}
              >
                {copied ? (
                  <>
                    <Check className="h-4 w-4 mr-1" />
                    Copied
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4 mr-1" />
                    Copy
                  </>
                )}
              </Button>
            </div>
          </DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-hidden">
          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {loading ? (
            <div className="h-full flex items-center justify-center">
              <p className="text-gray-500">Loading file content...</p>
            </div>
          ) : (
            <MonacoEditor
              height="100%"
              language={getLanguage()}
              value={content}
              onChange={(value) => setContent(value || '')}
              theme="vs-light"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                wordWrap: 'on',
                scrollBeyondLastLine: false,
              }}
            />
          )}
        </div>

        <DialogFooter className="mt-4">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleSave}
            disabled={saving || !hasChanges}
          >
            {saving ? (
              'Saving...'
            ) : (
              <>
                <Save className="h-4 w-4 mr-1" />
                Save Changes
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}