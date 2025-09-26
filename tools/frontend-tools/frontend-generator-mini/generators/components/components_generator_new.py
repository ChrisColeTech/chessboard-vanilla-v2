"""
Components Generator - Refactored to use template engine and name standardizer
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


class ComponentsGenerator(BaseGenerator):
    """Generates React components using template engine"""
    
    def __init__(self, output_path: Path):
        super().__init__(output_path)
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.template_engine = TemplateEngine(self.template_dir)
    
    def generate(self, endpoint_name: str, endpoint_config: dict, domain: str = 'other'):
        """Generate React components from backend config using templates"""
        print(f"🧩 Generating components: {endpoint_name} (domain: {domain})")
        
        # Skip dynamic generation for endpoints with special routing (e.g., auth)
        if endpoint_config.get('special_routing', False):
            print(f"⏭️  Skipping dynamic component generation for {endpoint_name} (special routing)")
            return
        
        entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
        properties = endpoint_config.get('properties', {})
        methods = endpoint_config.get('methods', [])
        
        # Generate different component types based on available methods
        if any(method.startswith('list') or (method.startswith('get') and not method.endswith('ById')) for method in methods):
            self._generate_list_component(endpoint_name, entity_name, domain, properties)
        
        if any(method.endswith('ById') for method in methods):
            self._generate_detail_component(endpoint_name, entity_name, domain, properties)
        
        if any(method.startswith('create') or method.startswith('update') for method in methods):
            self._generate_form_component(endpoint_name, entity_name, domain, properties)
    
    def _generate_list_component(self, endpoint_name: str, entity_name: str, domain: str, properties: Dict[str, str]):
        """Generate a list component for the entity"""
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'pascal_endpoint': NameStandardizer.to_pascal_case(endpoint_name),
            'kebab_endpoint': NameStandardizer.to_kebab_case(endpoint_name),
            'domain': domain,
            'properties': self._format_properties_for_display(properties),
            'component_type': 'List'
        }
        
        try:
            # Generate list component content
            component_content = self._generate_list_component_content(template_vars)
            
            # Write component file organized by domain
            output_dir = self.output_path / "components" / domain
            component_name = f"{entity_name}List"
            output_file = output_dir / f"{component_name}.tsx"
            
            self.write_file(output_file, component_content)
            
        except Exception as e:
            print(f"❌ Error generating list component {endpoint_name}: {e}")
    
    def _generate_detail_component(self, endpoint_name: str, entity_name: str, domain: str, properties: Dict[str, str]):
        """Generate a detail component for the entity"""
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'pascal_endpoint': NameStandardizer.to_pascal_case(endpoint_name),
            'kebab_endpoint': NameStandardizer.to_kebab_case(endpoint_name),
            'domain': domain,
            'properties': self._format_properties_for_display(properties),
            'component_type': 'Detail'
        }
        
        try:
            # Generate detail component content
            component_content = self._generate_detail_component_content(template_vars)
            
            # Write component file organized by domain
            output_dir = self.output_path / "components" / domain
            component_name = f"{entity_name}Detail"
            output_file = output_dir / f"{component_name}.tsx"
            
            self.write_file(output_file, component_content)
            
        except Exception as e:
            print(f"❌ Error generating detail component {endpoint_name}: {e}")
    
    def _generate_form_component(self, endpoint_name: str, entity_name: str, domain: str, properties: Dict[str, str]):
        """Generate a form component for the entity"""
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'pascal_endpoint': NameStandardizer.to_pascal_case(endpoint_name),
            'kebab_endpoint': NameStandardizer.to_kebab_case(endpoint_name),
            'domain': domain,
            'form_fields': self._generate_form_fields(properties),
            'component_type': 'Form'
        }
        
        try:
            # Generate form component content
            component_content = self._generate_form_component_content(template_vars)
            
            # Write component file organized by domain
            output_dir = self.output_path / "components" / domain
            component_name = f"{entity_name}Form"
            output_file = output_dir / f"{component_name}.tsx"
            
            self.write_file(output_file, component_content)
            
        except Exception as e:
            print(f"❌ Error generating form component {endpoint_name}: {e}")
    
    def _format_properties_for_display(self, properties: Dict[str, str]) -> str:
        """Format properties for display in components"""
        if not properties:
            return "        <p>No properties defined</p>"
        
        display_fields = []
        for prop_name, prop_type in properties.items():
            camel_prop = NameStandardizer.to_camel_case(prop_name)
            display_name = prop_name.replace('_', ' ').title()
            
            if prop_type in ['string', 'text']:
                display_fields.append(f"        <div><strong>{display_name}:</strong> {{item.{camel_prop}}}</div>")
            elif prop_type in ['number', 'integer', 'float']:
                display_fields.append(f"        <div><strong>{display_name}:</strong> {{item.{camel_prop}}}</div>")
            elif prop_type == 'boolean':
                display_fields.append(f"        <div><strong>{display_name}:</strong> {{item.{camel_prop} ? 'Yes' : 'No'}}</div>")
            elif prop_type in ['datetime', 'date']:
                display_fields.append(f"        <div><strong>{display_name}:</strong> {{new Date(item.{camel_prop}).toLocaleDateString()}}</div>")
            else:
                display_fields.append(f"        <div><strong>{display_name}:</strong> {{String(item.{camel_prop})}}</div>")
        
        return "\n".join(display_fields)
    
    def _generate_form_fields(self, properties: Dict[str, str]) -> str:
        """Generate form fields based on properties"""
        if not properties:
            return "        {/* No properties defined for form fields */}"
        
        form_fields = []
        for prop_name, prop_type in properties.items():
            camel_prop = NameStandardizer.to_camel_case(prop_name)
            display_name = prop_name.replace('_', ' ').title()
            
            if prop_name in ['id', 'created_at', 'updated_at']:
                continue  # Skip auto-generated fields
            
            if prop_type in ['string', 'text']:
                if 'email' in prop_name.lower():
                    input_type = 'email'
                elif 'password' in prop_name.lower():
                    input_type = 'password'
                else:
                    input_type = 'text'
                
                form_fields.append(f"""        <div className="form-group">
          <label htmlFor="{camel_prop}">{display_name}:</label>
          <input
            type="{input_type}"
            id="{camel_prop}"
            name="{camel_prop}"
            value={{formData.{camel_prop} || ''}}
            onChange={{handleChange}}
            required
          />
        </div>""")
            
            elif prop_type in ['number', 'integer', 'float']:
                form_fields.append(f"""        <div className="form-group">
          <label htmlFor="{camel_prop}">{display_name}:</label>
          <input
            type="number"
            id="{camel_prop}"
            name="{camel_prop}"
            value={{formData.{camel_prop} || ''}}
            onChange={{handleChange}}
            required
          />
        </div>""")
            
            elif prop_type == 'boolean':
                form_fields.append(f"""        <div className="form-group">
          <label htmlFor="{camel_prop}">
            <input
              type="checkbox"
              id="{camel_prop}"
              name="{camel_prop}"
              checked={{formData.{camel_prop} || false}}
              onChange={{(e) => setFormData(prev => ({{ ...prev, {camel_prop}: e.target.checked }}))}}
            />
            {display_name}
          </label>
        </div>""")
            
            elif prop_type in ['datetime', 'date']:
                input_type = 'datetime-local' if prop_type == 'datetime' else 'date'
                form_fields.append(f"""        <div className="form-group">
          <label htmlFor="{camel_prop}">{display_name}:</label>
          <input
            type="{input_type}"
            id="{camel_prop}"
            name="{camel_prop}"
            value={{formData.{camel_prop} || ''}}
            onChange={{handleChange}}
          />
        </div>""")
        
        return "\n\n".join(form_fields) if form_fields else "        {/* No editable fields */}"
    
    def _generate_list_component_content(self, vars: Dict[str, str]) -> str:
        """Generate list component content"""
        return f"""import React from 'react';
