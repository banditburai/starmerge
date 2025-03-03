"""
Example usage of validator functions from tw_merge.

This script demonstrates how to use the validator functions from the tw_merge library
to validate different types of Tailwind CSS class values.
"""

from tw_merge.lib.validators import (
    is_arbitrary_value,
    is_arbitrary_length,
    is_arbitrary_number,
    is_arbitrary_position,
    is_fraction,
    is_integer,
    is_number,
    is_percent,
    is_tshirt_size,
)


def main():
    """Run the example."""
    print("Tailwind Merge Validators Example")
    print("=================================")
    
    test_values = [
        "100px",              # A length
        "50%",                # A percentage
        "1/2",                # A fraction
        "md",                 # A t-shirt size
        "123",                # A number
        "3.14",               # A decimal number
        "[200px]",            # An arbitrary length value
        "[length:var(--size)]",  # An arbitrary length with label
        "[number:10]",        # An arbitrary number with label
        "[position:center]",  # An arbitrary position with label
        "url(image.jpg)",     # An image URL
        "[url:var(--image)]", # An arbitrary image with label
        "rgb(255, 0, 0)",     # A color function
        "[0_35px_60px_-15px_rgba(0,0,0,0.3)]",  # A shadow value
    ]
    
    # Test each value with different validators
    for value in test_values:
        print(f"\nValue: '{value}'")
        print(f"  is_arbitrary_value: {is_arbitrary_value(value)}")
        print(f"  is_arbitrary_length: {is_arbitrary_length(value)}")
        print(f"  is_arbitrary_number: {is_arbitrary_number(value)}")
        print(f"  is_arbitrary_position: {is_arbitrary_position(value)}")
        print(f"  is_fraction: {is_fraction(value)}")
        print(f"  is_integer: {is_integer(value)}")
        print(f"  is_number: {is_number(value)}")
        print(f"  is_percent: {is_percent(value)}")
        print(f"  is_tshirt_size: {is_tshirt_size(value)}")


if __name__ == "__main__":
    main() 