'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const router = useRouter()
  
  useEffect(() => {
    router.push('/widget')
  }, [router])
  
  return (
    <div className="flex min-h-screen items-center justify-center">
      <p className="text-gray-500">Redirecting to widget...</p>
    </div>
  )
}