import type {{ {vars['entity_name']} }} from '../../types/{vars['domain']}/{vars['camel_endpoint']}';

interface {vars['entity_name']}ListProps {{
  items: {vars['entity_name']}[];
  loading?: boolean;
  onItemClick?: (item: {vars['entity_name']}) => void;
}}

export const {vars['entity_name']}List: React.FC<{vars['entity_name']}ListProps> = ({{
  items,
  loading = false,
  onItemClick
}}) => {{
  if (loading) {{
    return <div className="loading">Loading {vars['entity_name_lower']}s...</div>;
  }}

  if (!items || items.length === 0) {{
    return <div className="empty">No {vars['entity_name_lower']}s found</div>;
  }}

  return (
    <div className="{vars['kebab_endpoint']}-list">
      {{items.map((item) => (
        <div
          key={{item.id}}
          className="{vars['entity_name_lower']}-item"
          onClick={{() => onItemClick?.(item)}}
          style={{{{ cursor: onItemClick ? 'pointer' : 'default' }}}}
        >
{vars['properties']}
        </div>
      ))}}
    </div>
  );
}};

export default {vars['entity_name']}List;"""
    
    def _generate_detail_component_content(self, vars: Dict[str, str]) -> str:
        """Generate detail component content"""
        return f"""import React from 'react';
