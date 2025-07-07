'use client'

import { Copy, Check, FolderOpen } from 'lucide-react'
import { useState } from 'react'
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
  DialogDescription 
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { SyftObject } from '@/lib/types'

interface PathModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  object: SyftObject | null
}

export function PathModal({ open, onOpenChange, object }: PathModalProps) {
  const [copiedPath, setCopiedPath] = useState<string | null>(null)

  const copyToClipboard = async (text: string, pathType: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedPath(pathType)
      setTimeout(() => setCopiedPath(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  if (!object) return null

  // Extract paths from syft URLs
  const extractPath = (syftUrl: string) => {
    // syft://datasite@email.com/objects/uid/file.ext
    const match = syftUrl.match(/syft:\/\/[^\/]+(\/.*)/)
    return match ? match[1] : syftUrl
  }

  const privatePath = object.files.private?.syft_url 
    ? extractPath(object.files.private.syft_url)
    : null
    
  const mockPath = object.files.mock?.syft_url 
    ? extractPath(object.files.mock.syft_url)
    : null

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-xl" onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FolderOpen className="h-5 w-5" />
            Object Paths
          </DialogTitle>
          <DialogDescription>
            File system paths for {object.name}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {privatePath && (
            <div className="space-y-2">
              <p className="text-sm font-medium">Private File Path</p>
              <div className="flex items-center gap-2 p-3 bg-blue-50 rounded-lg">
                <code className="text-xs flex-1 font-mono break-all">{privatePath}</code>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => copyToClipboard(privatePath, 'private')}
                >
                  {copiedPath === 'private' ? (
                    <Check className="h-3 w-3" />
                  ) : (
                    <Copy className="h-3 w-3" />
                  )}
                </Button>
              </div>
            </div>
          )}
          
          {mockPath && (
            <div className="space-y-2">
              <p className="text-sm font-medium">Mock File Path</p>
              <div className="flex items-center gap-2 p-3 bg-green-50 rounded-lg">
                <code className="text-xs flex-1 font-mono break-all">{mockPath}</code>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => copyToClipboard(mockPath, 'mock')}
                >
                  {copiedPath === 'mock' ? (
                    <Check className="h-3 w-3" />
                  ) : (
                    <Copy className="h-3 w-3" />
                  )}
                </Button>
              </div>
            </div>
          )}
          
          {!privatePath && !mockPath && (
            <p className="text-sm text-gray-500 text-center py-4">
              No file paths available for this object
            </p>
          )}
          
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-600">
              <strong>Note:</strong> These are relative paths within the SyftBox datasite. 
              The actual file system location depends on your SyftBox configuration.
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}