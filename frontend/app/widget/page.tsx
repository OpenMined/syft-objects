'use client'

import { useEffect, useState, useCallback } from 'react'
import { RefreshCw, Search, Filter, Eye, Globe, Lock, Calendar, User, FileText, ChevronUp, ChevronDown, ChevronLeft, ChevronRight, Trash2 } from 'lucide-react'

// Custom SyftBox Logo Component with zoom animation and rainbow explosion effect
function SyftBoxLogo({ className = "h-8 w-8", isLoading = false }: { className?: string, isLoading?: boolean }) {
  const [showLlama, setShowLlama] = useState(false)
  const [showExplosion, setShowExplosion] = useState(false)

  useEffect(() => {
    if (!isLoading && !showLlama) {
      // Show llama for a brief moment after loading stops
      const timer = setTimeout(() => setShowLlama(true), 500)
      const hideTimer = setTimeout(() => setShowLlama(false), 2000)
      return () => {
        clearTimeout(timer)
        clearTimeout(hideTimer)
      }
    }
  }, [isLoading, showLlama])

  useEffect(() => {
    if (isLoading) {
      // Create periodic explosion effect
      const explosionInterval = setInterval(() => {
        setShowExplosion(true)
        setTimeout(() => setShowExplosion(false), 400)
      }, 1600) // Explosion every 1.6 seconds
      
      return () => clearInterval(explosionInterval)
    }
  }, [isLoading])

  if (showLlama) {
    return <div className={`${className} text-4xl animate-bounce`}>🦙</div>
  }

  return (
    <svg
      className={`${className} ${isLoading ? 'syftbox-loading' : ''} ${showExplosion ? 'syftbox-explosion' : ''}`}
      viewBox="0 0 311 360"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
        <g clipPath="url(#clip0_7523_4240)">
          <path 
            d="M311.414 89.7878L155.518 179.998L-0.378906 89.7878L155.518 -0.422485L311.414 89.7878Z" 
            fill="url(#paint0_linear_7523_4240)"
          />
          <path 
            d="M311.414 89.7878V270.208L155.518 360.423V179.998L311.414 89.7878Z" 
            fill="url(#paint1_linear_7523_4240)"
          />
          <path 
            d="M155.518 179.998V360.423L-0.378906 270.208V89.7878L155.518 179.998Z" 
            fill="url(#paint2_linear_7523_4240)"
          />
        </g>
        <defs>
          <linearGradient id="paint0_linear_7523_4240" x1="-0.378904" y1="89.7878" x2="311.414" y2="89.7878" gradientUnits="userSpaceOnUse">
            <stop stopColor="#DC7A6E"/>
            <stop offset="0.251496" stopColor="#F6A464"/>
            <stop offset="0.501247" stopColor="#FDC577"/>
            <stop offset="0.753655" stopColor="#EFC381"/>
            <stop offset="1" stopColor="#B9D599"/>
          </linearGradient>
          <linearGradient id="paint1_linear_7523_4240" x1="309.51" y1="89.7878" x2="155.275" y2="360.285" gradientUnits="userSpaceOnUse">
            <stop stopColor="#BFCD94"/>
            <stop offset="0.245025" stopColor="#B2D69E"/>
            <stop offset="0.504453" stopColor="#8DCCA6"/>
            <stop offset="0.745734" stopColor="#5CB8B7"/>
            <stop offset="1" stopColor="#4CA5B8"/>
          </linearGradient>
          <linearGradient id="paint2_linear_7523_4240" x1="-0.378906" y1="89.7878" x2="155.761" y2="360.282" gradientUnits="userSpaceOnUse">
            <stop stopColor="#D7686D"/>
            <stop offset="0.225" stopColor="#C64B77"/>
            <stop offset="0.485" stopColor="#A2638E"/>
            <stop offset="0.703194" stopColor="#758AA8"/>
            <stop offset="1" stopColor="#639EAF"/>
          </linearGradient>
          <clipPath id="clip0_7523_4240">
            <rect width="311" height="360" fill="white"/>
          </clipPath>
        </defs>
      </svg>
  )
}

interface SyftObject {
  index: number
  uid: string
  name: string
  description: string
  email: string
  private_url: string
  mock_url: string
  syftobject_url: string
  created_at: string | null
  updated_at: string | null
  permissions: {
    syftobject: string[]
    mock_read: string[]
    mock_write: string[]
    private_read: string[]
    private_write: string[]
  }
  metadata: Record<string, any>
  file_exists: {
    private: boolean
    mock: boolean
  }
}

interface ApiResponse {
  objects: SyftObject[]
  total_count: number
  offset: number
  limit?: number
  has_more: boolean
  search_info?: string
}

interface AppStatus {
  app: string
  version: string
  syftbox: {
    status: string
    user_email?: string
  }
  components: {
    backend: string
    objects_collection: string
  }
}

