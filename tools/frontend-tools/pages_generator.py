#!/usr/bin/env python3
"""
Pages Generator
Generates React pages based on backend endpoints, grouped by domain
"""

from pathlib import Path
from typing import Dict, List
from base_generator import BaseFrontendGenerator

class PagesGenerator(BaseFrontendGenerator):
    """Generates React pages based on backend config endpoints"""
    
    def __init__(self, frontend_path: str = "../frontend-v2"):
        super().__init__(frontend_path)
        
        # Page domain mapper - groups related endpoints into logical page domains
        self.page_domain_mapping = {
            # Chess gameplay and learning
            'chess': ['puzzles', 'games', 'openings', 'endgames', 'analysis', 'historic-games'],
            
            # User management and authentication  
            'user': ['auth', 'sessions', 'users', 'profiles'],
            
            # Learning and education
            'learning': ['tutorials', 'learning', 'learning-modules', 'tutorial-steps', 'study-plans'],
            
            # Progress and achievements
            'progress': ['stats', 'progress', 'achievements', 'analytics', 'puzzle-attempts'],
            
            # Support and business
            'support': ['help', 'subscriptions', 'puzzle-sources', 'game-reviews']
        }
    
    def group_endpoints_by_page_domain(self, endpoints: List[str]) -> Dict[str, List[str]]:
        """Group endpoints into logical page domains"""
        page_domains = {}
        
        # Initialize page domains
        for domain in self.page_domain_mapping.keys():
            page_domains[domain] = []
        
        # Group endpoints by page domain
        for endpoint in endpoints:
            endpoint_assigned = False
            for page_domain, mapped_endpoints in self.page_domain_mapping.items():
                if endpoint in mapped_endpoints:
                    page_domains[page_domain].append(endpoint)
                    endpoint_assigned = True
                    break
            
            # If endpoint not mapped, create a separate domain for it
            if not endpoint_assigned:
                if 'other' not in page_domains:
                    page_domains['other'] = []
                page_domains['other'].append(endpoint)
        
        # Remove empty domains
        return {k: v for k, v in page_domains.items() if v}
    
    def get_parent_page_template(self, domain: str, endpoints: List[str]) -> str:
        """Generate parent page template following UITestPage pattern"""
        component_name = f"{domain.title()}Page"
        main_component = f"{domain.title()}MainPage"
        
        # Generate wrapper imports
        wrapper_imports = []
        child_conditionals = []
        
        for endpoint in endpoints:
            page_name = endpoint.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
            
            # Fix naming conflicts: if endpoint name matches domain, add "Feature" suffix
            if page_name.lower() == domain.lower():
                page_name = f"{page_name}Feature"
                
            wrapper_name = f"{page_name}PageWrapper"
            wrapper_imports.append(f'import {{ {wrapper_name} }} from "../../components/{domain}/{wrapper_name}";')
            child_conditionals.append(f'  if (currentChildPage === "{endpoint}") {{\n    CurrentPageComponent = {wrapper_name};\n  }}')
        
        wrapper_imports_str = '\n'.join(wrapper_imports)
        child_conditionals_str = ' else '.join(child_conditionals)
        
        return f'''import React from "react";
import {{ useAppStore }} from "../../stores/appStore";
import {{ {main_component} }} from "./{main_component}";
{wrapper_imports_str}

export const {component_name}: React.FC = () => {{
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = {main_component};

  {child_conditionals_str}

  return (
    <div className="relative h-full">
      {{/* Current page content */}}
      <CurrentPageComponent />
    </div>
  );
}};
'''

    def get_main_page_template(self, domain: str, endpoints: List[str]) -> str:
        """Generate main page template styled after LayoutTestPage"""
        component_name = f"{domain.title()}MainPage"
        hook_name = domain.lower()
        endpoints_list = ", ".join(endpoints)
        
        return f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";

