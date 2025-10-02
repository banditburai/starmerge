"""
Sort modifiers utility for tailwind-merge.

Position-sensitive modifiers (arbitrary variants and configured sensitive modifiers)
are preserved in their original position, while others are sorted alphabetically.
"""

from typing import List, Callable, Dict

from starmerge.lib.types import AnyConfig


def create_sort_modifiers(config: AnyConfig) -> Callable[[List[str]], List[str]]:
    order_sensitive_modifiers: Dict[str, bool] = {}
    sensitive_modifiers = config.get('order_sensitive_modifiers',
                                    config.get('orderSensitiveModifiers', []))

    for modifier in sensitive_modifiers:
        order_sensitive_modifiers[modifier] = True

    def sort_modifiers(modifiers: List[str]) -> List[str]:
        if len(modifiers) <= 1:
            return modifiers

        sorted_modifiers: List[str] = []
        unsorted_modifiers: List[str] = []

        for modifier in modifiers:
            is_position_sensitive = (
                modifier.startswith('[') or
                modifier in order_sensitive_modifiers
            )

            if is_position_sensitive:
                sorted_modifiers.extend(sorted(unsorted_modifiers))
                sorted_modifiers.append(modifier)
                unsorted_modifiers = []
            else:
                unsorted_modifiers.append(modifier)

        sorted_modifiers.extend(sorted(unsorted_modifiers))
        return sorted_modifiers

    return sort_modifiers
