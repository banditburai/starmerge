from typing import TypeVar, List, Dict, Union, Optional, Protocol, Callable, Literal, TypedDict, Any

# Generic type variables
GenericClassGroupIds = str
GenericThemeGroupIds = str 

# Basic type definitions
ClassValidator = Callable[[str], bool]


class ThemeGetter(Protocol):
    def __call__(self, theme: Dict[str, List[str]]) -> List[str]: ...
    is_theme_getter: bool = True

# Core type definitions
ClassDefinition = Union[str, ClassValidator, ThemeGetter, Dict[str, List[Any]]]
ClassGroup = List[ClassDefinition]
ThemeObject = Dict[str, ClassGroup]

# Config types
class ConfigStatic(TypedDict, total=False):
    cache_size: int
    prefix: Optional[str]
    separator: str
    experimental_parse_class_name: Optional[Callable[[Dict[str, Any]], Any]]

class ConfigGroups(TypedDict, total=False):
    theme: Dict[str, List[Any]]
    class_groups: Dict[str, List[Any]]
    conflicting_class_groups: Dict[str, List[str]]
    conflicting_class_group_modifiers: Dict[str, List[str]]

class Config(ConfigStatic, ConfigGroups):
    pass

# Internal types used by the implementation
class ClassValidatorObject(TypedDict):
    class_group_id: str
    validator: ClassValidator

class ClassPartObject(TypedDict):
    next_part: Dict[str, 'ClassPartObject']
    validators: List[ClassValidatorObject]
    class_group_id: Optional[str]

class ExperimentalParseClassNameParam(TypedDict):
    """Type of param passed to the experimentalParseClassName function."""
    class_name: str
    parse_class_name: Callable[[str], 'ExperimentalParsedClassName']

class ExperimentalParsedClassName(TypedDict):
    """Result of parsing a class name through experimental parser."""
    modifiers: List[str]
    has_important_modifier: bool
    base_class_name: str
    maybe_postfix_modifier_position: Optional[int]

class ConfigExtension(TypedDict, total=False):
    """Extension config for merging with base config."""
    cache_size: Optional[int]
    prefix: Optional[str]
    separator: Optional[str]
    experimental_parse_class_name: Optional[Callable[[Dict[str, Any]], Any]]
    override: Dict[str, Dict[str, Any]]
    extend: Dict[str, Dict[str, Any]]

# Default theme group IDs (subset shown for brevity)
DefaultThemeGroupIds = Literal[
    'blur',
    'borderColor',
    'borderRadius',
    'borderSpacing',
    'borderWidth',
    'brightness',
    'colors',
    'contrast',
    'gap',
    'gradientColorStopPositions',
    'gradientColorStops',
    'grayscale',
    'hueRotate',
    'inset',
    'invert',
    'margin',
    'opacity',
    'padding',
    'saturate',
    'scale',
    'sepia',
    'skew',
    'space',
    'spacing',
    'translate'
]

