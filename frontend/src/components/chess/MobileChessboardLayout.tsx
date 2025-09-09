import React, { useState, useEffect } from 'react'

interface MobileChessboardLayoutProps {
  children?: React.ReactNode
  topPieces?: React.ReactNode
  center: React.ReactNode
  bottomPieces?: React.ReactNode
  className?: string
}

export const MobileChessboardLayout: React.FC<MobileChessboardLayoutProps> = ({
  topPieces,
  center,
  bottomPieces,
  className = ""
}) => {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoaded(true)
    }, 200)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div 
      className={`w-full h-full relative transition-all duration-300 ease-in-out ${
        isLoaded ? 'opacity-100' : 'opacity-60'
      } ${className}`}
      style={{
        display: 'grid',
        gridTemplateRows: '80px auto 80px',
        boxSizing: 'border-box'
      }}
    >
      {/* Loading overlay */}
      {!isLoaded && (
        <div 
          className="absolute inset-0 z-10 flex items-center justify-center"
          style={{
            background: 'var(--background)',
            backdropFilter: 'blur(8px)',
            opacity: 0.95
          }}
        >
          <div className="text-muted-foreground">Loading...</div>
        </div>
      )}
      {/* Top captured pieces - compact horizontal layout without rounded corners */}
      {topPieces && (
        <div 
          className="transition-all duration-300 ease-in-out"
          style={{
            display: 'flex',
            alignItems: 'center',
            width: '100%',
            height: '100%',
            boxSizing: 'border-box',
            overflow: 'hidden',
            transform: 'translateZ(0)', // Hardware acceleration
            backdropFilter: 'blur(24px)',
            backgroundColor: 'color-mix(in srgb, var(--card) 80%, transparent)',
            border: '1px solid color-mix(in srgb, var(--border) 20%, transparent)'
          }}
        >
          <div 
            className="transition-transform duration-200 ease-in-out hover:scale-105"
            style={{ flex: 1, width: '100%', height: '100%' }}
          >
            {topPieces}
          </div>
        </div>
      )}
      
      {/* Center chessboard - takes remaining space but maintains aspect ratio */}
      <div 
        className="transition-all duration-300 ease-out"
        style={{ 
          width: '100%',
          height: '100%',
          minHeight: '0',
          boxSizing: 'border-box',
          overflow: 'hidden',
          transform: 'translateZ(0)', // Hardware acceleration
          border: '2px solid var(--border)'
        }}
      >
        {center}
      </div>
      
      {/* Bottom captured pieces - compact horizontal layout without rounded corners */}
      {bottomPieces && (
        <div 
          className="transition-all duration-300 ease-in-out"
          style={{
            display: 'flex',
            alignItems: 'center',
            width: '100%',
            height: '100%',
            boxSizing: 'border-box',
            overflow: 'hidden',
            transform: 'translateZ(0)', // Hardware acceleration
            backdropFilter: 'blur(24px)',
            backgroundColor: 'color-mix(in srgb, var(--card) 80%, transparent)',
            border: '1px solid color-mix(in srgb, var(--border) 20%, transparent)'
          }}
        >
          <div 
            className="transition-transform duration-200 ease-in-out hover:scale-105"
            style={{ flex: 1, width: '100%', height: '100%' }}
          >
            {bottomPieces}
          </div>
        </div>
      )}
    </div>
  )
}