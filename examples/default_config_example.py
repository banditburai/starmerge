"""
Example demonstrating the use of the default configuration with create_tailwind_merge.

This example shows how to use the default Tailwind CSS configuration with the
tailwind-merge library to merge class lists.
"""

from starmerge.lib.create_tailwind_merge import create_tailwind_merge
from starmerge.lib.default_config import get_default_config


def main():
    """
    Demonstrate using the default configuration with create_tailwind_merge.
    """
    # Create a tailwind_merge function using the default configuration
    tailwind_merge = create_tailwind_merge(get_default_config)
    
    # Example class merges
    test_cases = [
        'p-4 p-5',
        'text-red-500 text-blue-500',
        'bg-red-500 bg-opacity-50 bg-blue-500',
        'm-4 mx-8',
        'rounded-md rounded-t-lg',
        'flex items-center justify-between justify-center',
        'border border-2 border-red-500',
        'p-2 px-4 py-8',
        'w-full w-10',
        'text-sm font-bold text-lg',
        'grid grid-cols-3 grid-cols-4',
    ]
    
    # Test and print the results
    print("Default Configuration Examples:")
    print("-" * 30)
    
    for classes in test_cases:
        merged = tailwind_merge(classes)
        print(f"Input:  '{classes}'")
        print(f"Output: '{merged}'")
        print("-" * 30)


if __name__ == "__main__":
    main() 