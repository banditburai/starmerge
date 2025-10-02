"""
Example demonstrating how to use create_tailwind_merge.

This example shows how to create a custom tailwind merge function
with a simplified configuration, and how to use it to merge class lists.
"""

from starmerge import create_tailwind_merge


def main():
    """Demonstrate create_tailwind_merge usage."""
    # Create a custom tailwind merge function with a simplified configuration
    tailwind_merge = create_tailwind_merge(
        lambda: {
            'cache_size': 20,
            'theme': {},
            'class_groups': {
                'width': [{'width': ['1', '2', '3', '4']}],
                'height': [{'height': ['1', '2', '3', '4']}],
                'color': [{'color': ['red', 'green', 'blue']}],
                'bg': [{'bg': ['red', 'green', 'blue']}],
                'border': [{'border': ['red', 'green', 'blue']}],
                'float': ['float-left', 'float-right', 'float-none'],
                'display': ['block', 'inline', 'flex', 'grid'],
                'position': ['static', 'absolute', 'relative', 'fixed'],
            },
            'conflicting_class_groups': {
                'width': [],
                'height': [],
                'color': [],
                'bg': [],
                'border': [],
                'float': [],
                'display': [],
                'position': [],
            },
            'conflicting_class_group_modifiers': {},
            'order_sensitive_modifiers': [],
        }
    )

    # Demonstrate merging class lists
    print("Example 1: Merging width classes")
    print("Input: 'width-1 width-2'")
    print(f"Output: '{tailwind_merge('width-1 width-2')}'")
    print()

    print("Example 2: Merging display classes")
    print("Input: 'block inline flex'")
    print(f"Output: '{tailwind_merge('block inline flex')}'")
    print()

    print("Example 3: Merging color classes")
    print("Input: 'color-red bg-blue color-green'")
    print(f"Output: '{tailwind_merge('color-red bg-blue color-green')}'")
    print()

    print("Example 4: Merging with modifiers")
    print("Input: 'hover:color-red focus:color-blue hover:color-green'")
    print(f"Output: '{tailwind_merge('hover:color-red focus:color-blue hover:color-green')}'")
    print()

    print("Example 5: Merging different class groups")
    print("Input: 'width-1 height-2 color-red'")
    print(f"Output: '{tailwind_merge('width-1 height-2 color-red')}'")
    print()

    # Demonstrate extending configuration
    print("Example 6: Using a modified configuration")
    custom_tailwind_merge = create_tailwind_merge(
        lambda: {
            'cache_size': 20,
            'theme': {},
            'class_groups': {
                'width': [{'width': ['1', '2', '3', '4']}],
                'text': [{'text': ['sm', 'base', 'lg', 'xl']}],
            },
            'conflicting_class_groups': {
                'width': [],
                'text': [],
            },
            'conflicting_class_group_modifiers': {},
            'order_sensitive_modifiers': [],
        },
        lambda config: {
            **config,
            'class_groups': {
                **config['class_groups'],
                'custom': ['custom-1', 'custom-2', 'custom-3'],
            },
            'conflicting_class_groups': {
                **config['conflicting_class_groups'],
                'custom': ['width'],
            },
        }
    )

    print("Input: 'width-1 custom-2'")
    print(f"Output: '{custom_tailwind_merge('width-1 custom-2')}'")
    print()


if __name__ == "__main__":
    main() 