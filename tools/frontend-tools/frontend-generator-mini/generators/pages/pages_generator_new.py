"""
Pages Generator - Refactored to use template engine and name standardizer
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from template_engine import TemplateEngine
from name_standardizer import NameStandardizer
from generators.base_generator import BaseGenerator


class PagesGenerator(BaseGenerator):
    """Generates React pages using template engine"""
    
    def __init__(self, output_path: Path):
        super().__init__(output_path)
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.template_engine = TemplateEngine(self.template_dir)
    
    def generate(self, endpoint_name: str, endpoint_config: dict, domain: str = 'other'):
        """Generate React pages from backend config using templates"""
        print(f"📄 Generating pages: {endpoint_name} (domain: {domain})")
        
        # Check for named template first
        named_template = self.template_dir / "named" / "pages" / f"{endpoint_name}.tsx.template"
        if named_template.exists():
            print(f"📝 Using named template: {endpoint_name}.tsx.template")
            self._generate_from_named_template(endpoint_name, endpoint_config, domain, named_template)
            return
        
        # Skip dynamic generation for endpoints with special routing (e.g., auth)
        if endpoint_config.get('special_routing', False):
            print(f"⏭️  Skipping dynamic page generation for {endpoint_name} (special routing)")
            return
        
        # Generate different page types
        entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
        methods = endpoint_config.get('methods', [])
        
        # Generate list page if we have list methods
        if any(method.startswith('list') or (method.startswith('get') and not method.endswith('ById')) for method in methods):
            self._generate_list_page(endpoint_name, entity_name, domain)
        
        # Generate detail page if we have getById methods
        if any(method.endswith('ById') for method in methods):
            self._generate_detail_page(endpoint_name, entity_name, domain)
        
        # Generate form page if we have create/update methods
        if any(method.startswith('create') or method.startswith('update') for method in methods):
            self._generate_form_page(endpoint_name, entity_name, domain)
    
    def _generate_list_page(self, endpoint_name: str, entity_name: str, domain: str):
        """Generate a list page for the entity"""
        # Prepare template variables
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'pascal_endpoint': NameStandardizer.to_pascal_case(endpoint_name),
            'kebab_endpoint': NameStandardizer.to_kebab_case(endpoint_name),
            'domain': domain,
            'page_type': 'List'
        }
        
        # Load and render template
        try:
            page_content = self.template_engine.render_template(
                'api/page.tsx.template',
                template_vars,
                is_static=False
            )
            
            # Write page file organized by domain
            output_dir = self.output_path / "pages" / domain
            page_name = f"{entity_name}Page"
            output_file = output_dir / f"{page_name}.tsx"
            
            self.write_file(output_file, page_content)
            
        except Exception as e:
            print(f"❌ Error generating list page {endpoint_name}: {e}")
            self._generate_fallback_list_page(endpoint_name, entity_name, domain)
    
    def _generate_detail_page(self, endpoint_name: str, entity_name: str, domain: str):
        """Generate a detail page for the entity"""
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'pascal_endpoint': NameStandardizer.to_pascal_case(endpoint_name),
            'kebab_endpoint': NameStandardizer.to_kebab_case(endpoint_name),
            'domain': domain,
            'page_type': 'Detail'
        }
        
        # For detail pages, we need a slightly different template
        # For now, use the same template but could be customized
        try:
            # Generate a detail page with different content
            detail_content = self._generate_detail_page_content(entity_name, endpoint_name, domain)
            
            output_dir = self.output_path / "pages" / domain
            page_name = f"{entity_name}DetailPage"
            output_file = output_dir / f"{page_name}.tsx"
            
            self.write_file(output_file, detail_content)
            
        except Exception as e:
            print(f"❌ Error generating detail page {endpoint_name}: {e}")
    
    def _generate_form_page(self, endpoint_name: str, entity_name: str, domain: str):
        """Generate a form page for creating/editing the entity"""
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'pascal_endpoint': NameStandardizer.to_pascal_case(endpoint_name),
            'kebab_endpoint': NameStandardizer.to_kebab_case(endpoint_name),
            'domain': domain,
            'page_type': 'Form'
        }
        
        try:
            # Generate a form page with different content
            form_content = self._generate_form_page_content(entity_name, endpoint_name, domain)
            
            output_dir = self.output_path / "pages" / domain
            page_name = f"{entity_name}FormPage"
            output_file = output_dir / f"{page_name}.tsx"
            
            self.write_file(output_file, form_content)
            
        except Exception as e:
            print(f"❌ Error generating form page {endpoint_name}: {e}")
    
    def _generate_detail_page_content(self, entity_name: str, endpoint_name: str, domain: str) -> str:
        """Generate detail page content"""
        entity_name_lower = entity_name.lower()
        camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
        
        return f"""import React, {{ useEffect }} from 'react';
