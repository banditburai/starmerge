from collections.abc import Callable
from dataclasses import dataclass
from typing import NotRequired, Protocol, TypedDict

type AnyClassGroupIds = str
type AnyThemeGroupIds = str

type ClassValidator = Callable[[str], bool]
type TailwindMerge = Callable[..., str]

type ClassGroup = list[ClassDefinition]
type ClassObject = dict[str, ClassGroup]
type ThemeObject = dict[str, ClassGroup]


class ThemeGetter(Protocol):
    is_theme_getter: bool

    def __call__(self, theme: ThemeObject) -> ClassGroup: ...


type ClassDefinition = str | ClassValidator | ThemeGetter | ClassObject


@dataclass(slots=True)
class ParsedClassName:
    modifiers: list[str]
    has_important_modifier: bool
    base_class_name: str
    maybe_postfix_modifier_position: int | None = None
    is_external: bool = False


class ExperimentalParseClassNameParam(TypedDict):
    class_name: str
    parse_class_name: Callable[[str], ParsedClassName]


class ConfigStaticPart(TypedDict):
    cache_size: int
    prefix: NotRequired[str]
    experimental_parse_class_name: NotRequired[
        Callable[[ExperimentalParseClassNameParam], ParsedClassName]
    ]
    separator: NotRequired[str]


class ConfigGroupsPart(TypedDict):
    theme: ThemeObject
    class_groups: dict[str, ClassGroup]
    conflicting_class_groups: NotRequired[dict[str, list[str]]]
    conflicting_class_group_modifiers: NotRequired[dict[str, list[str]]]
    order_sensitive_modifiers: NotRequired[list[str]]


class Config(ConfigStaticPart, ConfigGroupsPart): ...


class PartialConfigGroupsPart(TypedDict, total=False):
    theme: ThemeObject
    class_groups: dict[str, ClassGroup]
    conflicting_class_groups: dict[str, list[str]]
    conflicting_class_group_modifiers: dict[str, list[str]]
    order_sensitive_modifiers: list[str]


class ConfigExtension(TypedDict, total=False):
    cache_size: int
    prefix: str
    experimental_parse_class_name: Callable[
        [ExperimentalParseClassNameParam], ParsedClassName
    ]
    separator: str
    override: PartialConfigGroupsPart
    extend: PartialConfigGroupsPart


type AnyConfig = Config
