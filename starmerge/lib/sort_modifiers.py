from collections.abc import Callable

from starmerge.lib.types import AnyConfig


def create_sort_modifiers(config: AnyConfig) -> Callable[[list[str]], list[str]]:
    sensitive = set(config.get('order_sensitive_modifiers', []))

    def sort_modifiers(modifiers: list[str]) -> list[str]:
        if len(modifiers) <= 1:
            return modifiers

        sorted_modifiers: list[str] = []
        unsorted_modifiers: list[str] = []

        for modifier in modifiers:
            if modifier.startswith('[') or modifier in sensitive:
                sorted_modifiers.extend(sorted(unsorted_modifiers))
                sorted_modifiers.append(modifier)
                unsorted_modifiers = []
            else:
                unsorted_modifiers.append(modifier)

        sorted_modifiers.extend(sorted(unsorted_modifiers))
        return sorted_modifiers

    return sort_modifiers
