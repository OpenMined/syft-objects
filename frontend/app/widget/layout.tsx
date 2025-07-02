import type { Metadata } from 'next'
import '../globals.css'

export const metadata: Metadata = {
  title: 'SyftObjects Widget',
  description: 'SyftObjects Widget for Jupyter notebooks',
}

export default function WidgetLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="fixed inset-0 w-full h-full bg-background p-0 m-0 overflow-auto">
      {children}
    </div>
  )
} 