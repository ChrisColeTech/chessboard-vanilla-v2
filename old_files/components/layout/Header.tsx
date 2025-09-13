import { Coins } from 'lucide-react'
import { useCoinsModal } from '../../stores/appStore'

interface HeaderProps {
  onOpenSettings: () => void
  isSettingsOpen: boolean
  coinBalance?: number
}

export function Header({ coinBalance }: HeaderProps) {
  const { open: openCoinsModal } = useCoinsModal()
  
  const handleCoinClick = () => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    openCoinsModal()
  }
  return (
    <div className="w-full h-16">
      <div className="container mx-auto px-6 h-full">
        <div className="flex items-center justify-between h-full">
          <div className="flex items-center gap-3">
            {/* Title and icon moved to TitleBar */}
          </div>
          
          <div className="flex items-center gap-4">
            {coinBalance !== undefined && (
              <button
                onClick={handleCoinClick}
                className="flex items-center gap-2 bg-background/50 px-3 py-1 rounded-lg border border-border hover:bg-background/70 hover:border-accent/50 transition-all duration-200 cursor-pointer group"
                aria-label="View coin balance details"
              >
                <Coins className="w-4 h-4 text-accent animate-pulse group-hover:scale-110 transition-transform duration-200" />
                <span className="text-sm font-bold text-foreground">{coinBalance.toLocaleString()}</span>
                <span className="text-xs text-muted-foreground">coins</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}