#!/usr/bin/env python3
"""
Batch generator for concept variant child pages
Generates multiple concepts with multiple variants each
"""

import subprocess
import sys
from pathlib import Path

def generate_concept_variants(start_concept=6, end_concept=13, variants_per_concept=4):
    """Generate concept variant child pages in batches"""
    
    base_path = "/mnt/c/Projects/chessboard-vanilla-v2"
    parent = "splash"
    
    # Common actions for all concept variants
    actions = [
        "test-concept:Test Concept:Zap:default",
        "restart-demo:Restart Demo:RotateCcw:secondary", 
        "toggle-fullscreen:Toggle Fullscreen:Maximize2:default",
        "export-concept:Export Concept:Download:secondary",
        "previous-variant:Previous Variant:ChevronLeft:secondary",
        "next-variant:Next Variant:ChevronRight:secondary"
    ]
    actions_str = ",".join(actions)
    
    # Generate by concept (4 variants at a time)
    for concept_num in range(start_concept, end_concept + 1):
        print(f"\n🎨 Generating Concept {concept_num} variants...")
        
        # Build children list for this concept
        children = []
        for variant in range(1, variants_per_concept + 1):
            children.append(f"concept{concept_num}variant{variant}")
        
        children_str = ",".join(children)
        
        # Run the generator
        cmd = [
            "python", "tools/child_page_generator.py",
            "--parent", parent,
            "--children", children_str,
            "--actions", actions_str,
            "--base-path", base_path
        ]
        
        print(f"📄 Creating: {children_str}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_path)
            if result.returncode == 0:
                print(f"✅ Concept {concept_num} variants created successfully!")
                print(result.stdout)
            else:
                print(f"❌ Error creating Concept {concept_num} variants:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Exception running generator: {e}")
            return False
    
    print(f"\n🎉 Successfully generated concepts {start_concept}-{end_concept} with {variants_per_concept} variants each!")
    print(f"📊 Total child pages created: {(end_concept - start_concept + 1) * variants_per_concept}")
    
    # Print navigation summary
    print(f"\n📋 Navigation Structure:")
    for concept_num in range(start_concept, end_concept + 1):
        print(f"   Concept {concept_num}:")
        for variant in range(1, variants_per_concept + 1):
            print(f"     • Variant {variant} (concept{concept_num}variant{variant})")
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate concept variant child pages in batches')
    parser.add_argument('--start', type=int, default=6, help='Starting concept number')
    parser.add_argument('--end', type=int, default=13, help='Ending concept number')
    parser.add_argument('--variants', type=int, default=4, help='Variants per concept')
    
    args = parser.parse_args()
    
    success = generate_concept_variants(args.start, args.end, args.variants)
    sys.exit(0 if success else 1)