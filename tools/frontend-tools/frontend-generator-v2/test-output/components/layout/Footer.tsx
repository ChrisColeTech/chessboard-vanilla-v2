import React from 'react';

interface FooterProps {
  showVersion?: boolean;
}

const Footer: React.FC<FooterProps> = ({ showVersion = true }) => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-left">
          <p>&copy; 2024 Chess Training App</p>
        </div>
        
        <div className="footer-center">
          <nav className="footer-nav">
            <a href="/privacy">Privacy</a>
            <a href="/terms">Terms</a>
            <a href="/help">Help</a>
          </nav>
        </div>
        
        <div className="footer-right">
          {showVersion && (
            <span className="version">v1.0.0</span>
          )}
        </div>
      </div>
    </footer>
  );
};

export default Footer;