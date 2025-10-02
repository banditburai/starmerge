"""Theme getter utility for creating functions that access theme values."""

from typing import Any, Dict, List, Protocol, Union

from starmerge.lib.types import AnyThemeGroupIds, ThemeObject


class ThemeGetter(Protocol):
    """Theme getter function type."""
    isThemeGetter: bool
    def __call__(self, theme: ThemeObject) -> List[Any]: ...


def from_theme(key: AnyThemeGroupIds) -> ThemeGetter:
    def theme_getter(theme: Union[ThemeObject, Any]) -> List[Any]:
        if not isinstance(theme, dict):
            return []
        return theme.get(key, [])

    setattr(theme_getter, 'is_theme_getter', True)
    return theme_getter  # type: ignore
