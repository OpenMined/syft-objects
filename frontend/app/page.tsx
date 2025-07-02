'use client'

import { useEffect, useState } from 'react'
import { RefreshCw, Search, Filter, Eye, Globe, Lock, Calendar, User, FileText } from 'lucide-react'

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

  const fetchObjects = async (search?: string, emailFilter?: string) => {
    try {
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (emailFilter) params.append('email_filter', emailFilter)
      params.append('limit', '50')

      const response = await fetch(`${API_BASE}/api/objects?${params}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch objects: ${response.statusText}`)
      }
      
      const data: ApiResponse = await response.json()
      setObjects(data.objects)
      setTotalCount(data.total_count)
      setSearchInfo(data.search_info)
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
      await fetchObjects(searchTerm, emailFilter)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh objects')
    } finally {
      setRefreshing(false)
    }
  }

  const handleSearch = () => {
    fetchObjects(searchTerm, emailFilter)
  }

  const handleClearFilters = () => {
    setSearchTerm('')
    setEmailFilter('')
    fetchObjects()
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A'
    try {
      return new Date(dateString).toLocaleString()
    } catch {
      return 'Invalid date'
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
        {searchInfo && (
          <div className="mt-3 text-sm text-muted-foreground">
            {searchInfo} ({totalCount} objects)
          </div>
        )}
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
                <th className="text-left px-4 py-3 font-medium">#</th>
                <th className="text-left px-4 py-3 font-medium">Name</th>
                <th className="text-left px-4 py-3 font-medium">Email</th>
                <th className="text-left px-4 py-3 font-medium">Files</th>
                <th className="text-left px-4 py-3 font-medium">Created</th>
                <th className="text-left px-4 py-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {objects.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                    {loading ? 'Loading...' : 'No syft objects found'}
                  </td>
                </tr>
              ) : (
                objects.map((obj) => (
                  <tr key={obj.uid} className="border-b hover:bg-muted/25">
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
      </div>

      {/* Object Detail Modal */}
      {selectedObject && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-background rounded-lg max-w-4xl max-h-[90vh] overflow-y-auto w-full">
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
                    <div><span className="font-medium">UID:</span> {selectedObject.uid}</div>
                    <div><span className="font-medium">Email:</span> {selectedObject.email}</div>
                    <div><span className="font-medium">Created:</span> {formatDate(selectedObject.created_at)}</div>
                    <div><span className="font-medium">Updated:</span> {formatDate(selectedObject.updated_at)}</div>
                  </div>
                </div>
                <div>
                  <h3 className="font-medium mb-2">URLs</h3>
                  <div className="space-y-2 text-sm">
                    <div><span className="font-medium">Private:</span> <code className="text-xs bg-muted px-1 rounded">{selectedObject.private_url}</code></div>
                    <div><span className="font-medium">Mock:</span> <code className="text-xs bg-muted px-1 rounded">{selectedObject.mock_url}</code></div>
                    <div><span className="font-medium">Metadata:</span> <code className="text-xs bg-muted px-1 rounded">{selectedObject.syftobject_url}</code></div>
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