export const {component_name}: React.FC = () => {{
  usePageInstructions("{hook_name}");

  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            {domain.title()}
          </h1>
          <p className="text-muted-foreground">
            Welcome to the {domain.lower()} hub. This page groups related functionality 
            and follows the domain-driven architecture.
          </p>
          <div className="mt-6 p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm mb-2">Page Domain: {domain.title()}</h3>
            <p className="text-xs text-muted-foreground">
              Endpoints: {endpoints_list}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
            <div className="p-4 bg-card border border-border rounded-lg">
              <h4 className="font-semibold text-sm">Related Features</h4>
              <div className="text-xs text-muted-foreground mt-1 space-y-1">
                {' '.join([f'<div>• {endpoint.replace("-", " ").title()}</div>' for endpoint in endpoints])}
              </div>
            </div>
            <div className="p-4 bg-card border border-border rounded-lg">
              <h4 className="font-semibold text-sm">Actions</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Use the action menu to navigate between specific features
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}};
'''
    
    def get_individual_page_template(self, endpoint_name: str, domain: str, page_name: str = None) -> tuple:
        """Generate templates for both desktop and mobile individual endpoint pages"""
        if page_name is None:
            page_name = endpoint_name.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
            
        component_name = f"{page_name}Page"
        mobile_component_name = f"Mobile{page_name}Page"
        hook_name = endpoint_name.lower().replace('-', '').replace('_', '')
        
        # Desktop template
        desktop_template = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";

export const {component_name}: React.FC = () => {{
  usePageInstructions("{hook_name}");

  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            {page_name}
          </h1>
          <p className="text-muted-foreground">
            Welcome to the {page_name.lower()} page. This page handles {endpoint_name} operations
            and belongs to the {domain} domain group.
          </p>
          <div className="mt-6 p-4 bg-card border border-border rounded-lg">
            <h3 className="font-semibold text-sm mb-2">Endpoint: {endpoint_name}</h3>
            <p className="text-xs text-muted-foreground">
              Domain Group: {domain.title()} | Desktop Feature Page
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
            <div className="p-4 bg-card border border-border rounded-lg">
              <h4 className="font-semibold text-sm">Desktop Features</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Full {endpoint_name.replace('-', ' ').title()} functionality with enhanced desktop interface
              </p>
            </div>
            <div className="p-4 bg-card border border-border rounded-lg">
              <h4 className="font-semibold text-sm">Actions</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Use the action sheet to navigate between features
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}};
'''

        # Mobile template
        mobile_template = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";

export const {mobile_component_name}: React.FC = () => {{
  usePageInstructions("{hook_name}");

  return (
    <section className="space-y-3 p-4">
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="text-center space-y-3">
          <h1 className="text-2xl font-bold text-gray-900">
            {page_name}
          </h1>
          <p className="text-gray-600 text-sm">
            Mobile {page_name.lower()} page for {endpoint_name} operations
          </p>
          <div className="mt-4 p-3 bg-gray-50 border border-gray-200 rounded-lg">
            <h3 className="font-medium text-xs mb-1">Endpoint: {endpoint_name}</h3>
            <p className="text-xs text-gray-500">
              Domain: {domain.title()} | Mobile Optimized
            </p>
          </div>
          <div className="space-y-3 mt-4">
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="font-medium text-xs">Mobile Features</h4>
              <p className="text-xs text-gray-500 mt-1">
                Touch-optimized {endpoint_name.replace('-', ' ').title()} interface
              </p>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="font-medium text-xs">Quick Actions</h4>
              <p className="text-xs text-gray-500 mt-1">
                Tap the action button for feature navigation
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}};
'''
        
        return desktop_template, mobile_template

    def get_page_wrapper_template(self, endpoint_name: str, domain: str, page_name: str = None) -> str:
        """Generate page wrapper template with mobile variant support"""
        if page_name is None:
            page_name = endpoint_name.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
        
        wrapper_name = f"{page_name}PageWrapper"
        mobile_wrapper_name = f"Mobile{page_name}PageWrapper"
        page_component = f"{page_name}Page"
        mobile_page_component = f"Mobile{page_name}Page"
        
        # Generate desktop wrapper
        desktop_wrapper = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ {page_component} }} from "../../pages/{domain}/{page_component}";

export const {wrapper_name}: React.FC = () => {{
  usePageInstructions("{endpoint_name}");
  
  return <{page_component} />;
}};
'''

        # Generate mobile wrapper  
        mobile_wrapper = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ {mobile_page_component} }} from "../../pages/{domain}/{mobile_page_component}";