import type {{ {vars['entity_name']} }} from '../../types/{vars['domain']}/{vars['camel_endpoint']}';

interface {vars['entity_name']}DetailProps {{
  item: {vars['entity_name']};
  onEdit?: (item: {vars['entity_name']}) => void;
  onDelete?: (id: string) => void;
}}

export const {vars['entity_name']}Detail: React.FC<{vars['entity_name']}DetailProps> = ({{
  item,
  onEdit,
  onDelete
}}) => {{
  return (
    <div className="{vars['kebab_endpoint']}-detail">
      <div className="{vars['entity_name_lower']}-info">
{vars['properties']}
      </div>
      
      <div className="actions">
        {{onEdit && (
          <button onClick={{() => onEdit(item)}} className="btn-edit">
            Edit
          </button>
        )}}
        {{onDelete && (
          <button 
            onClick={{() => onDelete(item.id)}} 
            className="btn-delete"
            onClick={{(e) => {{
              e.preventDefault();
              if (window.confirm('Are you sure you want to delete this {vars['entity_name_lower']}?')) {{
                onDelete(item.id);
              }}
            }}}}
          >
            Delete
          </button>
        )}}
      </div>
    </div>
  );
}};

export default {vars['entity_name']}Detail;"""
    
    def _generate_form_component_content(self, vars: Dict[str, str]) -> str:
        """Generate form component content"""
        return f"""import React, {{ useState }} from 'react';
import type {{ {vars['entity_name']} }} from '../../types/{vars['domain']}/{vars['camel_endpoint']}';

interface {vars['entity_name']}FormProps {{
  initialData?: Partial<{vars['entity_name']}>;
  onSubmit: (data: Partial<{vars['entity_name']}>) => void;
  onCancel?: () => void;
  loading?: boolean;
}}

export const {vars['entity_name']}Form: React.FC<{vars['entity_name']}FormProps> = ({{
  initialData = {{}},
  onSubmit,
  onCancel,
  loading = false
}}) => {{
  const [formData, setFormData] = useState<Partial<{vars['entity_name']}>>((initialData));

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {{
    const {{ name, value, type, checked }} = e.target;
    setFormData(prev => ({{
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }}));
  }};

  const handleSubmit = (e: React.FormEvent) => {{
    e.preventDefault();
    onSubmit(formData);
  }};

  return (
    <form onSubmit={{handleSubmit}} className="{vars['kebab_endpoint']}-form">
{vars['form_fields']}
      
      <div className="form-actions">
        <button type="submit" disabled={{loading}} className="btn-primary">
          {{loading ? 'Saving...' : 'Save'}}
        </button>
        {{onCancel && (
          <button type="button" onClick={{onCancel}} className="btn-secondary">
            Cancel
          </button>
        )}}
      </div>
    </form>
  );
}};

export default {vars['entity_name']}Form;"""
    
    def generate_all_components(self):
        """Generate all component categories from static templates"""
        print("🧩 Generating static components from templates...")
        
        # This method can handle static template copying if needed
        # For now, focus on dynamic component generation from backend config
        pass