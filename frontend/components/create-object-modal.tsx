'use client'

import { useState, useRef } from 'react'
import { Upload, X, FileText, Shield } from 'lucide-react'
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogDescription,
  DialogFooter 
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'

interface CreateObjectModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

export function CreateObjectModal({ open, onOpenChange, onSuccess }: CreateObjectModalProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [privateFile, setPrivateFile] = useState<File | null>(null)
  const [mockFile, setMockFile] = useState<File | null>(null)
  const [permissions, setPermissions] = useState({
    owners: [''] as string[],
    users: [''] as string[],
    groups: [''] as string[]
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const privateFileRef = useRef<HTMLInputElement>(null)
  const mockFileRef = useRef<HTMLInputElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Create form data
      const formData = new FormData()
      formData.append('name', name)
      formData.append('description', description)
      
      if (privateFile) {
        formData.append('private_file', privateFile)
      }
      if (mockFile) {
        formData.append('mock_file', mockFile)
      }

      // Add permissions
      const cleanPermissions = {
        owners: permissions.owners.filter(o => o.trim()),
        users: permissions.users.filter(u => u.trim()),
        groups: permissions.groups.filter(g => g.trim())
      }
      formData.append('permissions', JSON.stringify(cleanPermissions))

      await api.createObject(formData)
      
      // Reset form
      setName('')
      setDescription('')
      setPrivateFile(null)
      setMockFile(null)
      setPermissions({ owners: [''], users: [''], groups: [''] })
      
      onSuccess()
      onOpenChange(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create object')
    } finally {
      setLoading(false)
    }
  }

  const handleFileChange = (type: 'private' | 'mock', file: File | null) => {
    if (type === 'private') {
      setPrivateFile(file)
    } else {
      setMockFile(file)
    }
  }

  const addPermissionField = (type: 'owners' | 'users' | 'groups') => {
    setPermissions(prev => ({
      ...prev,
      [type]: [...prev[type], '']
    }))
  }

  const updatePermission = (type: 'owners' | 'users' | 'groups', index: number, value: string) => {
    setPermissions(prev => ({
      ...prev,
      [type]: prev[type].map((item, i) => i === index ? value : item)
    }))
  }

  const removePermission = (type: 'owners' | 'users' | 'groups', index: number) => {
    setPermissions(prev => ({
      ...prev,
      [type]: prev[type].filter((_, i) => i !== index)
    }))
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto" onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle>Create New Object</DialogTitle>
          <DialogDescription>
            Create a new SyftBox object with optional files and permissions
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter object name"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter object description"
              rows={3}
            />
          </div>

          {/* File uploads */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Private File</Label>
              <div 
                className={cn(
                  "border-2 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 transition-colors",
                  privateFile && "border-blue-500 bg-blue-50"
                )}
                onClick={() => privateFileRef.current?.click()}
              >
                <input
                  ref={privateFileRef}
                  type="file"
                  onChange={(e) => handleFileChange('private', e.target.files?.[0] || null)}
                  className="hidden"
                />
                {privateFile ? (
                  <div className="flex items-center justify-center gap-2">
                    <FileText className="h-5 w-5 text-blue-600" />
                    <span className="text-sm font-medium">{privateFile.name}</span>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleFileChange('private', null)
                      }}
                      className="ml-2 text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Upload className="h-8 w-8 mx-auto text-gray-400" />
                    <p className="text-sm text-gray-600">Click to upload private file</p>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label>Mock File</Label>
              <div 
                className={cn(
                  "border-2 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 transition-colors",
                  mockFile && "border-green-500 bg-green-50"
                )}
                onClick={() => mockFileRef.current?.click()}
              >
                <input
                  ref={mockFileRef}
                  type="file"
                  onChange={(e) => handleFileChange('mock', e.target.files?.[0] || null)}
                  className="hidden"
                />
                {mockFile ? (
                  <div className="flex items-center justify-center gap-2">
                    <FileText className="h-5 w-5 text-green-600" />
                    <span className="text-sm font-medium">{mockFile.name}</span>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleFileChange('mock', null)
                      }}
                      className="ml-2 text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Upload className="h-8 w-8 mx-auto text-gray-400" />
                    <p className="text-sm text-gray-600">Click to upload mock file</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Permissions */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              <Label>Permissions</Label>
            </div>

            {/* Owners */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Owners</Label>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  onClick={() => addPermissionField('owners')}
                >
                  Add Owner
                </Button>
              </div>
              {permissions.owners.map((owner, index) => (
                <div key={index} className="flex gap-2">
                  <Input
                    value={owner}
                    onChange={(e) => updatePermission('owners', index, e.target.value)}
                    placeholder="email@example.com"
                    className="flex-1"
                  />
                  {permissions.owners.length > 1 && (
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      onClick={() => removePermission('owners', index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>

            {/* Users */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Users</Label>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  onClick={() => addPermissionField('users')}
                >
                  Add User
                </Button>
              </div>
              {permissions.users.map((user, index) => (
                <div key={index} className="flex gap-2">
                  <Input
                    value={user}
                    onChange={(e) => updatePermission('users', index, e.target.value)}
                    placeholder="email@example.com"
                    className="flex-1"
                  />
                  {permissions.users.length > 1 && (
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      onClick={() => removePermission('users', index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>

            {/* Groups */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Groups</Label>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  onClick={() => addPermissionField('groups')}
                >
                  Add Group
                </Button>
              </div>
              {permissions.groups.map((group, index) => (
                <div key={index} className="flex gap-2">
                  <Input
                    value={group}
                    onChange={(e) => updatePermission('groups', index, e.target.value)}
                    placeholder="group-name"
                    className="flex-1"
                  />
                  {permissions.groups.length > 1 && (
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      onClick={() => removePermission('groups', index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading || !name}>
              {loading ? 'Creating...' : 'Create Object'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}