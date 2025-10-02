"""Parser for Tailwind CSS class names into their component parts."""

from typing import Callable, Optional, Protocol

from starmerge.lib.types import AnyConfig, ParsedClassName, ExperimentalParseClassNameParam

IMPORTANT_MODIFIER = '!'
MODIFIER_SEPARATOR = ':'
MODIFIER_SEPARATOR_LENGTH = len(MODIFIER_SEPARATOR)


def create_parse_class_name(config: AnyConfig) -> Callable[[str], ParsedClassName]:
    prefix = config.get('prefix')
    experimental_parse_class_name = config.get('experimental_parse_class_name')

    def parse_class_name(class_name: str) -> ParsedClassName:
        """
        Parse class name into parts.
        Inspired by splitAtTopLevelOnly from Tailwind CSS.
        https://github.com/tailwindlabs/tailwindcss/blob/v3.2.2/src/util/splitAtTopLevelOnly.js
        """
        modifiers = []
        
        bracket_depth = 0
        paren_depth = 0
        modifier_start = 0
        postfix_modifier_position: Optional[int] = None
        
        for index, current_character in enumerate(class_name):
            if bracket_depth == 0 and paren_depth == 0:
                if current_character == MODIFIER_SEPARATOR:
                    modifiers.append(class_name[modifier_start:index])
                    modifier_start = index + MODIFIER_SEPARATOR_LENGTH
                    continue
                
                if current_character == '/':
                    postfix_modifier_position = index
                    continue
            
            if current_character == '[':
                bracket_depth += 1
            elif current_character == ']':
                bracket_depth -= 1
            elif current_character == '(':
                paren_depth += 1
            elif current_character == ')':
                paren_depth -= 1
        
        base_class_name_with_important_modifier = (
            class_name if len(modifiers) == 0 else class_name[modifier_start:]
        )
        base_class_name = strip_important_modifier(base_class_name_with_important_modifier)
        has_important_modifier = base_class_name != base_class_name_with_important_modifier
        maybe_postfix_modifier_position = (
            postfix_modifier_position - modifier_start 
            if postfix_modifier_position is not None and postfix_modifier_position > modifier_start
            else None
        )
        
        return ParsedClassName(
            modifiers=modifiers,
            has_important_modifier=has_important_modifier,
            base_class_name=base_class_name,
            maybe_postfix_modifier_position=maybe_postfix_modifier_position,
        )

    if prefix:
        full_prefix = prefix + MODIFIER_SEPARATOR
        parse_class_name_original = parse_class_name
        
        def parse_class_name_with_prefix(class_name: str) -> ParsedClassName:
            if class_name.startswith(full_prefix):
                return parse_class_name_original(class_name[len(full_prefix):])
            return ParsedClassName(
                modifiers=[],
                has_important_modifier=False,
                base_class_name=class_name,
                maybe_postfix_modifier_position=None,
                is_external=True,
            )

        parse_class_name = parse_class_name_with_prefix

    if experimental_parse_class_name:
        parse_class_name_original = parse_class_name
        
        def parse_class_name_experimental(class_name: str) -> ParsedClassName:
            param = ExperimentalParseClassNameParam(
                class_name=class_name,
                parse_class_name=parse_class_name_original,
            )
            return experimental_parse_class_name(param)

        parse_class_name = parse_class_name_experimental

    return parse_class_name


def strip_important_modifier(base_class_name: str) -> str:
    """Strip the important modifier (!) from class name (can be at start or end)."""
    if base_class_name.endswith(IMPORTANT_MODIFIER):
        return base_class_name[:-1]

    # Tailwind CSS v3 compatibility: important modifier at start
    # https://github.com/dcastil/tailwind-merge/issues/513#issuecomment-2614029864
    if base_class_name.startswith(IMPORTANT_MODIFIER):
        return base_class_name[1:]

    return base_class_name
