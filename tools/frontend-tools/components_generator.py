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
        
        return f"""import React, {{ useEffect }} from 'react';
import {{ use{domain_capitalized}Queries }} from '../../hooks/{domain}';

interface {entity}ComponentProps {{
  className?: string;
}}

export const {entity}Component: React.FC<{entity}ComponentProps> = ({{
  className
}}) => {{
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
        main_content = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
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
        
        main_components_index = chr(10).join(exports) + chr(10)
        
        components_index_file = src_path / "components" / "index.ts"
        self.write_file(components_index_file, main_components_index)