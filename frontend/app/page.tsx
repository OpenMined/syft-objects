'use client'

import { useEffect, useState, useCallback, useRef } from 'react'
import { RefreshCw, Search, Filter, Eye, Globe, Lock, Calendar, User, FileText, ChevronUp, ChevronDown, ChevronLeft, ChevronRight } from 'lucide-react'

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

export default function Home() {
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
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(25)
  const [totalPages, setTotalPages] = useState(0)

  // Refs to avoid auto-refresh dependency issues
  const currentPageRef = useRef(currentPage)
  const searchTermRef = useRef(searchTerm)
  const emailFilterRef = useRef(emailFilter)

  // Update refs when state changes
  useEffect(() => { currentPageRef.current = currentPage }, [currentPage])
  useEffect(() => { searchTermRef.current = searchTerm }, [searchTerm])
  useEffect(() => { emailFilterRef.current = emailFilter }, [emailFilter])

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

  const fetchObjects = async (search?: string, emailFilter?: string, page: number = currentPage) => {
    try {
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (emailFilter) params.append('email_filter', emailFilter)
      params.append('limit', itemsPerPage.toString())
      params.append('offset', ((page - 1) * itemsPerPage).toString())

      const response = await fetch(`${API_BASE}/api/objects?${params}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch objects: ${response.statusText}`)
      }
      
      const data: ApiResponse = await response.json()
      
      setObjects(data.objects)
      setTotalCount(data.total_count)
      setTotalPages(Math.ceil(data.total_count / itemsPerPage))
      setSearchInfo(data.search_info || null)
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
      await fetchObjects(searchTerm, emailFilter, currentPage)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh objects')
    } finally {
      setRefreshing(false)
    }
  }

  const handleSearch = () => {
    setCurrentPage(1) // Reset to first page when searching
    fetchObjects(searchTerm, emailFilter, 1)
  }

  const handleClearFilters = () => {
    setSearchTerm('')
    setEmailFilter('')
    setCurrentPage(1) // Reset to first page when clearing filters
    fetchObjects('', '', 1)
  }

  // Pagination functions
  const handlePageChange = (page: number) => {
    setCurrentPage(page)
    fetchObjects(searchTerm, emailFilter, page)
  }

  const handleItemsPerPageChange = (newItemsPerPage: number) => {
    setItemsPerPage(newItemsPerPage)
    setCurrentPage(1) // Reset to first page when changing items per page
    // Use setTimeout to ensure state updates have taken effect
    setTimeout(() => {
      fetchObjects(searchTerm, emailFilter, 1)
    }, 0)
  }

  const sortObjects = useCallback((objectsToSort: SyftObject[], field: keyof SyftObject, direction: 'asc' | 'desc') => {
    return [...objectsToSort].sort((a, b) => {
      let aValue = a[field]
      let bValue = b[field]

      // Handle null/undefined values
      if (aValue === null || aValue === undefined) aValue = ''
      if (bValue === null || bValue === undefined) bValue = ''

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

  // Apply sorting when objects or sort parameters change
  useEffect(() => {
    const sorted = sortObjects(objects, sortField, sortDirection)
    setSortedObjects(sorted)
  }, [objects, sortField, sortDirection, sortObjects])

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
      fetchObjects(searchTermRef.current, emailFilterRef.current, currentPageRef.current)
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
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center space-y-4">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto text-blue-600" />
          <p className="text-muted-foreground">Loading syft objects...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Status Card */}
      {status && (
        <div className="bg-card rounded-lg border p-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">{status.app} v{status.version}</h2>
              <div className="flex items-center space-x-4 mt-2 text-sm text-muted-foreground">
                <span className="flex items-center space-x-1">
                  <div className={`w-2 h-2 rounded-full ${
                    status.syftbox.status === 'connected' ? 'bg-green-500' : 'bg-red-500'
                  }`} />
                  <span>SyftBox: {status.syftbox.status}</span>
                </span>
                {status.syftbox.user_email && (
                  <span className="flex items-center space-x-1">
                    <User className="h-3 w-3" />
                    <span>{status.syftbox.user_email}</span>
                  </span>
                )}
                <span className="flex items-center space-x-1">
                  <div className={`w-2 h-2 rounded-full ${
                    status.components.objects_collection === 'available' ? 'bg-green-500' : 'bg-red-500'
                  }`} />
                  <span>Objects: {status.components.objects_collection}</span>
                </span>
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                  autoRefresh 
                    ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}
              >
                <div className={`w-2 h-2 rounded-full ${autoRefresh ? 'bg-green-500' : 'bg-gray-500'}`} />
                <span>Auto</span>
              </button>
              <button
                onClick={refreshObjects}
                disabled={refreshing}
                className="flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50"
              >
                <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Search and Filters */}
      <div className="bg-card rounded-lg border p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search objects..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex-1">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Filter by email..."
                value={emailFilter}
                onChange={(e) => setEmailFilter(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleSearch}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
            >
              Search
            </button>
            <button
              onClick={handleClearFilters}
              className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90"
            >
              Clear
            </button>
          </div>
        </div>
        <div className="mt-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-sm text-muted-foreground">
          <div>
            {searchInfo && `${searchInfo} • `}
            {totalCount} objects total
            {sortField && (
              <span className="ml-2">
                • Sorted by {sortField === 'created_at' ? 'creation date' : sortField} 
                ({sortDirection === 'desc' ? 'newest first' : 'oldest first'})
              </span>
            )}
            <span className="ml-2">
              • Showing {((currentPage - 1) * itemsPerPage) + 1}-{Math.min(currentPage * itemsPerPage, totalCount)} of {totalCount}
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-xs">Per page:</span>
              <select
                value={itemsPerPage}
                onChange={(e) => handleItemsPerPageChange(Number(e.target.value))}
                className="text-xs border rounded px-2 py-1 bg-background"
              >
                <option value={10}>10</option>
                <option value={25}>25</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${autoRefresh ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
              <span className="text-xs">
                {autoRefresh ? 'Auto-refreshing every 1s' : 'Auto-refresh disabled'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
          <p className="text-destructive font-medium">Error: {error}</p>
        </div>
      )}

      {/* Objects Table */}
      <div className="bg-card rounded-lg border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50 border-b">
              <tr>
                <th 
                  className="text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none"
                  onClick={() => handleSort('index')}
                >
                  <div className="flex items-center space-x-1">
                    <span>#</span>
                    {sortField === 'index' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-3 w-3" /> : <ChevronUp className="h-3 w-3" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none"
                  onClick={() => handleSort('name')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Name</span>
                    {sortField === 'name' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-3 w-3" /> : <ChevronUp className="h-3 w-3" />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none"
                  onClick={() => handleSort('email')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Email</span>
                    {sortField === 'email' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-3 w-3" /> : <ChevronUp className="h-3 w-3" />
                    )}
                  </div>
                </th>
                <th className="text-left px-4 py-3 font-medium">Files</th>
                <th 
                  className="text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none"
                  onClick={() => handleSort('created_at')}
                >
                  <div className="flex items-center space-x-1">
                    <span>Created</span>
                    {sortField === 'created_at' && (
                      sortDirection === 'desc' ? <ChevronDown className="h-3 w-3" /> : <ChevronUp className="h-3 w-3" />
                    )}
                  </div>
                </th>
                <th className="text-left px-4 py-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedObjects.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                    {loading ? 'Loading...' : 'No syft objects found'}
                  </td>
                </tr>
              ) : (
                sortedObjects.map((obj) => (
                  <tr key={obj.uid} className={`border-b transition-colors hover:bg-muted/50 ${
                    isRecentObject(obj.created_at) ? 'rainbow-bg' : ''
                  }`}>
                    <td className="px-4 py-3 text-sm">{obj.index}</td>
                    <td className="px-4 py-3">
                      <div>
                        <div className="font-medium">{obj.name}</div>
                        {obj.description && (
                          <div className="text-sm text-muted-foreground truncate max-w-xs">
                            {obj.description}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div className="flex items-center space-x-1">
                        <User className="h-3 w-3 text-muted-foreground" />
                        <span>{obj.email}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex space-x-2">
                        <div className={`flex items-center space-x-1 px-2 py-1 rounded text-xs ${
                          obj.file_exists.private ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          <Lock className="h-3 w-3" />
                          <span>Private</span>
                        </div>
                        <div className={`flex items-center space-x-1 px-2 py-1 rounded text-xs ${
                          obj.file_exists.mock ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          <Globe className="h-3 w-3" />
                          <span>Mock</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <Calendar className="h-3 w-3" />
                        <span>{formatDate(obj.created_at)}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => setSelectedObject(obj)}
                        className="flex items-center space-x-1 px-3 py-1 bg-primary text-primary-foreground rounded text-sm hover:bg-primary/90"
                      >
                        <Eye className="h-3 w-3" />
                        <span>View</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        
        {/* Pagination Controls */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t">
            <div className="text-sm text-muted-foreground">
              Page {currentPage} of {totalPages}
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage <= 1}
                className="flex items-center space-x-1 px-3 py-1 border rounded-lg hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="h-4 w-4" />
                <span>Previous</span>
              </button>
              
              {/* Page numbers */}
              <div className="flex items-center space-x-1">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum;
                  if (totalPages <= 5) {
                    pageNum = i + 1;
                  } else if (currentPage <= 3) {
                    pageNum = i + 1;
                  } else if (currentPage >= totalPages - 2) {
                    pageNum = totalPages - 4 + i;
                  } else {
                    pageNum = currentPage - 2 + i;
                  }
                  
                  return (
                    <button
                      key={pageNum}
                      onClick={() => handlePageChange(pageNum)}
                      className={`px-3 py-1 text-sm rounded ${
                        currentPage === pageNum
                          ? 'bg-primary text-primary-foreground'
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
                className="flex items-center space-x-1 px-3 py-1 border rounded-lg hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span>Next</span>
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Object Detail Modal */}
      {selectedObject && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-background rounded-lg max-w-6xl max-h-[90vh] overflow-y-auto w-full">
            <div className="sticky top-0 bg-background border-b px-6 py-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">{selectedObject.name}</h2>
                <button
                  onClick={() => setSelectedObject(null)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  ✕
                </button>
              </div>
            </div>
            <div className="p-6 space-y-6">
              {/* Basic Info */}
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-medium mb-2">Basic Information</h3>
                  <div className="space-y-2 text-sm">
                    <div>
                      <div className="font-medium mb-1">UID:</div>
                      <code className="text-xs bg-muted px-2 py-1 rounded block break-all">{selectedObject.uid}</code>
                    </div>
                    <div><span className="font-medium">Email:</span> {selectedObject.email}</div>
                    <div><span className="font-medium">Created:</span> {formatDate(selectedObject.created_at)}</div>
                    <div><span className="font-medium">Updated:</span> {formatDate(selectedObject.updated_at)}</div>
                  </div>
                </div>
                <div>
                  <h3 className="font-medium mb-2">URLs</h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <div className="font-medium mb-1">Private:</div>
                      <code className="text-xs bg-muted px-2 py-1 rounded block break-all">{selectedObject.private_url}</code>
                    </div>
                    <div>
                      <div className="font-medium mb-1">Mock:</div>
                      <code className="text-xs bg-muted px-2 py-1 rounded block break-all">{selectedObject.mock_url}</code>
                    </div>
                    <div>
                      <div className="font-medium mb-1">Metadata:</div>
                      <code className="text-xs bg-muted px-2 py-1 rounded block break-all">{selectedObject.syftobject_url}</code>
                    </div>
                  </div>
                </div>
              </div>

              {/* Description */}
              {selectedObject.description && (
                <div>
                  <h3 className="font-medium mb-2">Description</h3>
                  <p className="text-sm text-muted-foreground">{selectedObject.description}</p>
                </div>
              )}

              {/* Permissions */}
              <div>
                <h3 className="font-medium mb-2">Permissions</h3>
                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="font-medium text-xs text-muted-foreground mb-1">READ PERMISSIONS</div>
                    <div className="space-y-1">
                      <div><span className="font-medium">Metadata:</span> {selectedObject.permissions.syftobject.join(', ') || 'None'}</div>
                      <div><span className="font-medium">Mock:</span> {selectedObject.permissions.mock_read.join(', ') || 'None'}</div>
                      <div><span className="font-medium">Private:</span> {selectedObject.permissions.private_read.join(', ') || 'None'}</div>
                    </div>
                  </div>
                  <div>
                    <div className="font-medium text-xs text-muted-foreground mb-1">WRITE PERMISSIONS</div>
                    <div className="space-y-1">
                      <div><span className="font-medium">Mock:</span> {selectedObject.permissions.mock_write.join(', ') || 'None'}</div>
                      <div><span className="font-medium">Private:</span> {selectedObject.permissions.private_write.join(', ') || 'None'}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Metadata */}
              {Object.keys(selectedObject.metadata).length > 0 && (
                <div>
                  <h3 className="font-medium mb-2">Metadata</h3>
                  <div className="bg-muted rounded p-3">
                    <pre className="text-xs overflow-auto">
                      {JSON.stringify(selectedObject.metadata, null, 2)}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 