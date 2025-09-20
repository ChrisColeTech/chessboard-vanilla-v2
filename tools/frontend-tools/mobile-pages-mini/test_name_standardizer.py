#!/usr/bin/env python3

import sys
from pathlib import Path

# Add parent directory to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from shared.name_standardizer import NameStandardizer

def test_name_standardizer():
    test_names = ['HTTPTracker', 'JSONValidator', 'APIClient', 'TestRunner']
    
    print("=== Testing NameStandardizer.to_pascal_case ===")
    for name in test_names:
        result = NameStandardizer.to_pascal_case(name)
        print(f'{name} -> {result}')
        
        # Also test the _split_to_words method
        words = NameStandardizer._split_to_words(name)
        print(f'  Words: {words}')
        print()

if __name__ == "__main__":
    test_name_standardizer()