export const {mobile_wrapper_name}: React.FC = () => {{
  usePageInstructions("{endpoint_name}");
  
  return <{mobile_page_component} />;
}};
'''
        
        return desktop_wrapper, mobile_wrapper

    def get_domain_actions_hook_template(self, domain: str, endpoints: List[str]) -> str:
        """Generate domain actions hook template"""
        hook_name = f"use{domain.title()}Actions"
        
        # Generate action functions for each endpoint
        action_functions = []
        return_items = []
        for endpoint in endpoints:
            page_name = endpoint.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
            
            # Fix naming conflicts: if endpoint name matches domain, add "Feature" suffix
            if page_name.lower() == domain.lower():
                page_name = f"{page_name}Feature"
                
            action_name = f"goTo{page_name}"
            action_functions.append(f'''  const {action_name} = useCallback(() => {{
    setCurrentChildPage('{endpoint}');
    playMove(false);
  }}, [setCurrentChildPage, playMove]);''')
            
            return_items.append(action_name)
        
        # Generate return object
        return_object = ',\n    '.join(return_items)
        
        action_functions_str = '\n\n'.join(action_functions)
        
        return f'''import {{ useCallback }} from "react";
import {{ useAppStore }} from "../../stores/appStore";
import {{ useUIClickSoundOptimized }} from "../audio/useUIClickSoundOptimized";

