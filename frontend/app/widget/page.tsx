'use client'

import React, { useState, useEffect, useCallback, useRef } from 'react'
import { Search, User, Trash2, Plus, RefreshCw, FileText, Shield, Info, FolderOpen } from 'lucide-react'
import { SyftBoxLogo } from '@/components/syftbox-logo'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { api } from '@/lib/api'
import { SyftObject, ClientInfo, StatusInfo } from '@/lib/types'
import { cn } from '@/lib/utils'
import { CreateObjectModal } from '@/components/create-object-modal'
import { FileEditorModal } from '@/components/file-editor-modal'
import { ObjectInfoModal } from '@/components/object-info-modal'
import { PathModal } from '@/components/path-modal'
import { PermissionsModal } from '@/components/permissions-modal'

export default function WidgetPage() {
  const [objects, setObjects] = useState<SyftObject[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFilter, setSelectedFilter] = useState<string | null>(null)
  const [clientInfo, setClientInfo] = useState<ClientInfo | null>(null)
  const [statusInfo, setStatusInfo] = useState<StatusInfo | null>(null)
  const [selectedObjects, setSelectedObjects] = useState<Set<string>>(new Set())
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [isDragging, setIsDragging] = useState(false)
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalObjects, setTotalObjects] = useState(0)
  const itemsPerPage = 10
  const [selectedObject, setSelectedObject] = useState<SyftObject | null>(null)
  const [fileEditorOpen, setFileEditorOpen] = useState(false)
  const [fileEditorType, setFileEditorType] = useState<'private' | 'mock' | null>(null)
  const [infoModalOpen, setInfoModalOpen] = useState(false)
  const [pathModalOpen, setPathModalOpen] = useState(false)
  const [permissionsModalOpen, setPermissionsModalOpen] = useState(false)
  const [copiedItems, setCopiedItems] = useState<Set<string>>(new Set())
  
  // Track if component is mounted to prevent state updates after unmount
  const isMountedRef = useRef(true)
  
  useEffect(() => {
    return () => {
      isMountedRef.current = false
    }
  }, [])

  // Fetch initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [status, client] = await Promise.all([
          api.getStatus(),
          api.getClientInfo()
        ])
        setStatusInfo(status)
        setClientInfo(client)
      } catch (error) {
        console.error('Failed to fetch initial data:', error)
      }
    }
    fetchInitialData()
  }, [])

  // Fetch objects
  const fetchObjects = useCallback(async () => {
    try {
      const result = await api.getObjects({
        search: searchTerm,
        admin_email: selectedFilter || undefined,
        skip: (currentPage - 1) * itemsPerPage,
        limit: itemsPerPage
      })
      setObjects(result.objects)
      setTotalObjects(result.total)
    } catch (error) {
      console.error('Failed to fetch objects:', error)
    } finally {
      setLoading(false)
    }
  }, [searchTerm, selectedFilter, currentPage])

  // Auto-refresh
  useEffect(() => {
    fetchObjects()
    if (autoRefresh) {
      const interval = setInterval(fetchObjects, 1000)
      return () => clearInterval(interval)
    }
  }, [fetchObjects, autoRefresh])

  // Handle search
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setCurrentPage(1) // Reset to first page on new search
    fetchObjects()
  }

  // Handle delete
  const handleDelete = async (uid: string) => {
    if (!confirm('Are you sure you want to delete this object?')) return
    
    // Add loading state to prevent multiple clicks
    setLoading(true)
    
    try {
      await api.deleteObject(uid)
      
      // Only update state if component is still mounted
      if (isMountedRef.current) {
        await fetchObjects()
      }
    } catch (error) {
      console.error('Failed to delete object:', error)
      // Show user-friendly error message only if component is still mounted
      if (isMountedRef.current) {
        alert(`Failed to delete object: ${error instanceof Error ? error.message : 'Unknown error'}`)
      }
    } finally {
      // Always reset loading state if component is still mounted
      if (isMountedRef.current) {
        setLoading(false)
      }
    }
  }

  // Handle bulk delete
  const handleBulkDelete = async () => {
    if (!confirm(`Are you sure you want to delete ${selectedObjects.size} objects?`)) return
    
    // Add loading state to prevent multiple clicks
    setLoading(true)
    
    try {
      // Delete objects one by one instead of all at once to handle individual failures
      const deletePromises = Array.from(selectedObjects).map(async (uid) => {
        try {
          await api.deleteObject(uid)
          return { uid, success: true }
        } catch (error) {
          console.error(`Failed to delete object ${uid}:`, error)
          return { uid, success: false, error: error instanceof Error ? error.message : 'Unknown error' }
        }
      })
      
      const results = await Promise.all(deletePromises)
      const successCount = results.filter(r => r.success).length
      const failureCount = results.filter(r => !r.success).length
      
      // Clear selection only for successfully deleted objects (if component is still mounted)
      if (successCount > 0 && isMountedRef.current) {
        const successfulUids = results.filter(r => r.success).map(r => r.uid)
        const newSelected = new Set(selectedObjects)
        successfulUids.forEach(uid => newSelected.delete(uid))
        setSelectedObjects(newSelected)
      }
      
      // Refresh the objects list (if component is still mounted)
      if (isMountedRef.current) {
        await fetchObjects()
      }
      
      // Show summary message (if component is still mounted)
      if (failureCount > 0 && isMountedRef.current) {
        alert(`Deleted ${successCount} objects successfully. Failed to delete ${failureCount} objects.`)
      }
    } catch (error) {
      console.error('Failed to delete objects:', error)
      // Show error message only if component is still mounted
      if (isMountedRef.current) {
        alert(`Failed to delete objects: ${error instanceof Error ? error.message : 'Unknown error'}`)
      }
    } finally {
      // Always reset loading state if component is still mounted
      if (isMountedRef.current) {
        setLoading(false)
      }
    }
  }

  // Drag and drop handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = Array.from(e.dataTransfer.files)
    if (files.length === 0) return
    
    // Open create modal for file upload
    setCreateModalOpen(true)
    // TODO: Pass files to modal
  }

  // Modal handlers
  const openInfoModal = (object: SyftObject) => {
    setSelectedObject(object)
    setInfoModalOpen(true)
  }

  const openFileEditor = (object: SyftObject, fileType: 'private' | 'mock') => {
    setSelectedObject(object)
    setFileEditorType(fileType)
    setFileEditorOpen(true)
  }

  const openPathModal = (object: SyftObject) => {
    setSelectedObject(object)
    setPathModalOpen(true)
  }

  const openPermissionsModal = (object: SyftObject) => {
    setSelectedObject(object)
    setPermissionsModalOpen(true)
  }

  // Handle row click to copy Python code
  const handleRowClick = async (e: React.MouseEvent<HTMLTableRowElement>, object: SyftObject) => {
    // Only handle clicks on the row itself or non-action cells
    const target = e.target as HTMLElement
    if (target.closest('.actions-cell') || target.closest('input[type="checkbox"]')) {
      return
    }

    // Sanitize object name for Python variable
    const varName = object.name
      .replace(/[^a-zA-Z0-9_]/g, '_')
      .replace(/^[0-9]/, '_$&')
    
    const code = `${varName} = so.objects["${object.uid}"]`
    
    try {
      await navigator.clipboard.writeText(code)
      
      // Add visual feedback
      setCopiedItems(prev => new Set(prev).add(object.uid))
      setTimeout(() => {
        setCopiedItems(prev => {
          const newSet = new Set(prev)
          newSet.delete(object.uid)
          return newSet
        })
      }, 2000)
    } catch (err) {
      console.error('Failed to copy to clipboard:', err)
    }
  }

  return (
    <div 
      className="min-h-screen bg-gray-50 p-4"
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {/* Rainbow overlay for drag and drop */}
      {isDragging && (
        <div className="fixed inset-0 z-50 rainbow-overlay pointer-events-none" />
      )}

      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <SyftBoxLogo className="h-10 w-10" />
          <div>
            <h1 className="text-2xl font-bold">SyftBox Objects</h1>
            {statusInfo && (
              <p className="text-sm text-gray-600">
                {statusInfo.datasite} • {statusInfo.email}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={cn(autoRefresh && "bg-green-50 border-green-300")}
          >
            <RefreshCw className={cn("h-4 w-4", autoRefresh && "animate-spin")} />
            {autoRefresh ? 'Auto' : 'Manual'}
          </Button>
          <Button variant="outline" size="sm" onClick={fetchObjects}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Search and filters */}
      <div className="mb-6 space-y-4">
        <form onSubmit={handleSearch} className="flex gap-2">
          <Input
            type="text"
            placeholder="Search objects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1"
          />
          <Button type="submit">
            <Search className="h-4 w-4" />
            Search
          </Button>
        </form>
        
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Button 
              size="sm" 
              variant="default"
              onClick={() => setCreateModalOpen(true)}
            >
              <Plus className="h-4 w-4 mr-1" />
              Create Object
            </Button>
            {selectedObjects.size > 0 && (
              <Button 
                size="sm" 
                variant="destructive"
                onClick={handleBulkDelete}
              >
                <Trash2 className="h-4 w-4 mr-1" />
                Delete ({selectedObjects.size})
              </Button>
            )}
          </div>
          <p className="text-sm text-gray-600">
            {totalObjects || objects.length} objects
          </p>
        </div>
      </div>

      {/* Objects table */}
      <div className="rounded-lg border bg-white shadow-sm">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="p-2 text-left">
                <input
                  type="checkbox"
                  checked={selectedObjects.size === objects.length && objects.length > 0}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedObjects(new Set(objects.map(o => o.uid)))
                    } else {
                      setSelectedObjects(new Set())
                    }
                  }}
                />
              </th>
              <th className="p-2 text-left">Name</th>
              <th className="p-2 text-left">Description</th>
              <th className="p-2 text-left">Owner</th>
              <th className="p-2 text-left">Files</th>
              <th className="p-2 text-left">Permissions</th>
              <th className="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={7} className="p-8 text-center text-gray-500">
                  Loading...
                </td>
              </tr>
            ) : objects.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-8 text-center text-gray-500">
                  No objects found
                </td>
              </tr>
            ) : (
              objects.map((object) => (
                <tr 
                  key={object.uid} 
                  className={cn(
                    "border-b hover:bg-gray-50 cursor-pointer transition-colors",
                    copiedItems.has(object.uid) && "bg-green-50"
                  )}
                  onClick={(e) => handleRowClick(e, object)}
                >
                  <td className="p-2">
                    <input
                      type="checkbox"
                      checked={selectedObjects.has(object.uid)}
                      onChange={(e) => {
                        const newSelected = new Set(selectedObjects)
                        if (e.target.checked) {
                          newSelected.add(object.uid)
                        } else {
                          newSelected.delete(object.uid)
                        }
                        setSelectedObjects(newSelected)
                      }}
                    />
                  </td>
                  <td className="p-2 font-medium">{object.name}</td>
                  <td className="p-2 text-sm text-gray-600">{object.description}</td>
                  <td className="p-2">
                    <div className="flex items-center gap-1">
                      <User className="h-3 w-3" />
                      <span className="text-sm">{object.email}</span>
                    </div>
                  </td>
                  <td className="p-2">
                    <div className="flex gap-1">
                      {object.files.private?.exists && (
                        <span className="rounded bg-blue-100 px-2 py-1 text-xs">Private</span>
                      )}
                      {object.files.mock?.exists && (
                        <span className="rounded bg-green-100 px-2 py-1 text-xs">Mock</span>
                      )}
                    </div>
                  </td>
                  <td className="p-2">
                    <button 
                      className="flex gap-1 hover:text-blue-600 transition-colors"
                      onClick={() => openPermissionsModal(object)}
                    >
                      <Shield className="h-4 w-4 text-gray-400" />
                      <span className="text-xs text-gray-600">
                        {Object.values(object.permissions).flat().length} rules
                      </span>
                    </button>
                  </td>
                  <td className="p-2 actions-cell">
                    <div className="flex gap-1">
                      <Button 
                        size="sm" 
                        variant="ghost"
                        title="View info"
                        onClick={() => openInfoModal(object)}
                      >
                        <Info className="h-4 w-4" />
                      </Button>
                      <Button 
                        size="sm" 
                        variant="ghost"
                        title="View files"
                        onClick={() => {
                          if (object.files.private?.exists) {
                            openFileEditor(object, 'private')
                          } else if (object.files.mock?.exists) {
                            openFileEditor(object, 'mock')
                          }
                        }}
                      >
                        <FileText className="h-4 w-4" />
                      </Button>
                      <Button 
                        size="sm" 
                        variant="ghost"
                        title="View path"
                        onClick={() => openPathModal(object)}
                      >
                        <FolderOpen className="h-4 w-4" />
                      </Button>
                      <Button 
                        size="sm" 
                        variant="ghost"
                        onClick={() => handleDelete(object.uid)}
                        title="Delete"
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
        
        {/* Pagination */}
        {totalObjects > itemsPerPage && (
          <div className="flex items-center justify-between p-4 border-t">
            <p className="text-sm text-gray-600">
              Showing {((currentPage - 1) * itemsPerPage) + 1} to {Math.min(currentPage * itemsPerPage, totalObjects)} of {totalObjects} objects
            </p>
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
              >
                Previous
              </Button>
              <div className="flex items-center gap-1">
                {Array.from({ length: Math.ceil(totalObjects / itemsPerPage) }, (_, i) => i + 1)
                  .filter(page => {
                    const totalPages = Math.ceil(totalObjects / itemsPerPage)
                    if (totalPages <= 7) return true
                    if (page === 1 || page === totalPages) return true
                    if (Math.abs(page - currentPage) <= 1) return true
                    if (page === currentPage - 2 && currentPage > 3) return true
                    if (page === currentPage + 2 && currentPage < totalPages - 2) return true
                    return false
                  })
                  .map((page, index, array) => {
                    const prevPage = array[index - 1]
                    const showEllipsis = prevPage && page - prevPage > 1
                    
                    return (
                      <React.Fragment key={page}>
                        {showEllipsis && (
                          <span className="px-2 text-gray-400">...</span>
                        )}
                        <Button
                          size="sm"
                          variant={page === currentPage ? "default" : "outline"}
                          onClick={() => setCurrentPage(page)}
                          className="h-8 w-8 p-0"
                        >
                          {page}
                        </Button>
                      </React.Fragment>
                    )
                  })}
              </div>
              <Button
                size="sm"
                variant="outline"
                onClick={() => setCurrentPage(p => Math.min(Math.ceil(totalObjects / itemsPerPage), p + 1))}
                disabled={currentPage === Math.ceil(totalObjects / itemsPerPage)}
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      <CreateObjectModal 
        open={createModalOpen}
        onOpenChange={setCreateModalOpen}
        onSuccess={fetchObjects}
      />
      
      <FileEditorModal
        open={fileEditorOpen}
        onOpenChange={setFileEditorOpen}
        object={selectedObject}
        fileType={fileEditorType}
        onSave={fetchObjects}
      />
      
      <ObjectInfoModal
        open={infoModalOpen}
        onOpenChange={setInfoModalOpen}
        object={selectedObject}
      />
      
      <PathModal
        open={pathModalOpen}
        onOpenChange={setPathModalOpen}
        object={selectedObject}
      />
      
      <PermissionsModal
        open={permissionsModalOpen}
        onOpenChange={setPermissionsModalOpen}
        object={selectedObject}
        onSave={fetchObjects}
      />
    </div>
  )
}
