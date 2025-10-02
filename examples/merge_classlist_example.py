"""
Example demonstrating the use of merge_class_list.

This example shows how to use the merge_class_list function to merge
Tailwind CSS classes, handling conflicts according to the configured rules.
"""

from starmerge.lib.merge_classlist import merge_class_list
from starmerge.lib.parse_class_name import create_parse_class_name
from starmerge.lib.class_group_utils import create_class_group_utils
from starmerge.lib.sort_modifiers import create_sort_modifiers


class SimpleConfigUtils:
    """Simple implementation of ConfigUtils for the example."""
    
    def __init__(self, parse_class_name, get_class_group_id, get_conflicting_class_group_ids, sort_modifiers):
        """Initialize with the required utility functions."""
        self.parse_class_name = parse_class_name
        self.get_class_group_id = get_class_group_id
        self.get_conflicting_class_group_ids = get_conflicting_class_group_ids
        self.sort_modifiers = sort_modifiers


def main():
    """Run the merge_classlist example."""
    # Create a simple configuration
    config = {
        'prefix': None,
        'theme': {},
        'class_groups': {
            'display': ['block', 'inline', 'inline-block', 'flex', 'grid', 'hidden'],
            'float': ['float-left', 'float-right', 'float-none'],
            'clear': ['clear-left', 'clear-right', 'clear-both', 'clear-none'],
            'padding': ['p-0', 'p-1', 'p-2', 'p-4', 'p-8', 'px-1', 'px-2', 'py-1', 'py-2'],
            'margin': ['m-0', 'm-1', 'm-2', 'm-4', 'm-8', 'mx-1', 'mx-2', 'my-1', 'my-2'],
            'text-color': ['text-red', 'text-blue', 'text-green', 'text-black', 'text-white'],
            'bg-color': ['bg-red', 'bg-blue', 'bg-green', 'bg-black', 'bg-white'],
        },
        'conflicting_class_groups': {
            'float': ['clear'],
            'clear': ['float'],
            'padding': ['margin'],
            'margin': ['padding'],
            'text-color': ['bg-color'],
            'bg-color': ['text-color'],
        },
        'conflicting_class_group_modifiers': {},
        'order_sensitive_modifiers': ['hover', 'focus', 'sm', 'md', 'lg', 'xl'],
    }
    
    # Create utility functions
    parse_class_name = create_parse_class_name(config)
    get_class_group_id, get_conflicting_class_group_ids = create_class_group_utils(config)
    sort_modifiers = create_sort_modifiers(config)
    
    # Create a config utils object
    config_utils = SimpleConfigUtils(
        parse_class_name,
        get_class_group_id,
        get_conflicting_class_group_ids,
        sort_modifiers
    )
    
    # Test cases
    test_cases = [
        'block inline',
        'float-left clear-left',
        'p-2 m-4',
        'text-red bg-blue text-green',
        'hover:block focus:inline',
        'sm:p-2 md:p-4 lg:p-8',
        'block non-tailwind-class inline',
        'p-2 p-4 p-8',
    ]
    
    # Run test cases
    print("Merge Class List Examples:")
    print("-" * 50)
    for test_case in test_cases:
        result = merge_class_list(test_case, config_utils)
        print(f"Input:  '{test_case}'")
        print(f"Output: '{result}'")
        print("-" * 50)


if __name__ == '__main__':
    main() 