export const {hook_name} = () => {{
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const {{ playMove }} = useUIClickSoundOptimized();

{action_functions_str}

  const backToMain = useCallback(() => {{
    setCurrentChildPage(null);
  }}, [setCurrentChildPage]);

  return {{
    {return_object},
    backToMain
  }};
}};
'''

    def generate_domain_pages(self, domain: str, endpoints: List[str]):
        """Generate parent page, main page, individual pages, wrappers, and action hooks"""
        domain_dir = self.get_src_path() / "pages" / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        components_dir = self.get_src_path() / "components" / domain
        components_dir.mkdir(parents=True, exist_ok=True)
        
        hooks_dir = self.get_src_path() / "hooks" / domain
        hooks_dir.mkdir(parents=True, exist_ok=True)
        
        generated_pages = []
        
        # 1. Generate parent page (router like UITestPage)
        parent_component_name = f"{domain.title()}Page"
        parent_page_content = self.get_parent_page_template(domain, endpoints)
        parent_page_file = domain_dir / f"{parent_component_name}.tsx"
        
        with open(parent_page_file, 'w') as f:
            f.write(parent_page_content)
        
        generated_pages.append(parent_component_name)
        print(f"  📄 Generated {domain}/{parent_component_name}.tsx (parent router)")
        
        # 2. Generate main page (like UITestsMainPage)
        main_component_name = f"{domain.title()}MainPage"
        main_page_content = self.get_main_page_template(domain, endpoints)
        main_page_file = domain_dir / f"{main_component_name}.tsx"
        
        with open(main_page_file, 'w') as f:
            f.write(main_page_content)
        
        generated_pages.append(main_component_name)
        print(f"  📄 Generated {domain}/{main_component_name}.tsx (main content)")
        
        # 3. Generate individual pages for each endpoint
        for endpoint_name in endpoints:
            page_name = endpoint_name.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
            
            # Fix naming conflicts: if endpoint name matches domain, add "Feature" suffix
            if page_name.lower() == domain.lower():
                page_name = f"{page_name}Feature"
            
            component_name = f"{page_name}Page"
            mobile_component_name = f"Mobile{page_name}Page"
            
            desktop_content, mobile_content = self.get_individual_page_template(endpoint_name, domain, page_name)
            
            # Write desktop page
            page_file = domain_dir / f"{component_name}.tsx"
            with open(page_file, 'w') as f:
                f.write(desktop_content)
            
            # Write mobile page
            mobile_page_file = domain_dir / f"{mobile_component_name}.tsx"
            with open(mobile_page_file, 'w') as f:
                f.write(mobile_content)
            
            generated_pages.append(component_name)
            generated_pages.append(mobile_component_name)
            print(f"  📄 Generated {domain}/{component_name}.tsx")
            print(f"  📱 Generated {domain}/{mobile_component_name}.tsx")
            
            # 4. Generate page wrappers (desktop and mobile) for each endpoint
            wrapper_name = f"{page_name}PageWrapper"
            mobile_wrapper_name = f"Mobile{page_name}PageWrapper"
            desktop_wrapper_content, mobile_wrapper_content = self.get_page_wrapper_template(endpoint_name, domain, page_name)
            
            # Write desktop wrapper
            wrapper_file = components_dir / f"{wrapper_name}.tsx"
            with open(wrapper_file, 'w') as f:
                f.write(desktop_wrapper_content)
            
            # Write mobile wrapper
            mobile_wrapper_file = components_dir / f"{mobile_wrapper_name}.tsx"
            with open(mobile_wrapper_file, 'w') as f:
                f.write(mobile_wrapper_content)
            
            print(f"  🔧 Generated components/{domain}/{wrapper_name}.tsx")
            print(f"  📱 Generated components/{domain}/{mobile_wrapper_name}.tsx")
        
        # 5. Generate domain actions hook
        actions_hook_name = f"use{domain.title()}Actions"
        actions_content = self.get_domain_actions_hook_template(domain, endpoints)
        actions_file = hooks_dir / f"{actions_hook_name}.ts"
        
        with open(actions_file, 'w') as f:
            f.write(actions_content)
        
        print(f"  🎣 Generated hooks/{domain}/{actions_hook_name}.ts")
        
        # 6. Generate component index
        self.generate_component_index(domain, endpoints)
        
        return generated_pages
    
    def generate_component_index(self, domain: str, endpoints: List[str]):
        """Generate component index for wrappers"""
        components_dir = self.get_src_path() / "components" / domain
        
        # Generate exports for all wrappers
        exports = []
        for endpoint in endpoints:
            page_name = endpoint.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
            
            # Fix naming conflicts: if endpoint name matches domain, add "Feature" suffix
            if page_name.lower() == domain.lower():
                page_name = f"{page_name}Feature"
                
            wrapper_name = f"{page_name}PageWrapper"
            exports.append(f'export {{ {wrapper_name} }} from "./{wrapper_name}";')
        
        index_content = '\n'.join(exports) + '\n'
        
        index_file = components_dir / "index.ts"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        print(f"  📝 Generated components/{domain}/index.ts")
    
    def generate_core_infrastructure(self):
        """Generate core hooks, stores, and infrastructure needed by the pages"""
        print("🛠️ Generating core infrastructure...")
        
        # Create core directories
        core_hooks_dir = self.get_src_path() / "hooks" / "core"
        core_hooks_dir.mkdir(parents=True, exist_ok=True)
        
        audio_hooks_dir = self.get_src_path() / "hooks" / "audio"
        audio_hooks_dir.mkdir(parents=True, exist_ok=True)
        
        stores_dir = self.get_src_path() / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)
        
        contexts_dir = self.get_src_path() / "contexts"
        contexts_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate usePageInstructions hook
        page_instructions_content = '''import { useEffect } from "react";
import { useInstructions } from "../useInstructions";

export const usePageInstructions = (pageId: string) => {
  const { setInstructions } = useInstructions();

  useEffect(() => {
    // Set basic instructions for the page
    setInstructions(`${pageId.charAt(0).toUpperCase() + pageId.slice(1)} Page`, [
      `Welcome to the ${pageId} page`,
      "Use the action menu to navigate",
      "This page follows the domain-driven architecture"
    ]);
  }, [pageId, setInstructions]);
};
'''
        
        with open(core_hooks_dir / "usePageInstructions.ts", 'w') as f:
            f.write(page_instructions_content)
        print("  🎣 Generated hooks/core/usePageInstructions.ts")
        
        # Generate useInstructions hook
        instructions_content = '''import { create } from "zustand";

interface InstructionsState {
  title: string;
  instructions: string[];
  setInstructions: (title: string, instructions: string[]) => void;
}

export const useInstructions = create<InstructionsState>((set) => ({
  title: "",
  instructions: [],
  setInstructions: (title, instructions) => set({ title, instructions }),
}));
'''
        
        with open(self.get_src_path() / "hooks" / "useInstructions.ts", 'w') as f:
            f.write(instructions_content)
        print("  🎣 Generated hooks/useInstructions.ts")
        
        # Generate appStore
        app_store_content = '''import { create } from "zustand";
