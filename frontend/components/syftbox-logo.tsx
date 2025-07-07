'use client'

export function SyftBoxLogo({ className = "" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="syftGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#1e40af" className="animate-gradient" />
          <stop offset="100%" stopColor="#7c3aed" className="animate-gradient" />
        </linearGradient>
      </defs>
      <rect width="200" height="200" rx="40" fill="url(#syftGradient)" />
      <path
        d="M100 40 L130 60 L130 100 L100 120 L70 100 L70 60 Z"
        fill="white"
        fillOpacity="0.9"
      />
      <path
        d="M100 80 L130 100 L130 140 L100 160 L70 140 L70 100 Z"
        fill="white"
        fillOpacity="0.7"
      />
    </svg>
  )
}
