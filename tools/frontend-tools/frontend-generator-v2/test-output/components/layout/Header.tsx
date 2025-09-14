import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

interface HeaderProps {
  title?: string;
  showUserMenu?: boolean;
}

const Header: React.FC<HeaderProps> = ({ 
  title = "Chess Training App",
  showUserMenu = true 
}) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="app-header">
      <div className="header-content">
        <div className="header-left">
          <h1 className="app-title">{title}</h1>
        </div>
        
        <div className="header-right">
          <button 
            onClick={toggleTheme}
            className="theme-toggle-button"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
          
          {showUserMenu && (
            <div className="user-menu">
              <button className="user-menu-button">
                👤 Profile
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;