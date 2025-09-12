
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
  return (
    <div 
      className={`w-full h-full flex flex-col gap-2 p-2 ${className}`}
      style={{ minHeight: '100%' }}
    >
      {/* Top pieces area */}
      <div 
        className="w-full flex items-center justify-center border border-border/50 p-4 rounded"
        style={{ minHeight: '80px' }}
      >
        {topPieces}
      </div>

      {/* Center board area */}
      <div 
        className="w-full flex-1 flex items-center justify-center border border-border/50 p-4 rounded"
        style={{ minHeight: '300px' }}
      >
        {center}
      </div>

      {/* Bottom pieces area */}
      <div 
        className="w-full flex items-center justify-center border border-border/50 p-4 rounded"
        style={{ minHeight: '80px' }}
      >
        {bottomPieces}
      </div>
    </div>
  )
}