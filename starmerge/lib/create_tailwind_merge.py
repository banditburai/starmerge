"""Create Tailwind Merge function generator for merging class lists."""

from typing import Any, Callable, List, TypeVar, Dict, cast

from starmerge.lib.config_utils import create_config_utils, ConfigUtils
from starmerge.lib.merge_classlist import merge_class_list
from starmerge.lib.tw_join import tw_join, ClassNameValue
from starmerge.lib.types import AnyConfig

CreateConfigFirst = Callable[[], AnyConfig]
CreateConfigSubsequent = Callable[[AnyConfig], AnyConfig]
TailwindMerge = Callable[..., str]


class ConfigUtilsWrapper:
    """Wrapper class for ConfigUtils dictionary to allow attribute access."""

    def __init__(self, config_utils_dict: Dict[str, Any]):
        self.config_utils_dict = config_utils_dict

    def __getattr__(self, name: str) -> Any:
        if name in self.config_utils_dict:
            return self.config_utils_dict[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


def create_tailwind_merge(
    create_config_first: CreateConfigFirst,
    *create_config_rest: CreateConfigSubsequent
) -> TailwindMerge:
    config_utils_wrapper = None
    cache_get = None
    cache_set = None

    def init_tailwind_merge(class_list: str) -> str:
        nonlocal config_utils_wrapper, cache_get, cache_set, function_to_call

        config = create_config_first()
        for create_config_current in create_config_rest:
            config = create_config_current(config)

        config_utils_dict = create_config_utils(config)
        config_utils_wrapper = ConfigUtilsWrapper(config_utils_dict)
        cache_get = config_utils_dict['cache'].get
        cache_set = config_utils_dict['cache'].set
        function_to_call = tailwind_merge

        return tailwind_merge(class_list)

    def tailwind_merge(class_list: str) -> str:
        cached_result = cache_get(class_list)

        if cached_result:
            return cached_result

        result = merge_class_list(class_list, config_utils_wrapper)
        cache_set(class_list, result)

        return result

    def call_tailwind_merge(*args: ClassNameValue) -> str:
        return function_to_call(tw_join(*args))

    function_to_call = init_tailwind_merge

    return call_tailwind_merge
