from dataclasses import dataclass
from typing import List, Optional, Callable, Dict, Any

from .types import GenericConfig, ExperimentalParsedClassName

IMPORTANT_MODIFIER = '!'

@dataclass
class ParsedClassName:
    """Result of parsing a Tailwind CSS class name."""
    modifiers: List[str]
    has_important_modifier: bool
    base_class_name: str
    maybe_postfix_modifier_position: Optional[int]

def create_parse_class_name(config: GenericConfig) -> Callable[[str], ParsedClassName]:
    """Creates a function that parses Tailwind CSS class names."""
    separator = config['separator']
    experimental_parse_class_name = config.get('experimental_parse_class_name')
    is_separator_single_character = len(separator) == 1
    first_separator_character = separator[0]
    separator_length = len(separator)

    def parse_class_name(class_name: str) -> ParsedClassName:
        modifiers: List[str] = []
        bracket_depth = 0
        modifier_start = 0
        postfix_modifier_position: Optional[int] = None

        for index in range(len(class_name)):
            current_character = class_name[index]

            if bracket_depth == 0:
                if (current_character == first_separator_character and 
                    (is_separator_single_character or 
                     class_name[index:index + separator_length] == separator)):
                    modifiers.append(class_name[modifier_start:index])
                    modifier_start = index + separator_length
                    continue

                if current_character == '/':
                    postfix_modifier_position = index
                    continue

            if current_character == '[':
                bracket_depth += 1
            elif current_character == ']':
                bracket_depth -= 1

        base_class_name_with_important = (
            class_name if not modifiers 
            else class_name[modifier_start:]
        )
        
        has_important_modifier = base_class_name_with_important.startswith(IMPORTANT_MODIFIER)
        base_class_name = (
            base_class_name_with_important[1:] if has_important_modifier 
            else base_class_name_with_important
        )

        maybe_postfix_modifier_position = (
            postfix_modifier_position - modifier_start
            if postfix_modifier_position is not None and postfix_modifier_position > modifier_start
            else None
        )

        return ParsedClassName(
            modifiers=modifiers,
            has_important_modifier=has_important_modifier,
            base_class_name=base_class_name,
            maybe_postfix_modifier_position=maybe_postfix_modifier_position
        )

    if experimental_parse_class_name:
        def wrapped_parse(class_name: str) -> ParsedClassName:
            return experimental_parse_class_name({
                'className': class_name,  # Note: using camelCase to match TS
                'parseClassName': parse_class_name
            })
        return wrapped_parse

    return parse_class_name

def sort_modifiers(modifiers: List[str]) -> List[str]:
    """Sort modifiers preserving arbitrary variants position."""
    if len(modifiers) <= 1:
        return modifiers

    sorted_modifiers: List[str] = []
    unsorted_modifiers: List[str] = []

    for modifier in modifiers:
        if modifier.startswith('['):
            sorted_modifiers.extend(sorted(unsorted_modifiers))
            sorted_modifiers.append(modifier)
            unsorted_modifiers = []
        else:
            unsorted_modifiers.append(modifier)

    sorted_modifiers.extend(sorted(unsorted_modifiers))
    return sorted_modifiers