import { persist, subscribeWithSelector } from "zustand/middleware";

export type TabId = 'chess' | 'user' | 'learning' | 'progress' | 'support' | 'other';

interface AppState {
  selectedTab: TabId;
  currentChildPage: string | null;
  setSelectedTab: (tab: TabId) => void;
  setCurrentChildPage: (childPage: string | null) => void;
}

export const useAppStore = create<AppState>()(
  subscribeWithSelector(
    persist(
      (set) => ({
        selectedTab: 'chess',
        currentChildPage: null,
        setSelectedTab: (tab) => set({ selectedTab: tab }),
        setCurrentChildPage: (childPage) => set({ currentChildPage: childPage }),
      }),
      {
        name: 'chess-app-store',
        partialize: (state) => ({
          selectedTab: state.selectedTab,
          currentChildPage: state.currentChildPage,
        }),
      }
    )
  )
);
'''
        
        with open(stores_dir / "appStore.ts", 'w') as f:
            f.write(app_store_content)
        print("  🏪 Generated stores/appStore.ts")
        
        # Generate useUIClickSoundOptimized hook
        audio_hook_content = '''import { useCallback } from "react";

export const useUIClickSoundOptimized = () => {
  const playMove = useCallback((isCapture: boolean = false) => {
    // Audio feedback implementation
    // For now, just a console log - can be enhanced with actual audio
    console.log(`UI Sound: ${isCapture ? 'capture' : 'move'}`);
  }, []);

  const playUISound = useCallback((soundType: string) => {
    console.log(`UI Sound: ${soundType}`);
  }, []);

  return {
    playMove,
    playUISound,
  };
};
'''
        
        with open(audio_hooks_dir / "useUIClickSoundOptimized.ts", 'w') as f:
            f.write(audio_hook_content)
        print("  🔊 Generated hooks/audio/useUIClickSoundOptimized.ts")
        
        print("✅ Core infrastructure generated successfully!")
    
    def generate_domain_index(self, domain: str, page_names: List[str]):
        """Generate index.ts file for a domain's pages"""
        domain_dir = self.get_src_path() / "pages" / domain
        
        # Generate exports
        exports = []
        for page_name in page_names:
            exports.append(f'export {{ {page_name} }} from "./{page_name}";')
        
        index_content = '\n'.join(exports) + '\n'
        
        index_file = domain_dir / "index.ts"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        print(f"  📝 Generated {domain}/index.ts")
    
    def generate_main_pages_index(self, domains: List[str]):
        """Generate main pages/index.ts file"""
        pages_dir = self.get_src_path() / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate exports for all domain directories
        exports = []
        for domain in domains:
            exports.append(f'export * from "./{domain}";')
        
        index_content = '\n'.join(exports) + '\n'
        
        index_file = pages_dir / "index.ts"
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        print("📝 Generated main pages/index.ts")
    
    def generate_all_domain_pages(self, all_endpoints: List[str]):
        """Generate grouped pages from backend config endpoints"""
        print("🚀 Generating grouped pages from backend config...")
        
        # Group endpoints into logical page domains
        page_domains = self.group_endpoints_by_page_domain(all_endpoints)
        print(f"📊 Grouped {len(all_endpoints)} endpoints into {len(page_domains)} page domains")
        
        all_domains = []
        
        # Generate pages for each domain group
        for domain, endpoints in page_domains.items():
            print(f"🔧 Generating {domain} pages (groups {len(endpoints)} endpoints)...")
            generated_pages = self.generate_domain_pages(domain, endpoints)
            self.generate_domain_index(domain, generated_pages)
            all_domains.append(domain)
        
        # Generate main index
        self.generate_main_pages_index(all_domains)
        
        print("✅ All grouped pages generated successfully!")
    
    def generate_specific_domain_pages(self, domain: str, endpoints: List[str]):
        """Generate pages for a specific domain only"""
        print(f"🔧 Generating {domain} domain pages...")
        
        generated_pages = self.generate_domain_pages(domain, endpoints)
        self.generate_domain_index(domain, generated_pages)
        
        print(f"✅ {domain} domain pages generated successfully!")