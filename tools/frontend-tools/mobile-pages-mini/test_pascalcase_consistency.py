#!/usr/bin/env python3
"""
Test for PascalCase naming consistency in template variables
Tests that hyphenated names like 'audio-demo' generate consistent PascalCase throughout all templates
"""

import tempfile
import os
from pathlib import Path
from modules.config import PageConfig
from modules.variable_generator import VariableGenerator
from modules.template_engine import TemplateEngine


def test_hyphenated_name_consistency():
    """Test that hyphenated names generate consistent PascalCase variables"""
    print("🧪 Testing hyphenated name consistency...")
    
    # Create a config with hyphenated name
    config = PageConfig(name="audio-demo", parent="uitests", mobile=True)
    
    # Test the base_name conversion
    print(f"  📊 Input name: 'audio-demo'")
    print(f"  📊 Generated base_name: '{config.base_name}'")
    assert config.base_name == "AudioDemo", f"Expected 'AudioDemo', got '{config.base_name}'"
    
    # Test page_name property
    print(f"  📊 Generated page_name: '{config.page_name}'")
    assert config.page_name == "AudioDemoPage", f"Expected 'AudioDemoPage', got '{config.page_name}'"
    
    # Test variable generation
    from modules.config import GenerationContext, ProjectCapabilities
    
    context = GenerationContext(
        frontend_root=Path("/tmp/test"),
        config=config,
        capabilities=ProjectCapabilities(),
        variables={}
    )
    
    generator = VariableGenerator()
    variables = generator.generate_child_variables(context)
    
    # Check child variables
    print(f"  📊 CHILD_NAME variable: '{variables['CHILD_NAME']}'")
    print(f"  📊 MOBILE_CHILD_NAME variable: '{variables['MOBILE_CHILD_NAME']}'")
    
    assert variables['CHILD_NAME'] == "AudioDemo", f"Expected 'AudioDemo', got '{variables['CHILD_NAME']}'"
    assert variables['MOBILE_CHILD_NAME'] == "MobileAudioDemo", f"Expected 'MobileAudioDemo', got '{variables['MOBILE_CHILD_NAME']}'"
    
    print("  ✅ Base naming test passed!")


def test_template_variable_consistency():
    """Test that template variables are consistent across wrapper templates"""
    print("🧪 Testing template variable consistency...")
    
    # Create a temporary template directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        templates_dir = Path(temp_dir) / "templates"
        dynamic_dir = templates_dir / "dynamic"
        components_dir = dynamic_dir / "components"
        components_dir.mkdir(parents=True)
        
        # Create a child wrapper template
        wrapper_template = components_dir / "child-wrapper-full-hooks.tsx.template"
        wrapper_content = '''import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { {{CHILD_NAME}}Page } from "../../pages/{{PARENT_ID}}/{{CHILD_NAME}}Page";
import { {{MOBILE_CHILD_NAME}}Page } from "../../pages/{{PARENT_ID}}/{{MOBILE_CHILD_NAME}}Page";

export const {{CHILD_NAME}}PageWrapper: React.FC = () => {
  const isMobile = useIsMobile();
  
  usePageInstructions("{{CHILD_ID}}");
  usePageActions("{{CHILD_ID}}");

  return isMobile ? <{{MOBILE_CHILD_NAME}}Page /> : <{{CHILD_NAME}}Page />;
};'''
        wrapper_template.write_text(wrapper_content)
        
        # Test template rendering
        engine = TemplateEngine(templates_dir)
        
        # Create config for hyphenated name
        config = PageConfig(name="audio-demo", parent="uitests", mobile=True)
        
        from modules.config import GenerationContext, ProjectCapabilities
        context = GenerationContext(
            frontend_root=Path("/tmp/test"),
            config=config,
            capabilities=ProjectCapabilities(),
            variables={}
        )
        
        generator = VariableGenerator()
        variables = generator.generate_child_variables(context)
        
        print(f"  📊 Template variables:")
        for key, value in variables.items():
            if 'CHILD' in key or 'PARENT' in key:
                print(f"    {key}: '{value}'")
        
        # Render the template
        rendered = engine.render_template("components/child-wrapper-full-hooks.tsx.template", variables)
        
        print(f"  📝 Rendered template snippet:")
        lines = rendered.split('\n')
        for i, line in enumerate(lines):
            if 'import {' in line and 'Page' in line:
                print(f"    Line {i+1}: {line.strip()}")
            elif 'export const' in line:
                print(f"    Line {i+1}: {line.strip()}")
            elif 'return isMobile' in line:
                print(f"    Line {i+1}: {line.strip()}")
        
        # Check that all PascalCase is consistent
        assert "AudioDemoPage" in rendered, "Should contain 'AudioDemoPage' import"
        assert "MobileAudioDemoPage" in rendered, "Should contain 'MobileAudioDemoPage' import"
        assert "AudioDemoPageWrapper" in rendered, "Should contain 'AudioDemoPageWrapper' export"
        assert "<MobileAudioDemoPage />" in rendered, "Should contain '<MobileAudioDemoPage />' component"
        assert "<AudioDemoPage />" in rendered, "Should contain '<AudioDemoPage />' component"
        
        # Check that no lowercase variants exist
        assert "AudiodemoPage" not in rendered, "Should not contain 'AudiodemoPage' (lowercase 'd')"
        assert "MobileAudiodemoPage" not in rendered, "Should not contain 'MobileAudiodemoPage' (lowercase 'd')"
        assert "AudiodemoPageWrapper" not in rendered, "Should not contain 'AudiodemoPageWrapper' (lowercase 'd')"
        
        print("  ✅ Template consistency test passed!")


def test_edge_cases():
    """Test edge cases for PascalCase conversion"""
    print("🧪 Testing edge cases...")
    
    test_cases = [
        ("single-word", "SingleWord"),
        ("multi-word-name", "MultiWordName"),
        ("with_underscores", "WithUnderscores"),
        ("mixed-case_name", "MixedCaseName"),
        ("already-pascal", "AlreadyPascal"),
        ("lowercase", "Lowercase"),
        ("UPPERCASE", "Uppercase"),
    ]
    
    for input_name, expected in test_cases:
        config = PageConfig(name=input_name)
        print(f"  📊 '{input_name}' → '{config.base_name}' (expected: '{expected}')")
        assert config.base_name == expected, f"Expected '{expected}', got '{config.base_name}'"
    
    print("  ✅ Edge cases test passed!")


if __name__ == "__main__":
    test_hyphenated_name_consistency()
    test_template_variable_consistency()
    test_edge_cases()
    print("🎉 All PascalCase consistency tests completed!")