import {{ useParams }} from 'react-router-dom';
import {{ use{entity_name} }} from '../../hooks/{domain}/use{entity_name}';

export const {entity_name}DetailPage = () => {{
  const {{ id }} = useParams<{{ id: string }}>();
  const {{ {entity_name_lower}, loading, error, get{entity_name}ById }} = use{entity_name}();

  useEffect(() => {{
    if (id) {{
      get{entity_name}ById(id);
    }}
  }}, [id, get{entity_name}ById]);

  if (loading) {{
    return <div className="loading">Loading {entity_name_lower}...</div>;
  }}

  if (error) {{
    return <div className="error">Error: {{error}}</div>;
  }}

  if (!{entity_name_lower}) {{
    return <div className="not-found">{entity_name} not found</div>;
  }}

  return (
    <div className="{NameStandardizer.to_kebab_case(endpoint_name)}-detail-page">
      <h1>{entity_name} Details</h1>
      <div className="{entity_name_lower}-details">
        <h2>{{id}}</h2>
        <pre>{{JSON.stringify({entity_name_lower}, null, 2)}}</pre>
      </div>
    </div>
  );
}};

export default {entity_name}DetailPage;"""
    
    def _generate_form_page_content(self, entity_name: str, endpoint_name: str, domain: str) -> str:
        """Generate form page content"""
        entity_name_lower = entity_name.lower()
        camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
        
        return f"""import React, {{ useState }} from 'react';
import {{ useNavigate }} from 'react-router-dom';
import {{ use{entity_name} }} from '../../hooks/{domain}/use{entity_name}';

export const {entity_name}FormPage = () => {{
  const navigate = useNavigate();
  const {{ loading, error, create{entity_name} }} = use{entity_name}();
  const [formData, setFormData] = useState({{}});

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    try {{
      await create{entity_name}(formData);
      navigate('/{NameStandardizer.to_kebab_case(endpoint_name)}');
    }} catch (err) {{
      console.error('Failed to create {entity_name_lower}:', err);
    }}
  }};

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {{
    setFormData(prev => ({{
      ...prev,
      [e.target.name]: e.target.value
    }}));
  }};

  return (
    <div className="{NameStandardizer.to_kebab_case(endpoint_name)}-form-page">
      <h1>Create {entity_name}</h1>
      
      {{error && <div className="error">Error: {{error}}</div>}}
      
      <form onSubmit={{handleSubmit}} className="{entity_name_lower}-form">
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={{formData.name || ''}}
            onChange={{handleChange}}
            required
          />
        </div>
        
        <div className="form-actions">
          <button type="submit" disabled={{loading}}>
            {{loading ? 'Creating...' : 'Create {entity_name}'}}
          </button>
          <button type="button" onClick={{() => navigate('/{NameStandardizer.to_kebab_case(endpoint_name)})}}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}};

export default {entity_name}FormPage;"""
    
    def _generate_fallback_list_page(self, endpoint_name: str, entity_name: str, domain: str):
        """Fallback to original hardcoded generation"""
        entity_name_lower = entity_name.lower()
        
        content = f"""import React from 'react';
import {{ use{entity_name} }} from '../../hooks/{domain}/use{entity_name}';

export const {entity_name}Page = () => {{
  const {{ {entity_name_lower}s, loading, error }} = use{entity_name}();

  if (loading) {{
    return <div className="loading">Loading {entity_name_lower}s...</div>;
  }}

  if (error) {{
    return <div className="error">Error: {{error}}</div>;
  }}

  return (
    <div className="{NameStandardizer.to_kebab_case(endpoint_name)}-page">
      <h1>{entity_name} Management</h1>
      <div className="{entity_name_lower}-list">
        {{({entity_name_lower}s || []).map((item) => (
          <div key={{item.id}} className="{entity_name_lower}-item">
            <h3>{{item.id}}</h3>
          </div>
        ))}}
      </div>
    </div>
  );
}};

export default {entity_name}Page;"""
        
        # Write file
        output_dir = self.output_path / "pages" / domain
        page_name = f"{entity_name}Page"
        output_file = output_dir / f"{page_name}.tsx"
        self.write_file(output_file, content)
    
    def _generate_from_named_template(self, endpoint_name: str, endpoint_config: dict, domain: str, template_path: Path):
        """Generate page from a named template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Write to the domain-specific pages directory
            output_dir = self.output_path / "pages" / domain
            entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
            page_name = f"{entity_name}Page"
            output_file = output_dir / f"{page_name}.tsx"
            
            self.write_file(output_file, template_content)
            
        except Exception as e:
            print(f"❌ Error generating from named template: {e}")