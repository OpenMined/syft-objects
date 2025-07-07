'use client'

import { useState, useEffect } from 'react'
import { Shield, User, Hash, X, Plus, Save } from 'lucide-react'
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
import { api } from '@/lib/api'
import { SyftObject } from '@/lib/types'

interface PermissionsModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  object: SyftObject | null
  onSave?: () => void
}

export function PermissionsModal({ 
  open, 
  onOpenChange, 
  object,
  onSave 
}: PermissionsModalProps) {
  const [permissions, setPermissions] = useState({
    owners: [] as string[],
    users: [] as string[],
    groups: [] as string[]
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (object) {
      setPermissions({
        owners: object.permissions.owners || [],
        users: object.permissions.users || [],
        groups: object.permissions.groups || []
      })
    }
  }, [object])

  const handleSave = async () => {
    if (!object) return
    
    setLoading(true)
    setError('')
    
    try {
      await api.updatePermissions(object.uid, permissions)
      if (onSave) {
        onSave()
      }
      onOpenChange(false)
    } catch (err) {
      setError('Failed to update permissions')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const addPermission = (type: 'owners' | 'users' | 'groups', value: string) => {
    if (value.trim() && !permissions[type].includes(value.trim())) {
      setPermissions(prev => ({
        ...prev,
        [type]: [...prev[type], value.trim()]
      }))
    }
  }

  const removePermission = (type: 'owners' | 'users' | 'groups', index: number) => {
    setPermissions(prev => ({
      ...prev,
      [type]: prev[type].filter((_, i) => i !== index)
    }))
  }

  const PermissionInput = ({ 
    type, 
    label, 
    icon: Icon,
    placeholder 
  }: { 
    type: 'owners' | 'users' | 'groups'
    label: string
    icon: any
    placeholder: string
  }) => {
    const [inputValue, setInputValue] = useState('')

    const handleAdd = () => {
      addPermission(type, inputValue)
      setInputValue('')
    }

    return (
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-gray-600" />
          <Label>{label}</Label>
        </div>
        
        <div className="space-y-2">
          <div className="flex gap-2">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={placeholder}
              onKeyPress={(e) => e.key === 'Enter' && handleAdd()}
              className="flex-1"
            />
            <Button
              type="button"
              size="sm"
              onClick={handleAdd}
              disabled={!inputValue.trim()}
            >
              <Plus className="h-4 w-4" />
            </Button>
          </div>
          
          <div className="space-y-2">
            {permissions[type].map((value, index) => (
              <div 
                key={index} 
                className="flex items-center justify-between p-2 bg-gray-50 rounded-lg"
              >
                <span className="text-sm">{value}</span>
                <Button
                  type="button"
                  size="sm"
                  variant="ghost"
                  onClick={() => removePermission(type, index)}
                  className="h-6 w-6 p-0"
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (!object) return null

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-xl" onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Manage Permissions
          </DialogTitle>
          <DialogDescription>
            Configure access permissions for {object.name}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <PermissionInput
            type="owners"
            label="Owners"
            icon={User}
            placeholder="owner@example.com"
          />

          <PermissionInput
            type="users"
            label="Users"
            icon={Shield}
            placeholder="user@example.com"
          />

          <PermissionInput
            type="groups"
            label="Groups"
            icon={Hash}
            placeholder="group-name"
          />

          <div className="rounded-lg bg-blue-50 p-4">
            <h4 className="text-sm font-medium mb-2">Permission Levels</h4>
            <ul className="text-xs space-y-1 text-gray-600">
              <li><strong>Owners:</strong> Full control over the object</li>
              <li><strong>Users:</strong> Can read and use the object</li>
              <li><strong>Groups:</strong> Group-based access control</li>
            </ul>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={loading}>
            {loading ? (
              'Saving...'
            ) : (
              <>
                <Save className="h-4 w-4 mr-1" />
                Save Permissions
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}