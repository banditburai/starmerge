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

from .generated_types import DefaultThemeGroupIds, DefaultClassGroupIds

AnyClassGroupIds = str
AnyThemeGroupIds = str

ClassGroupIds = TypeVar('ClassGroupIds', bound=str)
ThemeGroupIds = TypeVar('ThemeGroupIds', bound=str)

ClassValidator: TypeAlias = Callable[[str], bool]
TailwindMerge: TypeAlias = Callable[[str], str]

ClassGroup: TypeAlias = List["ClassDefinition"]
ClassObject: TypeAlias = Dict[str, "ClassGroup"]
ThemeObject: TypeAlias = Dict[str, "ClassGroup"]


class ThemeGetter(Protocol):
    """Theme getter function type."""
    isThemeGetter: bool
    def __call__(self, theme: ThemeObject) -> ClassGroup: ...


ClassDefinition: TypeAlias = Union[str, ClassValidator, ThemeGetter, ClassObject]

@dataclass
class ParsedClassName:
    """Result returned by parse_class_name. Experimental feature."""
    modifiers: List[str]
    has_important_modifier: bool
    base_class_name: str
    maybe_postfix_modifier_position: Optional[int] = None
    is_external: bool = False

    def __getitem__(self, key):
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
    """Param passed to experimental_parse_class_name. Experimental feature."""
    class_name: str
    parse_class_name: Callable[[str], ParsedClassName]


class ConfigStaticPart(TypedDict):
    """Static part of tailwind-merge configuration (always overridden when merging)."""
    cache_size: int
    prefix: NotRequired[str]
    experimental_parse_class_name: NotRequired[Callable[[ExperimentalParseClassNameParam], ParsedClassName]]
    separator: NotRequired[str]


class ConfigGroupsPart(TypedDict):
    """Dynamic part of tailwind-merge configuration (can be extended or overridden)."""
    theme: ThemeObject
    class_groups: Dict[str, ClassGroup]
    conflicting_class_groups: NotRequired[Dict[str, List[str]]]
    conflicting_class_group_modifiers: NotRequired[Dict[str, List[str]]]
    order_sensitive_modifiers: NotRequired[List[str]]


class Config(ConfigStaticPart, ConfigGroupsPart):
    """Type the tailwind-merge configuration adheres to."""
    pass


class PartialConfigGroupsPart(TypedDict, total=False):
    """Partial version of ConfigGroupsPart for extensions."""
    theme: ThemeObject
    class_groups: Dict[str, ClassGroup]
    conflicting_class_groups: Dict[str, List[str]]
    conflicting_class_group_modifiers: Dict[str, List[str]]
    order_sensitive_modifiers: List[str]


class ConfigExtension(TypedDict, total=False):
    """Configuration object that can be passed to extend_tailwind_merge."""
    cache_size: int
    prefix: str
    experimental_parse_class_name: Callable[[ExperimentalParseClassNameParam], ParsedClassName]
    separator: str
    override: PartialConfigGroupsPart
    extend: PartialConfigGroupsPart


AnyConfig: TypeAlias = Config
ClassMap: TypeAlias = Dict[str, Any]
ConflictingClassGroupIds: TypeAlias = Dict[AnyClassGroupIds, List[AnyClassGroupIds]]
