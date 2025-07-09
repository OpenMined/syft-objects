import { SyftObject, ClientInfo, StatusInfo } from './types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || ''

export const api = {
  async getStatus(): Promise<StatusInfo> {
    const res = await fetch(`${API_BASE}/api/status`)
    if (!res.ok) throw new Error('Failed to fetch status')
    return res.json()
  },

  async getObjects(params?: {
    search?: string
    admin_email?: string
    skip?: number
    limit?: number
  }): Promise<{ objects: SyftObject[]; total: number }> {
    const searchParams = new URLSearchParams()
    if (params?.search) searchParams.set('search', params.search)
    if (params?.admin_email) searchParams.set('admin_email', params.admin_email)
    if (params?.skip !== undefined) searchParams.set('skip', params.skip.toString())
    if (params?.limit !== undefined) searchParams.set('limit', params.limit.toString())

    const res = await fetch(`${API_BASE}/api/objects?${searchParams}`)
    if (!res.ok) throw new Error('Failed to fetch objects')
    return res.json()
  },

  async getObject(uid: string): Promise<SyftObject> {
    const res = await fetch(`${API_BASE}/api/objects/${uid}`)
    if (!res.ok) throw new Error('Failed to fetch object')
    return res.json()
  },

  async createObject(formData: FormData): Promise<SyftObject> {
    const res = await fetch(`${API_BASE}/api/objects`, {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) throw new Error('Failed to create object')
    return res.json()
  },

  async deleteObject(uid: string): Promise<void> {
    const res = await fetch(`${API_BASE}/api/objects/${uid}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Failed to delete object')
  },

  async updateFile(uid: string, fileType: 'private' | 'mock', content: string): Promise<void> {
    const res = await fetch(`${API_BASE}/api/objects/${uid}/file/${fileType}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'text/plain' },
      body: content,
    })
    if (!res.ok) throw new Error('Failed to update file')
  },

  async updatePermissions(uid: string, permissions: Record<string, string[]>): Promise<void> {
    const res = await fetch(`${API_BASE}/api/objects/${uid}/permissions`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(permissions),
    })
    if (!res.ok) throw new Error('Failed to update permissions')
  },

  async getClientInfo(): Promise<ClientInfo> {
    const res = await fetch(`${API_BASE}/api/client-info`)
    if (!res.ok) throw new Error('Failed to fetch client info')
    return res.json()
  },

  async refreshObjects(): Promise<void> {
    const res = await fetch(`${API_BASE}/api/objects/refresh`)
    if (!res.ok) throw new Error('Failed to refresh objects')
  },

  async getEmails(): Promise<string[]> {
    const res = await fetch(`${API_BASE}/api/metadata/emails`)
    if (!res.ok) throw new Error('Failed to fetch emails')
    return res.json()
  },

  async getFileContent(syftUrl: string): Promise<string> {
    const res = await fetch(`${API_BASE}/api/file?syft_url=${encodeURIComponent(syftUrl)}`)
    if (!res.ok) throw new Error('Failed to fetch file content')
    return res.text()
  },

  async getObjectMetadata(uid: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/object/${uid}/metadata`)
    if (!res.ok) throw new Error('Failed to fetch object metadata')
    return res.json()
  }
}
