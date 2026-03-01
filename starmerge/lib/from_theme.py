from starmerge.lib.types import AnyThemeGroupIds, ClassGroup, ThemeObject


class _ThemeGetter:
    __slots__ = ("key",)
    is_theme_getter: bool = True

    def __init__(self, key: AnyThemeGroupIds) -> None:
        self.key = key

    def __call__(self, theme: ThemeObject) -> ClassGroup:
        if not isinstance(theme, dict):
            return []
        return theme.get(self.key, [])


def from_theme(key: AnyThemeGroupIds) -> _ThemeGetter:
    return _ThemeGetter(key)
