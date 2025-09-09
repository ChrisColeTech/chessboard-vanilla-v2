import React from 'react'

interface ChessboardLayoutProps {
  children?: React.ReactNode
  topLeft?: React.ReactNode
  top?: React.ReactNode
  topRight?: React.ReactNode
  left?: React.ReactNode
  center: React.ReactNode
  right?: React.ReactNode
  bottomLeft?: React.ReactNode
  bottom?: React.ReactNode
  bottomRight?: React.ReactNode
  className?: string
}

export const ChessboardLayout: React.FC<ChessboardLayoutProps> = ({
  topLeft,
  top,
  topRight,
  left,
  center,
  right,
  bottomLeft,
  bottom,
  bottomRight,
  className = ""
}) => {
  return (
    <div 
      className={`w-full h-full border-2 border-border p-2 ${className}`}
      style={{
        display: 'grid',
        gridTemplateColumns: '100px 1fr 100px',
        gridTemplateRows: '80px 1fr 80px',
        gap: '8px',
        minHeight: '0'
      }}
    >
      {/* Row 1 */}
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {topLeft}
      </div>
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {top}
      </div>
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {topRight}
      </div>
      
      {/* Row 2 */}
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {left}
      </div>
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {center}
      </div>
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {right}
      </div>
      
      {/* Row 3 */}
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {bottomLeft}
      </div>
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {bottom}
      </div>
      <div 
        className="flex items-center justify-center border border-border/50 p-2 rounded"
        style={{ minHeight: '0', minWidth: '0' }}
      >
        {bottomRight}
      </div>
    </div>
  )
}