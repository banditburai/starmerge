from typing import Any, overload

from starmerge.lib.create_tailwind_merge import create_tailwind_merge
from starmerge.lib.default_config import get_default_config
from starmerge.lib.tw_join import tw_join


def _create_tailwind_merge():
    fn = create_tailwind_merge(get_default_config)
    fn.config = get_default_config()  # type: ignore[attr-defined]
    return fn


tailwind_merge = _create_tailwind_merge()


@overload
def merge(*args: str) -> str: ...


@overload
def merge(class_list: list[Any]) -> str: ...


def merge(*args: Any) -> str:
    if not args:
        return ""
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]
    return tailwind_merge(tw_join(*args))


__all__ = ["tailwind_merge", "merge"]
