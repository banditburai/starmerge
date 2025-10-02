"""Main API for tailwind-merge."""

from typing import Optional, overload, List, Union, Any

from starmerge.lib.create_tailwind_merge import create_tailwind_merge
from starmerge.lib.default_config import get_default_config
from starmerge.lib.types import TailwindMerge
from starmerge.lib.tw_join import tw_join


def _create_tailwind_merge() -> TailwindMerge:
    tailwind_merge_fn = create_tailwind_merge(get_default_config)
    tailwind_merge_fn.config = get_default_config()  # type: ignore
    return tailwind_merge_fn


tailwind_merge = _create_tailwind_merge()


@overload
def merge(*args: str) -> str: ...

@overload
def merge(class_list: List[Any]) -> str: ...

def merge(*args: Any) -> str:
    if not args:
        return ""

    if len(args) == 1 and isinstance(args[0], list):
        classes = tw_join(args[0])
        return tailwind_merge(classes)

    classes = tw_join(*args)
    return tailwind_merge(classes)


__all__ = ["tailwind_merge", "merge"]
