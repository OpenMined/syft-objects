'use client'

import Widget from '../widget/page'

export default function StandalonePage() {
  return (
    <div className="h-[600px] bg-gray-50">
      <div className="h-full bg-white">
        <Widget />
      </div>
    </div>
  )
} 