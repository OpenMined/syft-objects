'use client'

import { useState, useEffect } from 'react'
import { Copy, Check, FileText, Shield, User, Calendar, Hash } from 'lucide-react'
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
  DialogDescription 
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { SyftObject } from '@/lib/types'
import { cn } from '@/lib/utils'

interface ObjectInfoModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  object: SyftObject | null
}

export function ObjectInfoModal({ open, onOpenChange, object }: ObjectInfoModalProps) {
  const [copiedField, setCopiedField] = useState<string | null>(null)

  const copyToClipboard = async (text: string, field: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedField(field)
      setTimeout(() => setCopiedField(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  if (!object) return null

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl" onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle>Object Information</DialogTitle>
          <DialogDescription>
            Detailed information about {object.name}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Basic Information */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase text-gray-500">Basic Information</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <p className="text-sm text-gray-500">Name</p>
                <p className="font-medium">{object.name}</p>
              </div>
              
              <div className="space-y-1">
                <p className="text-sm text-gray-500">UID</p>
                <div className="flex items-center gap-2">
                  <p className="font-mono text-sm">{object.uid}</p>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(object.uid, 'uid')}
                  >
                    {copiedField === 'uid' ? (
                      <Check className="h-3 w-3" />
                    ) : (
                      <Copy className="h-3 w-3" />
                    )}
                  </Button>
                </div>
              </div>
            </div>

            <div className="space-y-1">
              <p className="text-sm text-gray-500">Description</p>
              <p className="text-sm">{object.description || 'No description provided'}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <p className="text-sm text-gray-500">Owner</p>
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4 text-gray-400" />
                  <p className="text-sm">{object.email}</p>
                </div>
              </div>
              
              <div className="space-y-1">
                <p className="text-sm text-gray-500">Created</p>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-gray-400" />
                  <p className="text-sm">{formatDate(object.created_at)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Files */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase text-gray-500">Files</h3>
            
            <div className="space-y-3">
              {object.files.private?.exists && (
                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileText className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="font-medium text-sm">Private File</p>
                      <p className="text-xs text-gray-600">
                        {object.files.private.filename || 'private.dat'} • {object.files.private.size} bytes
                      </p>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(object.files.private?.syft_url || '', 'private_url')}
                  >
                    {copiedField === 'private_url' ? (
                      <Check className="h-3 w-3" />
                    ) : (
                      <Copy className="h-3 w-3" />
                    )}
                  </Button>
                </div>
              )}
              
              {object.files.mock?.exists && (
                <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileText className="h-5 w-5 text-green-600" />
                    <div>
                      <p className="font-medium text-sm">Mock File</p>
                      <p className="text-xs text-gray-600">
                        {object.files.mock.filename || 'mock.dat'} • {object.files.mock.size} bytes
                      </p>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(object.files.mock?.syft_url || '', 'mock_url')}
                  >
                    {copiedField === 'mock_url' ? (
                      <Check className="h-3 w-3" />
                    ) : (
                      <Copy className="h-3 w-3" />
                    )}
                  </Button>
                </div>
              )}
              
              {!object.files.private?.exists && !object.files.mock?.exists && (
                <p className="text-sm text-gray-500">No files attached to this object</p>
              )}
            </div>
          </div>

          {/* Permissions */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase text-gray-500">Permissions</h3>
            
            <div className="space-y-3">
              {Object.entries(object.permissions).map(([key, values]) => {
                if (!values || values.length === 0) return null
                
                return (
                  <div key={key} className="space-y-2">
                    <p className="text-sm font-medium capitalize">{key}</p>
                    <div className="flex flex-wrap gap-2">
                      {values.map((value, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 rounded text-xs"
                        >
                          {key === 'owners' && <User className="h-3 w-3" />}
                          {key === 'users' && <Shield className="h-3 w-3" />}
                          {key === 'groups' && <Hash className="h-3 w-3" />}
                          {value}
                        </span>
                      ))}
                    </div>
                  </div>
                )
              })}
              
              {Object.values(object.permissions).every(p => !p || p.length === 0) && (
                <p className="text-sm text-gray-500">No special permissions configured</p>
              )}
            </div>
          </div>

          {/* Syft URL */}
          <div className="space-y-2">
            <h3 className="text-sm font-semibold uppercase text-gray-500">Syft URL</h3>
            <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
              <code className="text-xs flex-1 font-mono break-all">{object.syft_url}</code>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => copyToClipboard(object.syft_url, 'syft_url')}
              >
                {copiedField === 'syft_url' ? (
                  <Check className="h-3 w-3" />
                ) : (
                  <Copy className="h-3 w-3" />
                )}
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}