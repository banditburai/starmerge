"""
Type definitions for tailwind-merge Python port.

This module contains type definitions used throughout the library,
ported from the original TypeScript implementation.
"""

from __future__ import annotations
from typing import (
    Any, 
    Callable, 
    Dict, 
    List, 
    Literal, 
    NotRequired,
    Optional, 
    Protocol, 
    TypeAlias,    
    TypedDict, 
    TypeVar, 
    Union,
    runtime_checkable
)
from dataclasses import dataclass

# Import literal types from generated module
# These will be populated by running scripts/update_types.py
from .generated_types import DefaultThemeGroupIds, DefaultClassGroupIds

# Type aliases for generic class and theme group IDs
AnyClassGroupIds = str
AnyThemeGroupIds = str

# TypeVars for generic type parameters
ClassGroupIds = TypeVar('ClassGroupIds', bound=str)
ThemeGroupIds = TypeVar('ThemeGroupIds', bound=str)

# Type alias for ClassValidator
ClassValidator: TypeAlias = Callable[[str], bool]

# Type alias for TailwindMerge function
TailwindMerge: TypeAlias = Callable[[str], str]

# Forward declarations using string literals for circular references
ClassGroup: TypeAlias = List["ClassDefinition"]
ClassObject: TypeAlias = Dict[str, "ClassGroup"]
ThemeObject: TypeAlias = Dict[str, "ClassGroup"]

# ThemeGetter class with isThemeGetter property
class ThemeGetter(Protocol):
    """Theme getter function type."""
    isThemeGetter: bool
    def __call__(self, theme: ThemeObject) -> ClassGroup:
        ...

# Now we can define ClassDefinition
ClassDefinition: TypeAlias = Union[str, ClassValidator, ThemeGetter, ClassObject]

@dataclass
class ParsedClassName:
    """
    Type of the result returned by the `parse_class_name` function.
    
    This is an experimental feature and may introduce breaking changes in any minor version update.
    """
    # Modifiers of the class in the order they appear in the class.
    modifiers: List[str]
    
    # Whether the class has an `!important` modifier.
    has_important_modifier: bool
    
    # Base class without preceding modifiers.
    base_class_name: str
    
    # Index position of a possible postfix modifier in the class.
    # If the class has no postfix modifier, this is None.
    maybe_postfix_modifier_position: Optional[int] = None
    
    # Whether the class is external and merging logic should be skipped.
    is_external: bool = False
    
    def __getitem__(self, key):
        """Make the object subscriptable."""
        if key == "modifiers":
            return self.modifiers
        elif key == "has_important_modifier":
            return self.has_important_modifier
        elif key == "base_class_name":
            return self.base_class_name
        elif key == "maybe_postfix_modifier_position":
            return self.maybe_postfix_modifier_position
        elif key == "is_external":
            return self.is_external
        else:
            raise KeyError(f"Key '{key}' not found")


class ExperimentalParseClassNameParam(TypedDict):
    """
    Type of param passed to the `experimental_parse_class_name` function.
    
    This is an experimental feature and may introduce breaking changes in any minor version update.
    """
    class_name: str
    parse_class_name: Callable[[str], ParsedClassName]


class ConfigStaticPart(TypedDict):
    """
    The static part of the tailwind-merge configuration.
    When merging multiple configurations, the properties of this interface are always overridden.
    """
    # Integer indicating size of LRU cache used for memoizing results.
    # - Cache might be up to twice as big as `cacheSize`
    # - No cache is used for values <= 0
    cache_size: int
    
    # Prefix added to Tailwind-generated classes
    prefix: NotRequired[str]
    
    # Allows to customize parsing of individual classes passed to `tw_merge`.
    # All classes passed to `tw_merge` outside of cache hits are passed to this function
    # before it is determined whether the class is a valid Tailwind CSS class.
    experimental_parse_class_name: NotRequired[Callable[[ExperimentalParseClassNameParam], ParsedClassName]]
    
    # Custom separator for modifiers in Tailwind classes
    separator: NotRequired[str]


class ConfigGroupsPart(TypedDict):
    """
    The dynamic part of the tailwind-merge configuration.
    When merging multiple configurations, the user can choose to either override or extend the properties.
    """
    # Theme scales used in classGroups.
    theme: ThemeObject
    
    # Object with groups of classes.
    class_groups: Dict[str, ClassGroup]
    
    # Conflicting classes across groups.
    conflicting_class_groups: NotRequired[Dict[str, List[str]]]
    
    # Postfix modifiers conflicting with other class groups.
    conflicting_class_group_modifiers: NotRequired[Dict[str, List[str]]]
    
    # Modifiers whose order among multiple modifiers should be preserved
    # because their order changes which element gets targeted.
    order_sensitive_modifiers: NotRequired[List[str]]


class Config(ConfigStaticPart, ConfigGroupsPart):
    """
    Type the tailwind-merge configuration adheres to.
    """
    pass


class PartialConfigGroupsPart(TypedDict, total=False):
    """Partial version of ConfigGroupsPart for extensions."""
    theme: ThemeObject
    class_groups: Dict[str, ClassGroup]
    conflicting_class_groups: Dict[str, List[str]]
    conflicting_class_group_modifiers: Dict[str, List[str]]
    order_sensitive_modifiers: List[str]


class ConfigExtension(TypedDict, total=False):
    """
    Type of the configuration object that can be passed to `extend_tailwind_merge`.
    """
    # Static configuration parts (directly override existing config)
    cache_size: int
    prefix: str
    experimental_parse_class_name: Callable[[ExperimentalParseClassNameParam], ParsedClassName]
    separator: str
    
    # Override parts of the configuration
    override: PartialConfigGroupsPart
    
    # Extend parts of the configuration
    extend: PartialConfigGroupsPart


# Type alias for a configuration that allows for any possible configuration
AnyConfig: TypeAlias = Config

# Define the ClassMap type alias
ClassMap: TypeAlias = Dict[str, Any]

# Define the ConflictingClassGroupIds type alias
ConflictingClassGroupIds: TypeAlias = Dict[AnyClassGroupIds, List[AnyClassGroupIds]]
