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
    
    def __init__(self, frontend_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2"):
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
        
        # Page instruction mapping - provides meaningful instructions for each page type
        self.page_instructions = {
            # Chess domain
            'puzzles': 'Solve chess puzzles to improve your tactical skills. Click on pieces to make moves.',
            'games': 'Play chess games against opponents or review completed matches.',
            'openings': 'Study chess opening theory and explore different opening variations.',
            'endgames': 'Practice essential endgame positions and techniques.',
            'analysis': 'Analyze chess positions using computer assistance and evaluation.',
            'historic-games': 'Browse and study famous chess games from history.',
            
            # User domain
            'auth': 'Sign in to your account or create a new account to access all features.',
            'sessions': 'Manage your active sessions and device connections.',
            'users': 'View and manage user profiles and information.',
            'profiles': 'Customize your chess profile, ratings, and preferences.',
            
            # Learning domain
            'tutorials': 'Interactive chess tutorials to learn fundamental concepts.',
            'learning': 'Structured chess courses covering all aspects of the game.',
            'learning-modules': 'Individual learning modules focusing on specific chess topics.',
            'tutorial-steps': 'Step-by-step guidance through chess learning materials.',
            'study-plans': 'Personalized study plans tailored to your chess level.',
            
            # Progress domain
            'stats': 'View your chess statistics, ratings, and performance trends.',
            'progress': 'Track your chess improvement over time with detailed metrics.',
            'achievements': 'Browse your chess achievements and unlock new milestones.',
            'analytics': 'Deep dive into your playing patterns and areas for improvement.',
            'puzzle-attempts': 'Review your puzzle solving history and accuracy.',
            
            # Support domain
            'help': 'Find answers to common questions and get support.',
            'subscriptions': 'Manage your premium subscriptions and billing.',
            'puzzle-sources': 'Explore different sources and databases of chess puzzles.',
            'game-reviews': 'Professional game reviews and analysis from chess masters.',
        }
    
    def get_page_instruction(self, endpoint_name: str) -> str:
        """Get meaningful instruction for a specific page/endpoint"""
        return self.page_instructions.get(endpoint_name, f'Navigate and interact with the {endpoint_name} interface.')
    
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
        
        return f'''import {{ useAppStore }} from "../../stores/appStore";
import {{ {main_component} }} from "./{main_component}";
{wrapper_imports_str}

export const {component_name} = () => {{
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
        instruction = self.get_page_instruction(domain)
        
        return f'''import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageData }} from "../../hooks/core/usePageData";
import {{ ChessboardLayout }} from "../../components/chess/ChessboardLayout";
import {{ DataTable }} from "../../components/ui/DataTable";

export const {component_name} = () => {{
  usePageInstructions("{domain}");
  const {{ data, loading, error }} = usePageData("{domain}");

  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={{<div className="uitest-layout-corner">{domain.title()} Main Top Left</div>}}
        top={{<div className="uitest-layout-center"></div>}}
        topRight={{<div className="uitest-layout-corner">{domain.title()} Main Top Right</div>}}
        left={{<div className="uitest-layout-corner">{domain.title()} Main Left</div>}}
        center={{<DataTable data={{data}} loading={{loading}} error={{error}} />}}
        right={{<div className="uitest-layout-corner">{domain.title()} Main Right</div>}}
        bottomLeft={{<div className="uitest-layout-corner">{domain.title()} Main Bottom Left</div>}}
        bottom={{<div className="uitest-layout-center"></div>}}
        bottomRight={{<div className="uitest-layout-corner">{domain.title()} Main Bottom Right</div>}}
        className="w-full h-full"
      />
    </div>
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
        instruction = self.get_page_instruction(endpoint_name)
        
        # Desktop template
        desktop_template = f'''import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageData }} from "../../hooks/core/usePageData";
import {{ ChessboardLayout }} from "../../components/chess/ChessboardLayout";
import {{ DataTable }} from "../../components/ui/DataTable";

export const {component_name} = () => {{
  usePageInstructions("{endpoint_name}");
  const {{ data, loading, error }} = usePageData("{endpoint_name}");

  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={{<div className="uitest-layout-corner">{page_name} Top Left</div>}}
        top={{<div className="uitest-layout-center"></div>}}
        topRight={{<div className="uitest-layout-corner">{page_name} Top Right</div>}}
        left={{<div className="uitest-layout-corner">{page_name} Left</div>}}
        center={{<DataTable data={{data}} loading={{loading}} error={{error}} />}}
        right={{<div className="uitest-layout-corner">{page_name} Right</div>}}
        bottomLeft={{<div className="uitest-layout-corner">{page_name} Bottom Left</div>}}
        bottom={{<div className="uitest-layout-center"></div>}}
        bottomRight={{<div className="uitest-layout-corner">{page_name} Bottom Right</div>}}
        className="w-full h-full"
      />
    </div>
  );
}};
'''

        # Mobile template
        mobile_template = f'''import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageData }} from "../../hooks/core/usePageData";
import {{ MobileChessboardLayout }} from "../../components/chess/MobileChessboardLayout";
import {{ DataTable }} from "../../components/ui/DataTable";

export const {mobile_component_name} = () => {{
  usePageInstructions("{endpoint_name}");
  const {{ data, loading, error }} = usePageData("{endpoint_name}");

  return (
    <div className="uitest-mobile-container-padded">
      <MobileChessboardLayout
        topPieces={{<div className="uitest-mobile-pieces">{page_name} Top Pieces</div>}}
        center={{<DataTable data={{data}} loading={{loading}} error={{error}} />}}
        bottomPieces={{<div className="uitest-mobile-pieces">{page_name} Bottom Pieces</div>}}
      />
    </div>
  );
}};
'''
        
        return desktop_template, mobile_template

    def get_page_wrapper_template(self, endpoint_name: str, domain: str, page_name: str = None) -> tuple:
        """Generate page wrapper template with mobile variant support"""
        if page_name is None:
            page_name = endpoint_name.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
        
        wrapper_name = f"{page_name}PageWrapper"
        mobile_wrapper_name = f"Mobile{page_name}PageWrapper"
        page_component = f"{page_name}Page"
        mobile_page_component = f"Mobile{page_name}Page"
        instruction = self.get_page_instruction(endpoint_name)
        
        # Generate desktop wrapper
        desktop_wrapper = f'''import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ {page_component} }} from "../../pages/{domain}/{page_component}";

export const {wrapper_name} = () => {{
  usePageInstructions("{endpoint_name}");
  
  return <{page_component} />;
}};
'''

        # Generate mobile wrapper  
        mobile_wrapper = f'''import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ {mobile_page_component} }} from "../../pages/{domain}/{mobile_page_component}";

export const {mobile_wrapper_name} = () => {{
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
        
        # Skip appStore generation - it will be handled by stores_generator
        print("  🏪 Skipped appStore generation (handled by stores_generator)")
        
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