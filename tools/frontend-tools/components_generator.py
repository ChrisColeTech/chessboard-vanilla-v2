#!/usr/bin/env python3
"""
Components Generator Module
Handles generation of React components for all domains
"""

from typing import List
from base_generator import BaseFrontendGenerator

class ComponentsGenerator(BaseFrontendGenerator):
    """Generates React components for all domains"""
    
    def generate_domain_components(self, domain: str, endpoints: List[str]):
        """Generate placeholder components for a domain"""
        src_path = self.get_src_path()
        components_path = src_path / "components" / domain
        
        domain_components = []
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = self.get_entity_name(endpoint_name)
            
            if entity:
                component_content = self._generate_component_content(domain, entity)
                component_file = components_path / f"{entity}Component.tsx"
                self.write_file(component_file, component_content)
                domain_components.append(entity)
        
        # Generate domain component index
        if domain_components:
            self._generate_components_index(components_path, domain_components)
    
    def _generate_component_content(self, domain: str, entity: str) -> str:
        """Generate component content for an entity"""
        domain_capitalized = self.capitalize_domain(domain)
        
        return f"""import {{ useEffect }} from 'react';
import {{ use{domain_capitalized}Queries }} from '../../hooks/{domain}';

interface {entity}ComponentProps {{
  className?: string;
}}

export const {entity}Component = ({{
  className
}}: {entity}ComponentProps) => {{
  const {{ data, loading, error, refetch }} = use{domain_capitalized}Queries();
  
  // Load data on component mount
  useEffect(() => {{
    refetch();
  }}, []);
  
  const renderTable = () => {{
    if (!data?.data || !Array.isArray(data.data)) {{
      return <p>No data available</p>;
    }}
    
    const items = data.data;
    if (items.length === 0) {{
      return <p>No {entity.lower()} records found</p>;
    }}
    
    // Get column headers from the first item
    const columns = Object.keys(items[0]);
    
    return (
      <table style={{{{ width: '100%', borderCollapse: 'collapse', marginTop: '16px' }}}}>
        <thead>
          <tr>
            {{columns.map((col: string) => (
              <th key={{col}} style={{{{ 
                border: '1px solid #ddd', 
                padding: '8px', 
                backgroundColor: '#f5f5f5',
                textAlign: 'left'
              }}}}>
                {{col.charAt(0).toUpperCase() + col.slice(1).replace(/_/g, ' ')}}
              </th>
            ))}}
          </tr>
        </thead>
        <tbody>
          {{items.map((item: any, index: number) => (
            <tr key={{item.id || index}}>
              {{columns.map((col: string) => (
                <td key={{col}} style={{{{ 
                  border: '1px solid #ddd', 
                  padding: '8px'
                }}}}>
                  {{typeof item[col] === 'object' ? JSON.stringify(item[col]) : String(item[col] ?? '')}}
                </td>
              ))}}
            </tr>
          ))}}
        </tbody>
      </table>
    );
  }};
  
  return (
    <div className={{`{entity.lower()}-component ${{className || ''}}`}} style={{{{ padding: '16px' }}}}>
      <div style={{{{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}}}>
        <h2>{entity} Data</h2>
        <button 
          onClick={{() => refetch()}}
          disabled={{loading}}
          style={{{{
            padding: '8px 16px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'default' : 'pointer'
          }}}}
        >
          {{loading ? 'Loading...' : 'Refresh'}}
        </button>
      </div>
      
      {{error && (
        <div style={{{{
          color: 'red', 
          backgroundColor: '#ffebee', 
          padding: '12px', 
          borderRadius: '4px', 
          marginBottom: '16px'
        }}}}>
          <strong>Error:</strong> {{error}}
        </div>
      )}}
      
      {{loading && !data && (
        <div style={{{{ textAlign: 'center', padding: '40px' }}}}>
          <p>Loading {entity.lower()} data...</p>
        </div>
      )}}
      
      {{!loading && renderTable()}}
    </div>
  );
}};
"""
    
    def _generate_components_index(self, components_path, domain_components: List[str]):
        """Generate domain component index"""
        domain_index = "\n".join([
            f"export {{ {comp}Component }} from './{comp}Component';" 
            for comp in domain_components
        ])
        
        domain_index_file = components_path / "index.ts"
        self.write_file(domain_index_file, domain_index)
    
    def generate_main_entry_files(self):
        """Generate main React entry files"""
        src_path = self.get_src_path()
        
        # Generate main.tsx
        main_content = """import { StrictMode } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)"""
        
        main_file = src_path / "main.tsx"
        self.write_file(main_file, main_content)
        
        # Generate App.tsx dynamically
        from domain_mapping import DomainMapping
        domain_mapping_obj = DomainMapping()
        domains = domain_mapping_obj.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        # Generate imports for all domain components using actual entity names
        imports = []
        sections = []
        for domain in sorted(domains.keys()):
            # Get the actual component names for this domain
            domain_endpoints = domains[domain]
            domain_components = []
            
            for endpoint_name in domain_endpoints:
                if endpoint_name in self.backend_config['endpoints']:
                    endpoint_config = self.backend_config['endpoints'][endpoint_name]
                    entity = self.get_entity_name(endpoint_name)
                    if entity:
                        component_name = f"{entity}Component"
                        if component_name not in [comp[0] for comp in domain_components]:
                            domain_components.append((component_name, entity))
            
            # Generate imports and sections for this domain
            if domain_components:
                domain_imports = []
                domain_elements = []
                for component_name, entity in domain_components:
                    domain_imports.append(component_name)
                    domain_elements.append(f"<{component_name} />")
                
                imports.append(f"import {{ {', '.join(domain_imports)} }} from './components/{domain}'")
                sections.append(f"""        <div className="domain-section">
          <h2>{self.capitalize_domain(domain)} Domain</h2>
          {chr(10).join([f'          {elem}' for elem in domain_elements])}
        </div>""")
        
        app_content = f"""import './App.css'
import {{ useState, useEffect }} from 'react';
import {{ AuthAPIClient }} from './clients/AuthAPIClient';

// Import our generated components
{chr(10).join(imports)}

function App() {{
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<any>(null);
  const authClient = new AuthAPIClient();

  // Check if user is already logged in on app start
  useEffect(() => {{
    const token = localStorage.getItem('auth_token');
    if (token) {{
      setIsLoggedIn(true);
      // Optionally fetch user info
      authClient.getCurrentUser().then(response => {{
        if (response.success) {{
          setUser(response.data);
        }}
      }}).catch(() => {{
        // Token might be invalid, clear it
        localStorage.removeItem('auth_token');
        setIsLoggedIn(false);
      }});
    }}
  }}, []);

  const handleLogin = async () => {{
    setLoading(true);
    try {{
      // Login with demo credentials - try admin first, then test user
      let response;
      try {{
        response = await authClient.login({{
          email: 'admin@admin.com',
          password: 'admin'
        }});
      }} catch (err) {{
        // Fallback to test user
        response = await authClient.login({{
          email: 'test3@example.com',
          password: 'password123'
        }});
      }}
      
      if (response.success && response.data?.token) {{
        localStorage.setItem('auth_token', response.data.token);
        setIsLoggedIn(true);
        setUser(response.data.user);
        console.log('Login successful:', response.data);
      }} else {{
        console.error('Login failed:', response);
        alert('Login failed. Please check your credentials.');
      }}
    }} catch (error: any) {{
      console.error('Login error:', error);
      alert('Login error: ' + error.message);
    }} finally {{
      setLoading(false);
    }}
  }};

  const handleLogout = () => {{
    localStorage.removeItem('auth_token');
    setIsLoggedIn(false);
    setUser(null);
  }};

  if (!isLoggedIn) {{
    return (
      <div className="App">
        <header className="App-header">
          <h1>Chess Platform - Login Required</h1>
          <p>Please log in to access the application</p>
          <div style={{{{ marginTop: '2rem' }}}}>
            <button 
              onClick={{handleLogin}}
              disabled={{loading}}
              style={{{{
                padding: '12px 24px',
                fontSize: '16px',
                backgroundColor: loading ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'default' : 'pointer'
              }}}}
            >
              {{loading ? 'Logging in...' : 'Login with Demo Account'}}
            </button>
            <p style={{{{ fontSize: '14px', color: '#666', marginTop: '1rem' }}}}>
              Demo credentials: admin@admin.com / admin (or test3@example.com / password123)
            </p>
          </div>
        </header>
      </div>
    );
  }}

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chess Platform - Domain-Driven Frontend</h1>
        <p>Generated frontend with complete API contract coverage</p>
        <div style={{{{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}}}>
          <span>Welcome{{user ? `, ${{user.name || user.email}}` : ''}}!</span>
          <button 
            onClick={{handleLogout}}
            style={{{{
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}}}
          >
            Logout
          </button>
        </div>
      </header>
      
      <main className="App-main">
{chr(10).join(sections)}
      </main>
    </div>
  )
}}

export default App"""
        
        app_file = src_path / "App.tsx" 
        self.write_file(app_file, app_content)
        
        # Generate CSS files
        self._generate_css_files(src_path)
    
    def _generate_css_files(self, src_path):
        """Generate CSS files for the application"""
        app_css = """.App {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.App-header {
  margin-bottom: 2rem;
}

.App-header h1 {
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.App-header p {
  color: #666;
  font-size: 1.1rem;
}

.App-main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.domain-section {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: #f9f9f9;
}

.domain-section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

button {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

button:hover {
  background: #2980b9;
}"""
        
        app_css_file = src_path / "App.css"
        self.write_file(app_css_file, app_css)
        
        index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}"""
        
        index_css_file = src_path / "index.css"
        self.write_file(index_css_file, index_css)
    
    def generate_ui_components(self):
        """Generate UI components like DataTable"""
        src_path = self.get_src_path()
        ui_components_path = src_path / "components" / "ui"
        ui_components_path.mkdir(parents=True, exist_ok=True)
        
        # Generate DataTable component
        data_table_content = '''
interface Column {
  key: string;
  header: string;
  render?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
  data: any[];
  columns?: Column[];
  loading?: boolean;
  error?: string | null;
  className?: string;
}

export const DataTable: React.FC<DataTableProps> = ({
  data = [],
  columns = [],
  loading = false,
  error = null,
  className = ""
}) => {
  // Auto-generate columns if not provided
  const finalColumns = columns.length > 0 ? columns : generateColumnsFromData(data);

  if (loading) {
    return (
      <div className={`w-full h-full flex items-center justify-center ${className}`}>
        <div className="text-muted-foreground">Loading data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`w-full h-full flex items-center justify-center ${className}`}>
        <div className="text-red-500 text-center">
          <div className="font-semibold">Error loading data</div>
          <div className="text-sm mt-1">{error}</div>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className={`w-full h-full flex items-center justify-center ${className}`}>
        <div className="text-muted-foreground">No data available</div>
      </div>
    );
  }

  return (
    <div className={`w-full h-full overflow-auto ${className}`}>
      <div className="min-w-full">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-border bg-card/50">
              {finalColumns.map((column) => (
                <th
                  key={column.key}
                  className="text-left p-3 font-semibold text-sm text-foreground"
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr
                key={index}
                className="border-b border-border/50 hover:bg-card/30 transition-colors"
              >
                {finalColumns.map((column) => (
                  <td key={column.key} className="p-3 text-sm text-muted-foreground">
                    {column.render
                      ? column.render(row[column.key], row)
                      : formatValue(row[column.key])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Helper function to auto-generate columns from data
function generateColumnsFromData(data: any[]): Column[] {
  if (data.length === 0) return [];

  const firstRow = data[0];
  const keys = Object.keys(firstRow);

  return keys.slice(0, 6).map((key) => ({
    key,
    header: key.charAt(0).toUpperCase() + key.slice(1).replace(/[_-]/g, ' ')
  }));
}

// Helper function to format values for display
function formatValue(value: any): string {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (typeof value === 'object') return JSON.stringify(value);
  if (typeof value === 'string' && value.length > 50) {
    return value.substring(0, 50) + '...';
  }
  return String(value);
}'''
        
        data_table_file = ui_components_path / "DataTable.tsx"
        self.write_file(data_table_file, data_table_content)
        
        # Generate Button component
        button_content = '''import type { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "destructive" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  disabled,
  className = "",
  ...props
}) => {
  const baseClasses = "inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none";
  
  const variantClasses = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500",
    destructive: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
    ghost: "text-gray-700 hover:bg-gray-100 focus:ring-gray-500"
  };
  
  const sizeClasses = {
    sm: "px-3 py-1.5 text-sm rounded",
    md: "px-4 py-2 text-base rounded-md",
    lg: "px-6 py-3 text-lg rounded-lg"
  };
  
  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;
  
  return (
    <button
      className={classes}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <>
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};'''
        
        button_file = ui_components_path / "button.tsx"
        self.write_file(button_file, button_content)
        
        # Generate UI components index
        ui_index_content = '''export { DataTable } from "./DataTable";
export { Button } from "./button";
'''
        ui_index_file = ui_components_path / "index.ts"
        self.write_file(ui_index_file, ui_index_content)
        
        print("  📝 Generated UI components (DataTable, Button)")

    def generate_main_components_index(self):
        """Generate main components index file dynamically"""
        src_path = self.get_src_path()
        
        # Group endpoints by domain to get all domains
        from domain_mapping import DomainMapping
        domain_mapping_obj = DomainMapping()
        domains = domain_mapping_obj.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        # Generate exports for all domains
        exports = []
        for domain in domains.keys():
            exports.append(f"export * from './{domain}';")
        
        # Add UI components export
        exports.append("export * from './ui';")
        
        main_components_index = chr(10).join(exports) + chr(10)
        
        components_index_file = src_path / "components" / "index.ts"
        self.write_file(components_index_file, main_components_index)

    def generate_chess_components(self):
        """Generate chess layout components"""
        src_path = self.get_src_path()
        chess_components_path = src_path / "components" / "chess"
        chess_components_path.mkdir(parents=True, exist_ok=True)
        
        # Generate ChessboardLayout component
        chessboard_layout_content = '''
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
        minHeight: '100%'
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
}'''
        
        chessboard_file = chess_components_path / "ChessboardLayout.tsx"
        self.write_file(chessboard_file, chessboard_layout_content)

        # Generate MobileChessboardLayout component  
        mobile_chessboard_content = '''
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
}'''
        
        mobile_chessboard_file = chess_components_path / "MobileChessboardLayout.tsx"
        self.write_file(mobile_chessboard_file, mobile_chessboard_content)
        
        # Generate chess components index
        chess_index_content = '''export { ChessboardLayout } from "./ChessboardLayout";
export { MobileChessboardLayout } from "./MobileChessboardLayout";
'''
        chess_index_file = chess_components_path / "index.ts"
        self.write_file(chess_index_file, chess_index_content)
        
        print("  📝 Generated chess layout components")