DefaultClassGroupIds = Literal[
    'accent',
    'align-content',
    'align-items',
    'align-self',
    'animate',
    'appearance',
    'aspect',
    'auto-cols',
    'auto-rows',
    'backdrop-blur',
    'backdrop-brightness',
    'backdrop-contrast',
    'backdrop-filter',
    'backdrop-grayscale',
    'backdrop-hue-rotate',
    'backdrop-invert',
    'backdrop-opacity',
    'backdrop-saturate',
    'backdrop-sepia',
    'basis',
    'bg-attachment',
    'bg-blend',
    'bg-clip',
    'bg-color',
    'bg-image',
    'bg-opacity',
    'bg-origin',
    'bg-position',
    'bg-repeat',
    'bg-size',
    'blur',
    'border-collapse',
    'border-color-b',
    'border-color-e',
    'border-color-l',
    'border-color-r',
    'border-color-s',
    'border-color-t',
    'border-color-x',
    'border-color-y',
    'border-color',
    'border-opacity',
    'border-spacing-x',
    'border-spacing-y',
    'border-spacing',
    'border-style',
    'border-w-b',
    'border-w-e',
    'border-w-l',
    'border-w-r',
    'border-w-s',
    'border-w-t',
    'border-w-x',
    'border-w-y',
    'border-w',
    'bottom',
    'box-decoration',
    'box',
    'break-after',
    'break-before',
    'break-inside',
    'break',
    'brightness',
    'caption',
    'caret-color',
    'clear',
    'col-end',
    'col-start-end',
    'col-start',
    'columns',
    'container',
    'content',
    'contrast',
    'cursor',
    'delay',
    'display',
    'divide-color',
    'divide-opacity',
    'divide-style',
    'divide-x-reverse',
    'divide-x',
    'divide-y-reverse',
    'divide-y',
    'drop-shadow',
    'duration',
    'ease',
    'end',
    'fill',
    'filter',
    'flex-direction',
    'flex-wrap',
    'flex',
    'float',
    'font-family',
    'font-size',
    'font-smoothing',
    'font-style',
    'font-weight',
    'forced-color-adjust',
    'fvn-figure',
    'fvn-fraction',
    'fvn-normal',
    'fvn-ordinal',
    'fvn-slashed-zero',
    'fvn-spacing',
    'gap-x',
    'gap-y',
    'gap',
    'gradient-from-pos',
    'gradient-from',
    'gradient-to-pos',
    'gradient-to',
    'gradient-via-pos',
    'gradient-via',
    'grayscale',
    'grid-cols',
    'grid-flow',
    'grid-rows',
    'grow',
    'h',
    'hue-rotate',
    'hyphens',
    'indent',
    'inset-x',
    'inset-y',
    'inset',
    'invert',
    'isolation',
    'justify-content',
    'justify-items',
    'justify-self',
    'leading',
    'left',
    'line-clamp',
    'list-image',
    'list-style-position',
    'list-style-type',
    'm',
    'mb',
    'me',
    'min-h',
    'min-w',
    'mix-blend',
    'ml',
    'mr',
    'ms',
    'mt',
    'mx',
    'my',
    'object-fit',
    'object-position',
    'opacity',
    'order',
    'outline-color',
    'outline-offset',
    'outline-style',
    'outline-w',
    'overflow-x',
    'overflow-y',
    'overflow',
    'overscroll-x',
    'overscroll-y',
    'overscroll',
    'p',
    'pb',
    'pe',
    'pl',
    'place-content',
    'place-items',
    'place-self',
    'placeholder-color',
    'placeholder-opacity',
    'pointer-events',
    'position',
    'pr',
    'ps',
    'pt',
    'px',
    'py',
    'resize',
    'right',
    'ring-color',
    'ring-offset-color',
    'ring-offset-w',
    'ring-opacity',
    'ring-w-inset',
    'ring-w',
    'rotate',
    'rounded-b',
    'rounded-bl',
    'rounded-br',
    'rounded-e',
    'rounded-ee',
    'rounded-es',
    'rounded-l',
    'rounded-r',
    'rounded-s',
    'rounded-se',
    'rounded-ss',
    'rounded-t',
    'rounded-tl',
    'rounded-tr',
    'rounded',
    'row-end',
    'row-start-end',
    'row-start',
    'saturate',
    'scale-x',
    'scale-y',
    'scale',
    'scroll-behavior',
    'scroll-m',
    'scroll-mb',
    'scroll-me',
    'scroll-ml',
    'scroll-mr',
    'scroll-ms',
    'scroll-mt',
    'scroll-mx',
    'scroll-my',
    'scroll-p',
    'scroll-pb',
    'scroll-pe',
    'scroll-pl',
    'scroll-pr',
    'scroll-ps',
    'scroll-pt',
    'scroll-px',
    'scroll-py',
    'select',
    'sepia',
    'shadow-color',
    'shadow',
    'shrink',
    'size',
    'skew-x',
    'skew-y',
    'snap-align',
    'snap-stop',
    'snap-strictness',
    'snap-type',
    'space-x-reverse',
    'space-x',
    'space-y-reverse',
    'space-y',
    'sr',
    'start',
    'stroke-w',
    'stroke',
    'table-layout',
    'text-alignment',
    'text-color',
    'text-decoration-color',
    'text-decoration-style',
    'text-decoration-thickness',
    'text-decoration',
    'text-opacity',
    'text-overflow',
    'text-transform',
    'text-wrap',
    'top',
    'touch-pz',
    'touch-x',
    'touch-y',
    'touch',
    'tracking',
    'transform-origin',
    'transform',
    'transition',
    'translate-x',
    'translate-y',
    'underline-offset',
    'vertical-align',
    'visibility',
    'w',
    'whitespace',
    'will-change',
    'z'
]

GenericConfig = Dict[str, Any]

__all__ = [
    'ClassValidator',
    'ClassDefinition',
    'ClassGroup',
    'ThemeObject',
    'Config',
    'ConfigExtension',  # Added this
    'ClassValidatorObject',
    'ClassPartObject',
    'ExperimentalParseClassNameParam',
    'ExperimentalParsedClassName'
]