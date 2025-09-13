import { HiOutlineMenu } from 'react-icons/hi';
import { VscChromeMinimize, VscChromeMaximize, VscChromeClose } from 'react-icons/vsc';
import { Crown, Sun, Moon } from 'lucide-react';
import { useTheme } from '../../stores/appStore';

interface TitleBarProps {
  onMenuClick?: () => void;
  onMinimize?: () => void;
  onMaximize?: () => void;
  onClose?: () => void;
}

export function TitleBar({ 
  onMenuClick, 
  onMinimize, 
  onMaximize, 
  onClose 
}: TitleBarProps) {
  const { isDarkMode, toggleMode } = useTheme();
  // Force Tailwind to regenerate titlebar classes
  return (
    <div className="w-full h-10 bg-titlebar flex items-center justify-between select-none" style={{ WebkitAppRegion: 'drag' }}>
      {/* Left side - Hamburger menu + App title */}
      <div className="flex items-center">
        <button
          onClick={onMenuClick}
          className="w-12 h-10 flex items-center justify-center titlebar-btn hover:bg-titlebar-hover transition-colors duration-200 text-titlebar-foreground"
          title="Menu"
          style={{ WebkitAppRegion: 'no-drag' }}
        >
          <HiOutlineMenu className="w-4 h-4" />
        </button>
        <div className="flex items-center gap-2 px-3">
          <Crown className="w-4 h-4 text-titlebar-foreground" />
          <span className="text-sm font-medium text-titlebar-foreground">Master Chess Training</span>
          <span className="text-xs text-titlebar-foreground opacity-60">POC</span>
        </div>
      </div>

      {/* Center - Spacer */}
      <div className="flex-1"></div>

      {/* Right side - Dark mode toggle (always) + Window controls (desktop only) */}
      <div className="flex items-center">
        <button
          onClick={toggleMode}
          className="w-12 h-10 flex items-center justify-center titlebar-btn hover:bg-titlebar-hover transition-colors duration-200 text-titlebar-foreground"
          title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
          style={{ WebkitAppRegion: 'no-drag' }}
        >
          {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
        <div className="hidden md:flex items-center">
        <button
          onClick={onMinimize}
          className="w-12 h-10 flex items-center justify-center titlebar-btn hover:bg-titlebar-hover transition-colors duration-200 text-titlebar-foreground"
          title="Minimize"
          style={{ WebkitAppRegion: 'no-drag' }}
        >
          <VscChromeMinimize className="w-4 h-4" />
        </button>
        <button
          onClick={onMaximize}
          className="w-12 h-10 flex items-center justify-center titlebar-btn hover:bg-titlebar-hover transition-colors duration-200 text-titlebar-foreground"
          title="Maximize"
          style={{ WebkitAppRegion: 'no-drag' }}
        >
          <VscChromeMaximize className="w-4 h-4" />
        </button>
        <button
          onClick={onClose}
          className="w-12 h-10 flex items-center justify-center titlebar-btn hover:bg-titlebar-close-hover transition-colors duration-200 text-titlebar-foreground hover:text-white"
          title="Close"
          style={{ WebkitAppRegion: 'no-drag' }}
        >
          <VscChromeClose className="w-4 h-4" />
        </button>
        </div>
      </div>
    </div>
  );
}