// Permission Editor Component
function PermissionEditor({
  permissions,
  onAddPermission,
  onRemovePermission
}: {
  permissions: SyftObject['permissions']
  onAddPermission: (type: keyof SyftObject['permissions'], email: string) => void
  onRemovePermission: (type: keyof SyftObject['permissions'], email: string) => void
}) {
  const [newEmails, setNewEmails] = useState<Record<string, string>>({
    private_read: '',
    private_write: '',
    mock_read: '',
    mock_write: '',
    syftobject: ''
  })

  const handleAddEmail = (type: keyof SyftObject['permissions']) => {
    const email = newEmails[type]
    if (email.trim()) {
      onAddPermission(type, email.trim())
      setNewEmails(prev => ({ ...prev, [type]: '' }))
    }
  }

  const permissionTypes = [
    { key: 'private_read' as const, label: 'Private Read', color: 'text-green-700' },
    { key: 'private_write' as const, label: 'Private Write', color: 'text-green-800' },
    { key: 'mock_read' as const, label: 'Mock Read', color: 'text-blue-700' },
    { key: 'mock_write' as const, label: 'Mock Write', color: 'text-blue-800' },
    { key: 'syftobject' as const, label: 'Syft Object', color: 'text-purple-700' }
  ]

  return (
    <div className="space-y-4">
      {permissionTypes.map(({ key, label, color }) => (
        <div key={key} className="border rounded p-3">
          <h4 className={`font-medium ${color} mb-2`}>{label}</h4>
          <div className="space-y-2">
            <div className="flex flex-wrap gap-1">
              {permissions[key].map(email => (
                <span key={email} className="flex items-center bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs">
                  {email}
                  <button
                    onClick={() => onRemovePermission(key, email)}
                    className="ml-1 text-red-500 hover:text-red-700"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
            <div className="flex space-x-2">
              <input
                type="text"
                placeholder="Add email or 'public'"
                value={newEmails[key]}
                onChange={(e) => setNewEmails(prev => ({ ...prev, [key]: e.target.value }))}
                onKeyPress={(e) => e.key === 'Enter' && handleAddEmail(key)}
                className="flex-1 px-2 py-1 border rounded text-xs"
              />
              <button
                onClick={() => handleAddEmail(key)}
                className="px-2 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default function Widget() {
  const [objects, setObjects] = useState<SyftObject[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [status, setStatus] = useState<AppStatus | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [emailFilter, setEmailFilter] = useState('')
  const [selectedObject, setSelectedObject] = useState<SyftObject | null>(null)
  const [totalCount, setTotalCount] = useState(0)
  const [searchInfo, setSearchInfo] = useState<string | null>(null)
  const [sortField, setSortField] = useState<keyof SyftObject>('created_at')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')
  const [sortedObjects, setSortedObjects] = useState<SyftObject[]>([])
  const [autoRefresh, setAutoRefresh] = useState(true)
  
  // Checkbox selection state
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set())
  const [selectAll, setSelectAll] = useState(false)
  
  // Track previous search terms to only clear selections when search actually changes
  const [prevSearchTerm, setPrevSearchTerm] = useState('')
  const [prevEmailFilter, setPrevEmailFilter] = useState('')
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(50) // More objects per page by default
  const [totalPages, setTotalPages] = useState(0)

  // File content modal state
  const [fileContentModal, setFileContentModal] = useState<{
    isOpen: boolean
    title: string
    content: string
    editedContent: string
    loading: boolean
    saving: boolean
    fileType: 'private' | 'mock' | null
    objectUid: string | null
    canWrite: boolean
  }>({
    isOpen: false,
    title: '',
    content: '',
    editedContent: '',
    loading: false,
    saving: false,
    fileType: null,
    objectUid: null,
    canWrite: false
  })

  // Delete confirmation modal state
  const [deleteModal, setDeleteModal] = useState<{
    isOpen: boolean
    object: SyftObject | null
    loading: boolean
  }>({
    isOpen: false,
    object: null,
    loading: false
  })

  // Permission editing state
  const [editingPermissions, setEditingPermissions] = useState(false)
  const [editedPermissions, setEditedPermissions] = useState<SyftObject['permissions'] | null>(null)
  const [savingPermissions, setSavingPermissions] = useState(false)

  // UID copy feedback state
  const [copiedUid, setCopiedUid] = useState<string | null>(null)
  
  // Email copy feedback state
  const [copiedEmail, setCopiedEmail] = useState<string | null>(null)
  
  // Row click rainbow animation state
  const [clickedRows, setClickedRows] = useState<Set<string>>(new Set())
  
  // Global clipboard notification state
  const [clipboardNotification, setClipboardNotification] = useState<string | null>(null)
  
  // Show clipboard notification
  const showClipboardNotification = (text: string) => {
    setClipboardNotification(`copied to clipboard: ${text}`)
    setTimeout(() => setClipboardNotification(null), 3000)
  }

  // These refs are no longer needed since we're doing client-side filtering

  const API_BASE = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8003'

  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/status`)
      if (!response.ok) throw new Error('Failed to fetch status')
      const data = await response.json()
      setStatus(data)
    } catch (err) {
      console.error('Error fetching status:', err)
    }
  }

  const fetchObjects = async () => {
    try {
      // Fetch all objects without filtering - filtering is now done client-side
      const response = await fetch(`${API_BASE}/api/objects`)
      if (!response.ok) {
        throw new Error(`Failed to fetch objects: ${response.statusText}`)
      }
      
      const data: ApiResponse = await response.json()
      
      setObjects(data.objects)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch objects')
      setObjects([])
    }
  }

  const refreshObjects = async () => {
    setRefreshing(true)
    try {
      const response = await fetch(`${API_BASE}/api/objects/refresh`)
      if (!response.ok) throw new Error('Failed to refresh objects')
      await fetchObjects()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh objects')
    } finally {
      setRefreshing(false)
    }
  }

  const handleSearch = () => {
    setCurrentPage(1) // Reset to first page when searching
    // Search is now handled by the useEffect with client-side filtering
  }

  // Enhanced search function that works against all fields
  const searchInObject = (obj: SyftObject, term: string): boolean => {
    if (!term) return true
    
    const searchTerm = term.toLowerCase()
    
    // Search in basic fields
    const basicFields = [
      obj.name,
      obj.description,
      obj.email,
      obj.uid,
      obj.private_url,
      obj.mock_url,
      obj.syftobject_url,
      obj.index.toString()
    ]
    
    // Search in dates
    const dateFields = [
      obj.created_at,
      obj.updated_at
    ].filter(Boolean).map(date => {
      if (!date) return ''
      try {
        return new Date(date).toLocaleString().toLowerCase()
      } catch {
        return date.toLowerCase()
      }
    })
    
    // Search in permissions
    const permissionFields = [
      ...obj.permissions.syftobject,
      ...obj.permissions.mock_read,
      ...obj.permissions.mock_write,
      ...obj.permissions.private_read,
      ...obj.permissions.private_write
    ]
    
    // Search in metadata
    const metadataString = JSON.stringify(obj.metadata).toLowerCase()
    
    const allFields = [
      ...basicFields,
      ...dateFields,
      ...permissionFields,
      metadataString
    ]
    
    return allFields.some(field => 
      field && field.toString().toLowerCase().includes(searchTerm)
    )
  }

  const handleClearFilters = () => {
    setSearchTerm('')
    setEmailFilter('')
    setCurrentPage(1) // Reset to first page when clearing filters
    // Filtering is now handled by the useEffect with client-side filtering
  }

  // Checkbox handling functions
  const handleSelectAll = () => {
    const currentPageObjects = sortedObjects.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
    const currentPageUids = currentPageObjects.map(obj => obj.uid)
    const allCurrentPageSelected = currentPageUids.every(uid => selectedItems.has(uid))
    
    if (allCurrentPageSelected) {
      // Deselect all items on current page
      const newSelected = new Set(selectedItems)
      currentPageUids.forEach(uid => newSelected.delete(uid))
      setSelectedItems(newSelected)
    } else {
      // Select all items on current page
      const newSelected = new Set(selectedItems)
      currentPageUids.forEach(uid => newSelected.add(uid))
      setSelectedItems(newSelected)
    }
  }

  const handleItemSelect = (uid: string) => {
    const newSelected = new Set(selectedItems)
    if (newSelected.has(uid)) {
      newSelected.delete(uid)
    } else {
      newSelected.add(uid)
    }
    setSelectedItems(newSelected)
  }

  // Update selectAll state based on current page selection
  useEffect(() => {
    const currentPageObjects = sortedObjects.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
    const currentPageUids = currentPageObjects.map(obj => obj.uid)
    const allCurrentPageSelected = currentPageUids.length > 0 && currentPageUids.every(uid => selectedItems.has(uid))
    setSelectAll(allCurrentPageSelected)
  }, [selectedItems, sortedObjects, currentPage, itemsPerPage])

  // Bulk operations

  const handleBulkDelete = () => {
    const selectedObjects = sortedObjects.filter(obj => selectedItems.has(obj.uid))
    if (selectedObjects.length === 0) return
    
    // Show confirmation modal for bulk delete
    setDeleteModal({
      isOpen: true,
      object: null, // null indicates bulk delete
      loading: false
    })
  }

  // Pagination functions
  const handlePageChange = (page: number) => {
    setCurrentPage(page)
    // Pagination is now handled by client-side filtering
  }

  const handleItemsPerPageChange = (newItemsPerPage: number) => {
    setItemsPerPage(newItemsPerPage)
    setCurrentPage(1) // Reset to first page when changing items per page
    // Pagination is now handled by client-side filtering
  }

  const sortObjects = useCallback((objectsToSort: SyftObject[], field: keyof SyftObject, direction: 'asc' | 'desc') => {
    return [...objectsToSort].sort((a, b) => {
      let aValue = a[field]
      let bValue = b[field]

      // Handle null/undefined values
      if (aValue === null || aValue === undefined) aValue = ''
      if (bValue === null || bValue === undefined) bValue = ''

      // Special handling for numeric fields (index)
      if (field === 'index') {
        const aNum = Number(aValue)
        const bNum = Number(bValue)
        return direction === 'desc' ? bNum - aNum : aNum - bNum
      }

      // Special handling for dates
      if (field === 'created_at' || field === 'updated_at') {
        const aDate = aValue ? new Date(aValue as string).getTime() : 0
        const bDate = bValue ? new Date(bValue as string).getTime() : 0
        return direction === 'desc' ? bDate - aDate : aDate - bDate
      }

      // Handle string comparisons (case insensitive)
      const aStr = String(aValue).toLowerCase()
      const bStr = String(bValue).toLowerCase()

      if (aStr < bStr) return direction === 'desc' ? 1 : -1
      if (aStr > bStr) return direction === 'desc' ? -1 : 1
      return 0
    })
  }, [])

  const handleSort = (field: keyof SyftObject) => {
    const newDirection = sortField === field && sortDirection === 'desc' ? 'asc' : 'desc'
    setSortField(field)
    setSortDirection(newDirection)
  }

  const convertSyftUrlToHttp = (syftUrl: string): string => {
    // Convert syft://email@domain.com/path/to/file to HTTP API endpoint
    if (syftUrl.startsWith('syft://')) {
      // Use the backend API to serve the file, encoding the entire URL
      return `${API_BASE}/api/file?syft_url=${encodeURIComponent(syftUrl)}`
    }
    return syftUrl
  }

  const fetchFileContent = async (url: string, title: string, fileType: 'private' | 'mock', objectUid: string, canWrite: boolean = false) => {
    setFileContentModal({
      isOpen: true,
      title,
      content: '',
      editedContent: '',
      loading: true,
      saving: false,
      fileType,
      objectUid,
      canWrite
    })

    try {
      const httpUrl = convertSyftUrlToHttp(url)
      const response = await fetch(httpUrl)
      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.statusText}`)
      }
      const content = await response.text()
      setFileContentModal(prev => ({
        ...prev,
        content,
        editedContent: content,
        loading: false
      }))
    } catch (error) {
      const errorMessage = `Error loading file: ${error instanceof Error ? error.message : 'Unknown error'}`
      setFileContentModal(prev => ({
        ...prev,
        content: errorMessage,
        editedContent: errorMessage,
        loading: false
      }))
    }
  }

  const saveFileContent = async () => {
    if (!fileContentModal.fileType || !fileContentModal.objectUid) return

    setFileContentModal(prev => ({ ...prev, saving: true }))

    try {
      const response = await fetch(`${API_BASE}/api/objects/${fileContentModal.objectUid}/file/${fileContentModal.fileType}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'text/plain',
        },
        body: fileContentModal.editedContent
      })

      if (!response.ok) {
        throw new Error(`Failed to save file: ${response.statusText}`)
      }

      // Update the content to match what was saved
      setFileContentModal(prev => ({
        ...prev,
        content: prev.editedContent,
        saving: false
      }))

      // Refresh the objects list to update any metadata
      await fetchObjects()

    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to save file')
      setFileContentModal(prev => ({ ...prev, saving: false }))
    }
  }

  const copyToClipboard = async (text: string) => {
    try {
      console.log('🚀 Starting copy operation...')
      console.log('🔍 Clipboard API available:', !!navigator.clipboard)
      console.log('🔍 WriteText available:', !!(navigator.clipboard && navigator.clipboard.writeText))
      console.log('🔍 Is secure context:', window.isSecureContext)
      console.log('🔍 Document has focus:', document.hasFocus())
      
      // Try modern clipboard API first
      if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
        console.log('📋 Attempting modern clipboard API...')
        
        // Check permissions first
        try {
          const permission = await navigator.permissions.query({ name: 'clipboard-write' as any })
          console.log('🔍 Clipboard permission:', permission.state)
        } catch (permError) {
          console.log('🔍 Could not check clipboard permissions:', permError)
        }
        
        await navigator.clipboard.writeText(text)
        console.log('✅ Copied to clipboard (modern API):', text.substring(0, 20) + '...')
        showClipboardNotification(text)
        return
      }
      
      // Fallback method
      console.log('📋 Using fallback clipboard method...')
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      textArea.style.width = '1px'
      textArea.style.height = '1px'
      textArea.style.opacity = '0'
      
      document.body.appendChild(textArea)
      
      try {
        // Focus and select
        textArea.focus()
        textArea.select()
        textArea.setSelectionRange(0, text.length)
        
        // Try execCommand
        const successful = document.execCommand('copy')
        console.log('🔍 execCommand copy result:', successful)
        
        if (successful) {
          console.log('✅ Copied to clipboard (fallback):', text.substring(0, 20) + '...')
          showClipboardNotification(text)
        } else {
          throw new Error('execCommand copy failed')
        }
      } finally {
        document.body.removeChild(textArea)
      }
      
    } catch (err) {
      console.error('❌ Copy operation failed:', err)
      const error = err as Error
      console.error('❌ Error details:', {
        name: error.name,
        message: error.message,
        stack: error.stack
      })
      
      // Try one more fallback - create a temporary input
      try {
        console.log('📋 Trying final fallback method...')
        const input = document.createElement('input')
        input.value = text
        input.style.position = 'fixed'
        input.style.left = '-999999px'
        input.style.top = '-999999px'
        
        document.body.appendChild(input)
        input.focus()
        input.select()
        
        const success = document.execCommand('copy')
        document.body.removeChild(input)
        
        if (success) {
          console.log('✅ Copied to clipboard (final fallback)!')
          showClipboardNotification(text)
        } else {
          throw new Error('All copy methods failed')
        }
      } catch (finalErr) {
        console.error('❌ Final fallback also failed:', finalErr)
        showClipboardNotification('Failed to copy to clipboard')
      }
    }
  }





  const copyPath = async (obj: SyftObject) => {
    // Try to get the local path of the private file first, then mock as fallback
    let path = ''
    try {
      if (obj.private_url) {
        const response = await fetch(`${API_BASE}/api/file?syft_url=${encodeURIComponent(obj.private_url)}`)
        if (response.ok) {
          // If we can access the file, try to get the local path from the URL conversion
          const url = new URL(obj.private_url.replace('syft://', 'http://'))
          const email = url.hostname
          const filePath = url.pathname
          path = `~/SyftBox/datasites/${email}${filePath}`
        }
      }
      
      // Fallback to mock path if private doesn't work
      if (!path && obj.mock_url) {
        const url = new URL(obj.mock_url.replace('syft://', 'http://'))
        const email = url.hostname
        const filePath = url.pathname  
        path = `~/SyftBox/datasites/${email}${filePath}`
      }
      
      if (path) {
        await copyToClipboard(path)
      } else {
        throw new Error('Could not determine local path')
      }
    } catch (error) {
      // Fallback: just copy the syft:// URL
      await copyToClipboard(obj.private_url || obj.mock_url || 'Path not available')
    }
  }

  // Helper function to get current permissions for an object (checks both table and selected object)
  const getCurrentPermissions = (uid: string) => {
    // If this is the currently selected object, use its updated permissions
    if (selectedObject && selectedObject.uid === uid) {
      return selectedObject.permissions
    }
    // Otherwise find it in the sorted objects array
    const obj = sortedObjects.find(o => o.uid === uid)
    return obj?.permissions || null
  }

  // Check if current user can edit permissions (owner or has admin rights)
  const canEditPermissions = (obj: SyftObject): boolean => {
    const userEmail = status?.syftbox?.user_email || ''
    // User can edit if they're the owner or if they have admin permissions on the object
    return obj.email === userEmail || obj.permissions.syftobject.includes(userEmail)
  }

  // Permission editing functions
  const startEditingPermissions = () => {
    if (selectedObject) {
      setEditedPermissions(JSON.parse(JSON.stringify(selectedObject.permissions)))
      setEditingPermissions(true)
    }
  }

  const cancelEditingPermissions = () => {
    setEditingPermissions(false)
    setEditedPermissions(null)
  }

  const addPermission = (type: keyof SyftObject['permissions'], email: string) => {
    if (!editedPermissions || !email.trim()) return
    
    const newPermissions = { ...editedPermissions }
    if (!newPermissions[type].includes(email.trim())) {
      newPermissions[type] = [...newPermissions[type], email.trim()]
    }
    setEditedPermissions(newPermissions)
  }

  const removePermission = (type: keyof SyftObject['permissions'], email: string) => {
    if (!editedPermissions) return
    
    const newPermissions = { ...editedPermissions }
    newPermissions[type] = newPermissions[type].filter(e => e !== email)
    setEditedPermissions(newPermissions)
  }

  const savePermissions = async () => {
    if (!selectedObject || !editedPermissions) return

    setSavingPermissions(true)
    try {
      console.log('🔧 Saving permissions for object:', selectedObject.uid)
      console.log('🔧 Permissions payload:', editedPermissions)
      
      const response = await fetch(`${API_BASE}/api/objects/${selectedObject.uid}/permissions`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedPermissions)
      })

      const responseData = await response.text()
      console.log('🔧 Response status:', response.status)
      console.log('🔧 Response data:', responseData)

      if (!response.ok) {
        throw new Error(`Failed to save permissions: ${response.status} ${response.statusText} - ${responseData}`)
      }

      // Update the selected object with new permissions
      const updatedObject = { ...selectedObject, permissions: editedPermissions }
      setSelectedObject(updatedObject)

      // Refresh the objects list
      await fetchObjects()

      // Exit editing mode
      setEditingPermissions(false)
      setEditedPermissions(null)

      // Show success message
      console.log('✅ Permissions saved successfully')

    } catch (error) {
      console.error('❌ Error saving permissions:', error)
      setError(error instanceof Error ? error.message : 'Failed to save permissions')
    } finally {
      setSavingPermissions(false)
    }
  }

  const deleteObject = async (objectUid: string) => {
    setDeleteModal(prev => ({ ...prev, loading: true }))
    
    try {
      const response = await fetch(`${API_BASE}/api/objects/${objectUid}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`Failed to delete object: ${response.statusText}`)
      }
      
      // Refresh the objects list
      await fetchObjects()
      
      // Close the modal
      setDeleteModal({ isOpen: false, object: null, loading: false })
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to delete object')
      setDeleteModal(prev => ({ ...prev, loading: false }))
    }
  }

  const deleteBulkObjects = async () => {
    setDeleteModal(prev => ({ ...prev, loading: true }))
    
    try {
      const selectedObjects = sortedObjects.filter(obj => selectedItems.has(obj.uid))
      const deletePromises = selectedObjects.map(obj => 
        fetch(`${API_BASE}/api/objects/${obj.uid}`, { method: 'DELETE' })
      )
      
      const responses = await Promise.all(deletePromises)
      const failedDeletes = responses.filter(response => !response.ok)
      
      if (failedDeletes.length > 0) {
        throw new Error(`Failed to delete ${failedDeletes.length} objects`)
      }
      
      // Clear selections and refresh the objects list
      setSelectedItems(new Set())
      setSelectAll(false)
      await fetchObjects()
      
      // Close the modal
      setDeleteModal({ isOpen: false, object: null, loading: false })
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to delete objects')
      setDeleteModal(prev => ({ ...prev, loading: false }))
    }
  }

  // Apply filtering and sorting when objects or parameters change
  useEffect(() => {
    let filtered = objects
    
    // Apply client-side search filtering
    if (searchTerm) {
      filtered = objects.filter(obj => searchInObject(obj, searchTerm))
    }
    
    // Apply email filtering
    if (emailFilter) {
      filtered = filtered.filter(obj => 
        obj.email.toLowerCase().includes(emailFilter.toLowerCase())
      )
    }
    
    const sorted = sortObjects(filtered, sortField, sortDirection)
    setSortedObjects(sorted)
    
    // Update total count for filtered results
    setTotalCount(sorted.length)
    setTotalPages(Math.ceil(sorted.length / itemsPerPage))
    
    // Only clear selections when search terms actually change, not on auto-refresh
    const searchChanged = searchTerm !== prevSearchTerm || emailFilter !== prevEmailFilter
    if (searchChanged) {
      setSelectedItems(new Set())
      setSelectAll(false)
      setPrevSearchTerm(searchTerm)
      setPrevEmailFilter(emailFilter)
    }
  }, [objects, sortField, sortDirection, searchTerm, emailFilter, sortObjects, itemsPerPage, prevSearchTerm, prevEmailFilter])

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A'
    try {
      return new Date(dateString).toLocaleString()
    } catch {
      return 'Invalid date'
    }
  }

  const isRecentObject = (createdAt: string | null) => {
    if (!createdAt) return false
    try {
      const createdTime = new Date(createdAt).getTime()
      const currentTime = new Date().getTime()
      const timeDifference = (currentTime - createdTime) / 1000 // Convert to seconds
      return timeDifference < 10 // Less than 10 seconds old
    } catch {
      return false
    }
  }

  useEffect(() => {
    const initialize = async () => {
      setLoading(true)
      await Promise.all([fetchStatus(), fetchObjects()])
      setLoading(false)
    }
    initialize()
  }, [])

  // Auto-refresh every 1 second
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      fetchObjects()
    }, 1000)

    return () => clearInterval(interval)
  }, [autoRefresh]) // Only depend on autoRefresh to avoid restart issues

  // Update total pages when itemsPerPage changes
  useEffect(() => {
    if (totalCount > 0) {
      setTotalPages(Math.ceil(totalCount / itemsPerPage))
    }
  }, [totalCount, itemsPerPage])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[200px] p-4">
        <div className="text-center space-y-4">
          <SyftBoxLogo className="h-12 w-12 mx-auto" isLoading={true} />
          <p className="text-sm text-muted-foreground">Loading syft objects...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full bg-background text-foreground flex flex-col overflow-hidden">
      {/* Header Section */}
      <div className="flex-shrink-0 space-y-3 p-0">


      {/* Compact Search and Filters */}
      <div className="bg-card rounded border p-2">
        <div className="flex flex-col sm:flex-row gap-1">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search objects..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full pl-7 pr-2 py-1 border rounded text-xs focus:ring-1 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex-1">
            <div className="relative">
              <Filter className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-muted-foreground" />
              <input
                type="text"
                placeholder="Filter by Admin..."
                value={emailFilter}
                onChange={(e) => setEmailFilter(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full pl-7 pr-2 py-1 border rounded text-xs focus:ring-1 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex space-x-1">
            <button
              onClick={handleSearch}
              className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs hover:bg-blue-200"
            >
              Search
            </button>
            <button
              onClick={handleClearFilters}
              className="px-2 py-1 bg-secondary text-secondary-foreground rounded text-xs hover:bg-secondary/90"
            >
              Clear
            </button>
              <button
                onClick={handleSelectAll}
                className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs hover:bg-blue-200"
              >
                {selectAll ? 'Deselect All' : 'Select All'}
              </button>
              {selectedItems.size > 0 && (
                <>
                  <button
                    onClick={handleBulkDelete}
                    className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs hover:bg-red-200"
                  >
                    Delete Selected ({selectedItems.size})
                  </button>
                </>
              )}
              <button
                onClick={() => window.open('/standalone/', '_blank')}
                className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-xs hover:bg-gray-200"
                title="Open widget in separate window"
              >
                Open in Window
              </button>
          </div>
        </div>

      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded p-2">
          <p className="text-destructive text-xs font-medium">Error: {error}</p>
        </div>
      )}
      </div>

      {/* Table Section - Flexible Height */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="bg-card rounded border overflow-hidden flex-1 flex flex-col">
          <div className="flex-1 overflow-auto">
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead className="bg-muted/50 border-b">
              <tr>
                <th className="text-left px-1 py-1.5 font-medium w-6">
                  <input
                    type="checkbox"
                    checked={selectAll}
                    onChange={handleSelectAll}
                    className="h-3 w-3"
                  />
                </th>
                <th 
                  className="text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-8"
                  onClick={() => handleSort('index')}
                >
                  <div className="flex items-center space-x-1">
                    <span>#</span>
                    {sortField === 'index' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-2 w-2" /> : <ChevronUp className="h-2 w-2" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-24"
                  onClick={() => handleSort('name')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Name</span>
                    {sortField === 'name' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-2 w-2" /> : <ChevronUp className="h-2 w-2" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-32"
                  onClick={() => handleSort('description')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Description</span>
                    {sortField === 'description' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-2 w-2" /> : <ChevronUp className="h-2 w-2" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-32"
                  onClick={() => handleSort('email')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Admin</span>
                    {sortField === 'email' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-2 w-2" /> : <ChevronUp className="h-2 w-2" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-20"
                  onClick={() => handleSort('uid')}
                >
                  <div className="flex items-center space-x-1">
                    <span>UID</span>
                    {sortField === 'uid' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-2 w-2" /> : <ChevronUp className="h-2 w-2" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-28"
                  onClick={() => handleSort('created_at')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Created</span>
                    {sortField === 'created_at' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-2 w-2" /> : <ChevronUp className="h-2 w-2" />
                    )}
                  </div>
                </th>
                <th className="text-left px-1 py-1.5 font-medium w-20">Files</th>
                <th className="text-left px-1 py-1.5 font-medium w-40">Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedObjects.length === 0 ? (
                <tr>
                  <td colSpan={9} className="px-2 py-4 text-center text-muted-foreground">
                    {loading ? 'Loading...' : 'No syft objects found'}
                  </td>
                </tr>
              ) : (
                sortedObjects.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((obj) => (
                  <tr key={obj.uid} className={`border-b transition-colors hover:bg-muted/50 cursor-pointer ${
                    isRecentObject(obj.created_at) || clickedRows.has(obj.uid) ? 'rainbow-bg' : ''
                  }`}
                  onClick={(e) => {
                    // Only trigger if clicked on the row itself, not on buttons or inputs
                    if (e.target === e.currentTarget || (e.target as HTMLElement).closest('td:not(.actions-cell):not([data-no-click])')) {
                      const variableName = obj.name.replace(/[^a-zA-Z0-9_]/g, '_').replace(/^[0-9]/, '_$&');
                      const code = `${variableName} = syo.objects["${obj.uid}"]`;
                      copyToClipboard(code);
                      
                      // Add rainbow animation for 2 seconds
                      setClickedRows(prev => new Set(prev).add(obj.uid));
                      setTimeout(() => {
                        setClickedRows(prev => {
                          const newSet = new Set(prev);
                          newSet.delete(obj.uid);
                          return newSet;
                        });
                      }, 2000);
                    }
                  }}>
                    <td className="px-1 py-1.5 w-6" data-no-click="true" onClick={(e) => e.stopPropagation()}>
                      <input
                        type="checkbox"
                        checked={selectedItems.has(obj.uid)}
                        onChange={() => handleItemSelect(obj.uid)}
                        className="h-3 w-3"
                      />
                    </td>
                    <td className="px-1 py-1.5 w-8">{obj.index}</td>
                    <td className="px-1 py-1.5 w-24">
                      <div className="font-medium truncate text-xs">
                        <span className="text-foreground">{obj.name}</span>
                          </div>
                    </td>
                    <td className="px-1 py-1.5 w-32">
                      <div className="truncate text-xs text-muted-foreground">
                        {obj.description || '—'}
                      </div>
                    </td>
                    <td className="px-1 py-1.5 w-32" data-no-click="true">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          copyToClipboard(obj.email);
                          setCopiedEmail(obj.email);
                          setTimeout(() => setCopiedEmail(null), 2000);
                        }}
                        className={`flex items-center space-x-1 text-xs font-mono text-gray-700 hover:text-gray-900 cursor-pointer hover:bg-blue-100 hover:shadow-sm px-1 py-0.5 rounded truncate transition-all duration-500 border border-transparent hover:border-blue-200 w-full ${
                          copiedEmail === obj.email ? 'bg-gradient-to-r from-pink-200 via-red-200 via-yellow-200 via-green-200 via-blue-200 to-purple-200 text-gray-800 border-blue-300' : ''
                        }`}
                        title="Click to copy admin email to clipboard"
                      >
                        <User className="h-2 w-2 text-muted-foreground flex-shrink-0" />
                        <span className="truncate">{obj.email}</span>
                        {copiedEmail === obj.email && (
                          <span className="ml-1 text-green-700 font-semibold">✓</span>
                        )}
                      </button>
                    </td>
                    <td className="px-1 py-1.5 w-20" data-no-click="true">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          copyToClipboard(obj.uid);
                          setCopiedUid(obj.uid);
                          setTimeout(() => setCopiedUid(null), 2000);
                        }}
                        className={`text-xs font-mono text-gray-700 hover:text-gray-900 cursor-pointer hover:bg-blue-100 hover:shadow-sm px-1 py-0.5 rounded truncate transition-all duration-500 border border-transparent hover:border-blue-200 ${
                          copiedUid === obj.uid ? 'bg-gradient-to-r from-pink-200 via-red-200 via-yellow-200 via-green-200 via-blue-200 to-purple-200 text-gray-800 border-blue-300' : ''
                        }`}
                        title="Click to copy full UID to clipboard"
                      >
                        {obj.uid.substring(0, 8)}...
                        {copiedUid === obj.uid && (
                          <span className="ml-1 text-green-700 font-semibold">✓</span>
                        )}
                      </button>
                    </td>
                    <td className="px-1 py-1.5 text-muted-foreground w-28">
                      <div className="flex items-center space-x-1">
                        <Calendar className="h-2 w-2 flex-shrink-0" />
                        <span className="truncate text-xs">{formatDate(obj.created_at)}</span>
                      </div>
                    </td>
                    <td className="px-1 py-1.5 w-20" data-no-click="true" onClick={(e) => e.stopPropagation()}>
                      <div className="flex space-x-0.5">
                        {obj.file_exists.mock ? (
                          <button
                            onClick={() => {
                              const userEmail = status?.syftbox?.user_email || ''
                              const currentPermissions = getCurrentPermissions(obj.uid)
                              const canWrite = currentPermissions?.mock_write.includes(userEmail) || false
                              fetchFileContent(obj.mock_url, `Mock: ${obj.name}`, 'mock', obj.uid, canWrite)
                            }}
                            className="flex items-center space-x-0.5 px-1 py-0.5 rounded bg-slate-100 text-slate-700 hover:bg-slate-200 cursor-pointer text-xs"
                            title="Edit mock file"
                          >
                          <Globe className="h-2 w-2" />
                            <span>Mock</span>
                          </button>
                        ) : (
                          <div className="flex items-center space-x-0.5 px-1 py-0.5 rounded bg-slate-100 text-slate-700 opacity-50 text-xs">
                            <Globe className="h-2 w-2" />
                            <span>Mock</span>
                        </div>
                        )}
                        {obj.file_exists.private ? (
                          <button
                            onClick={() => {
                              const userEmail = status?.syftbox?.user_email || ''
                              const currentPermissions = getCurrentPermissions(obj.uid)
                              const canWrite = currentPermissions?.private_write.includes(userEmail) || false
                              fetchFileContent(obj.private_url, `Private: ${obj.name}`, 'private', obj.uid, canWrite)
                            }}
                            className="flex items-center space-x-0.5 px-1 py-0.5 rounded bg-gray-100 text-gray-700 hover:bg-gray-200 cursor-pointer text-xs"
                            title="Edit private file"
                          >
                          <Lock className="h-2 w-2" />
                            <span>Private</span>
                          </button>
                        ) : (
                          <div className="flex items-center space-x-0.5 px-1 py-0.5 rounded bg-red-100 text-red-800 opacity-50 text-xs">
                            <Lock className="h-2 w-2" />
                            <span>Private</span>
                      </div>
                        )}
                      </div>
                    </td>
                    <td className="px-1 py-1.5 w-40 actions-cell" data-no-click="true" onClick={(e) => e.stopPropagation()}>
                      <div className="flex space-x-0.5">
                      <button
                        onClick={() => setSelectedObject(obj)}
                          className="flex items-center px-1.5 py-0.5 bg-blue-100 text-blue-800 rounded hover:bg-blue-200 text-xs"
                          title="View object details"
                      >
                          <span>Info</span>
                      </button>
                        <button
                          onClick={() => copyPath(obj)}
                          className="flex items-center px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded hover:bg-purple-200 text-xs"
                          title="Copy local file path"
                        >
                          <span>Path</span>
                        </button>
                        <button
                          onClick={() => setDeleteModal({ isOpen: true, object: obj, loading: false })}
                          className="flex items-center px-1 py-0.5 bg-red-100 text-red-800 rounded hover:bg-red-200 text-xs"
                          title="Delete object"
                        >
                          <Trash2 className="h-2 w-2" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
            </div>
        </div>
        
        {/* Compact Pagination Controls */}
        {totalPages > 1 && (
                        <div className="flex items-center justify-between px-2 py-2 border-t bg-muted/20 flex-shrink-0">
            <div className="text-xs text-muted-foreground">
                {totalCount} objects • Page {currentPage} of {totalPages}
            </div>
            <div className="flex-1 flex justify-center">
              {clipboardNotification && (
                <div className="text-xs text-muted-foreground italic">
                  {clipboardNotification}
                </div>
              )}
            </div>
            <div className="flex items-center space-x-1">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage <= 1}
                className="flex items-center space-x-1 px-2 py-1 border rounded hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed text-xs"
              >
                <ChevronLeft className="h-3 w-3" />
                <span>Prev</span>
              </button>
              
              {/* Compact Page numbers - show max 3 */}
              <div className="flex items-center space-x-1">
                {Array.from({ length: Math.min(3, totalPages) }, (_, i) => {
                  let pageNum;
                  if (totalPages <= 3) {
                    pageNum = i + 1;
                  } else if (currentPage <= 2) {
                    pageNum = i + 1;
                  } else if (currentPage >= totalPages - 1) {
                    pageNum = totalPages - 2 + i;
                  } else {
                    pageNum = currentPage - 1 + i;
                  }
                  
                  return (
                    <button
                      key={pageNum}
                      onClick={() => handlePageChange(pageNum)}
                      className={`px-2 py-1 text-xs rounded ${
                        currentPage === pageNum
                          ? 'bg-blue-100 text-blue-800'
                          : 'hover:bg-muted'
                      }`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
              </div>
              
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage >= totalPages}
                className="flex items-center space-x-1 px-2 py-1 border rounded hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed text-xs"
              >
                <span>Next</span>
                <ChevronRight className="h-3 w-3" />
              </button>
            </div>
          </div>
        )}
        
        {/* Footer for single page or always-visible notification */}
        {totalPages <= 1 && (
          <div className="flex items-center justify-center px-2 py-2 border-t bg-muted/20 flex-shrink-0">
            {clipboardNotification && (
              <div className="text-xs text-muted-foreground italic">
                {clipboardNotification}
              </div>
            )}
          </div>
        )}
        </div>
      </div>

      {/* Compact Object Detail Modal */}
      {selectedObject && (
        <div 
          className="fixed inset-0 bg-black/50 flex items-center justify-center p-2 z-50"
          onClick={() => {
            setSelectedObject(null)
            setEditingPermissions(false)
            setEditedPermissions(null)
          }}
        >
          <div 
            className="bg-background rounded-lg max-w-4xl max-h-[95vh] overflow-y-auto w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="sticky top-0 bg-background border-b px-4 py-2">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">{selectedObject.name}</h2>
                <button
                  onClick={() => {
                    setSelectedObject(null)
                    setEditingPermissions(false)
                    setEditedPermissions(null)
                  }}
                  className="text-muted-foreground hover:text-foreground"
                >
                  ✕
                </button>
              </div>
            </div>
            <div className="p-4 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="font-semibold text-sm mb-2">Object Details</h3>
                  <div className="space-y-2 text-sm">
                    <div><span className="font-medium">UID:</span> <span className="font-mono text-xs">{selectedObject.uid}</span></div>
                    <div><span className="font-medium">Owner:</span> {selectedObject.email}</div>
                    <div><span className="font-medium">Created:</span> {formatDate(selectedObject.created_at)}</div>
                    <div><span className="font-medium">Updated:</span> {formatDate(selectedObject.updated_at)}</div>
            </div>
          </div>
                <div>
                  <h3 className="font-semibold text-sm mb-2">Files</h3>
                  <div className="space-y-2 text-sm">
                    <div><span className="font-medium">Private:</span> {selectedObject.file_exists.private ? '✓ Available' : '✗ Not found'}</div>
                    <div><span className="font-medium">Mock:</span> {selectedObject.file_exists.mock ? '✓ Available' : '✗ Not found'}</div>
        </div>
                </div>
              </div>

              {/* Permissions Section */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-sm">Permissions</h3>
                  {canEditPermissions(selectedObject) && !editingPermissions && (
                    <button
                      onClick={startEditingPermissions}
                      className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
                    >
                      Edit
                    </button>
                  )}
                  {editingPermissions && (
                    <div className="flex space-x-1">
                      <button
                        onClick={savePermissions}
                        disabled={savingPermissions}
                        className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200 disabled:opacity-50 flex items-center space-x-1"
                      >
                        {savingPermissions && <RefreshCw className="h-3 w-3 animate-spin" />}
                        <span>{savingPermissions ? 'Saving...' : 'Save'}</span>
                      </button>
                      <button
                        onClick={cancelEditingPermissions}
                        className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded hover:bg-gray-200"
                      >
                        Cancel
                      </button>
                    </div>
                  )}
                </div>

                {editingPermissions && editedPermissions ? (
                  <PermissionEditor
                    permissions={editedPermissions}
                    onAddPermission={addPermission}
                    onRemovePermission={removePermission}
                  />
                ) : (
                  <div className="grid grid-cols-3 gap-4 text-xs">
                    <div>
                      <h4 className="font-medium text-green-700 mb-1">Private Data</h4>
                      <div className="space-y-1">
                        <div><span className="font-medium">Read:</span> {selectedObject.permissions.private_read.length > 0 ? selectedObject.permissions.private_read.join(', ') : 'None'}</div>
                        <div><span className="font-medium">Write:</span> {selectedObject.permissions.private_write.length > 0 ? selectedObject.permissions.private_write.join(', ') : 'None'}</div>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-blue-700 mb-1">Mock Data</h4>
                      <div className="space-y-1">
                        <div><span className="font-medium">Read:</span> {selectedObject.permissions.mock_read.length > 0 ? selectedObject.permissions.mock_read.join(', ') : 'None'}</div>
                        <div><span className="font-medium">Write:</span> {selectedObject.permissions.mock_write.length > 0 ? selectedObject.permissions.mock_write.join(', ') : 'None'}</div>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-purple-700 mb-1">Syft Object</h4>
                      <div className="space-y-1">
                        <div><span className="font-medium">Access:</span> {selectedObject.permissions.syftobject.length > 0 ? selectedObject.permissions.syftobject.join(', ') : 'None'}</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              {selectedObject.description && (
                <div>
                  <h3 className="font-semibold text-sm mb-2">Description</h3>
                  <p className="text-sm text-muted-foreground">{selectedObject.description}</p>
                </div>
              )}
              
              <div>
                <h3 className="font-semibold text-sm mb-2">URLs</h3>
                <div className="space-y-2 text-xs font-mono">
                  <div><span className="font-medium">Private:</span> {selectedObject.private_url}</div>
                  <div><span className="font-medium">Mock:</span> {selectedObject.mock_url}</div>
                  <div><span className="font-medium">Syft Object:</span> {selectedObject.syftobject_url}</div>
                </div>
              </div>
              
              {selectedObject.metadata && Object.keys(selectedObject.metadata).length > 0 && (
                <div>
                  <h3 className="font-semibold text-sm mb-2">Metadata</h3>
                  <pre className="text-xs bg-muted/20 p-3 rounded overflow-auto max-h-40">
                    {JSON.stringify(selectedObject.metadata, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* File Content Editor Modal */}
      {fileContentModal.isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 flex items-center justify-center p-2 z-50"
          onClick={() => setFileContentModal({
            isOpen: false,
            title: '',
            content: '',
            editedContent: '',
            loading: false,
            saving: false,
            fileType: null,
            objectUid: null,
            canWrite: false
          })}
        >
          <div 
            className="bg-background rounded-lg max-w-4xl max-h-[95vh] overflow-hidden w-full flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="bg-background border-b px-4 py-2 flex-shrink-0">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">{fileContentModal.title}</h2>
                <button
                  onClick={() => setFileContentModal({
                    isOpen: false,
                    title: '',
                    content: '',
                    editedContent: '',
                    loading: false,
                    saving: false,
                    fileType: null,
                    objectUid: null,
                    canWrite: false
                  })}
                  className="text-muted-foreground hover:text-foreground"
                >
                  ✕
                </button>
              </div>
            </div>
            <div className="flex-1 overflow-hidden p-4 flex flex-col">
              {fileContentModal.loading ? (
                <div className="flex items-center justify-center h-32">
                  <RefreshCw className="h-6 w-6 animate-spin text-blue-600" />
                  <span className="ml-2">Loading file content...</span>
                </div>
              ) : (
                <>
                  <textarea
                    value={fileContentModal.editedContent}
                    onChange={(e) => setFileContentModal(prev => ({ ...prev, editedContent: e.target.value }))}
                    className="flex-1 w-full text-sm font-mono bg-muted/20 p-4 rounded border resize-none focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="File content..."
                    readOnly={!fileContentModal.canWrite}
                  />
                  <div className="flex items-center justify-between mt-4">
                    <div className="text-xs text-muted-foreground">
                      {fileContentModal.canWrite ? (
                        "You can edit and save this file"
                      ) : (
                        "You don't have write permission for this file"
                      )}
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setFileContentModal(prev => ({ ...prev, editedContent: prev.content }))}
                        disabled={fileContentModal.editedContent === fileContentModal.content}
                        className="px-3 py-1 text-sm bg-secondary text-secondary-foreground rounded hover:bg-secondary/90 disabled:opacity-50"
                      >
                        Reset
                      </button>
                      <button
                        onClick={saveFileContent}
                        disabled={!fileContentModal.canWrite || fileContentModal.saving || fileContentModal.editedContent === fileContentModal.content}
                        className="px-3 py-1 text-sm bg-green-100 text-green-800 rounded hover:bg-green-200 disabled:opacity-50 flex items-center space-x-1"
                      >
                        {fileContentModal.saving && <RefreshCw className="h-3 w-3 animate-spin" />}
                        <span>{fileContentModal.saving ? 'Saving...' : 'Save'}</span>
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteModal.isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 flex items-center justify-center p-2 z-50"
          onClick={() => setDeleteModal({ isOpen: false, object: null, loading: false })}
        >
          <div 
            className="bg-background rounded-lg max-w-md w-full p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center space-x-3 mb-4">
                             <div className="flex-shrink-0 w-10 h-10 mx-auto bg-red-100 rounded-full flex items-center justify-center">
                 <Trash2 className="h-5 w-5 text-red-600" />
               </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {deleteModal.object ? 'Delete Object' : 'Delete Selected Objects'}
                </h3>
                <p className="text-sm text-gray-500">This action cannot be undone.</p>
              </div>
            </div>
            
            <div className="mb-6">
              {deleteModal.object ? (
                <>
                  <p className="text-sm text-gray-700">
                    Are you sure you want to delete "<span className="font-medium">{deleteModal.object.name}</span>"?
                  </p>
                  <p className="text-xs text-gray-500 mt-2">
                    This will permanently delete all associated files (private, mock, and syft object files).
                  </p>
                </>
              ) : (
                <>
                  <p className="text-sm text-gray-700">
                    Are you sure you want to delete <span className="font-medium">{selectedItems.size} selected objects</span>?
                  </p>
                  <p className="text-xs text-gray-500 mt-2">
                    This will permanently delete all associated files (private, mock, and syft object files) for all selected objects.
                  </p>
                  <div className="mt-3 max-h-20 overflow-y-auto">
                    <p className="text-xs text-gray-600 font-medium">Objects to delete:</p>
                    <ul className="text-xs text-gray-500 mt-1">
                      {sortedObjects.filter(obj => selectedItems.has(obj.uid)).map(obj => (
                        <li key={obj.uid}>• {obj.name}</li>
                      ))}
                    </ul>
                  </div>
                </>
              )}
            </div>
            
            <div className="flex space-x-3 justify-end">
              <button
                onClick={() => setDeleteModal({ isOpen: false, object: null, loading: false })}
                disabled={deleteModal.loading}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={() => deleteModal.object ? deleteObject(deleteModal.object.uid) : deleteBulkObjects()}
                disabled={deleteModal.loading}
                className="px-4 py-2 text-sm font-medium text-red-800 bg-red-100 rounded-md hover:bg-red-200 disabled:opacity-50 flex items-center space-x-2"
              >
                {deleteModal.loading && <RefreshCw className="h-4 w-4 animate-spin" />}
                <span>{deleteModal.loading ? 'Deleting...' : 'Delete'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  )
} 