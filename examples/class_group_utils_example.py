"""
Example usage of class_group_utils from tw_merge.

This script demonstrates how to use the class group utilities from the tw_merge library
to identify Tailwind CSS class groups and resolve conflicts.
"""

from tw_merge.lib.class_group_utils import create_class_group_utils
from typing import Dict, List, Any

def main():
    """Run the example."""
    print("Tailwind Merge Class Group Utils Example")
    print("========================================")
    
    # Define a simple config
    config = {
        'theme': {},
        'class_groups': {
            # Background colors
            'backgroundColor': [
                'bg-red', 'bg-blue', 'bg-green', 'bg-yellow',
                # Add dark variants directly
                'bg-dark-red', 'bg-dark-blue',
                # With validator function
                lambda class_name: class_name.startswith('bg-hex-')
            ],
            # Text colors
            'textColor': ['text-red', 'text-blue', 'text-green', 'text-yellow'],
            # Margins
            'margin': [
                'm-0', 'm-1', 'm-2', 'm-4', 'm-8',
                # Add direct variants for mx/my variants
                'mx-0', 'mx-1', 'mx-2', 'mx-4', 'mx-8',
                'my-0', 'my-1', 'my-2', 'my-4', 'my-8',
            ],
            # Paddings
            'padding': [
                'p-0', 'p-1', 'p-2', 'p-4', 'p-8',
                # Add direct variants for px/py variants
                'px-0', 'px-1', 'px-2', 'px-4', 'px-8',
                'py-0', 'py-1', 'py-2', 'py-4', 'py-8',
            ],
        },
        'conflicting_class_groups': {
            'backgroundColor': ['textColor'],
            'textColor': ['backgroundColor'],
            'margin': ['padding'],
            'padding': ['margin'],
        },
        'conflicting_class_group_modifiers': {
            'backgroundColor': ['margin'],
        }
    }
    
    # Create the class group utilities
    get_class_group_id, get_conflicting_class_group_ids = create_class_group_utils(config)
    
    # Test classes to identify
    test_classes = [
        'bg-red',                  # Standard class
        'bg-dark-blue',            # Nested variant
        'bg-hex-ff5500',           # Validator function
        'text-green',              # Different group
        'm-2',                     # Margin
        'mx-4',                    # Margin with x modifier
        'p-2',                     # Padding
        'py-8',                    # Padding with y modifier
        '[bg:blue]',               # Arbitrary property
        'unknown-class',           # Unknown class
    ]
    
    print("\nIdentifying class groups:")
    print("--------------------------")
    for class_name in test_classes:
        group_id = get_class_group_id(class_name)
        print(f"Class: '{class_name}' -> Group ID: {group_id}")
    
    print("\nChecking conflicting class groups:")
    print("---------------------------------")
    group_ids = ['backgroundColor', 'textColor', 'margin', 'padding']
    for group_id in group_ids:
        without_modifier = get_conflicting_class_group_ids(group_id, False)
        with_modifier = get_conflicting_class_group_ids(group_id, True)
        
        print(f"Group ID: '{group_id}'")
        print(f"  Without postfix modifier: {without_modifier}")
        print(f"  With postfix modifier: {with_modifier}")


if __name__ == "__main__":
    main() 