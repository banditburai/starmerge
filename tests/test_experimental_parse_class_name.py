"""
Python equivalent of js-source/experimental-parse-class-name.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the experimental parse class name feature.
"""

import pytest
from tw_merge import extend_tailwind_merge
from typing import Dict, Any


def test_default_case():
    """Test the default case of experimentalParseClassName."""
    def parse_class_name_fn(args: Dict[str, Any]) -> Any:
        class_name = args["class_name"]
        parse_class_name = args["parse_class_name"]
        return parse_class_name(class_name)
    
    tw_merge = extend_tailwind_merge({
        "experimental_parse_class_name": parse_class_name_fn
    })
    
    assert tw_merge('px-2 py-1 p-3') == 'p-3'


def test_removing_first_three_characters_from_class():
    """Test removing first three characters from class using experimentalParseClassName."""
    def parse_class_name_fn(args: Dict[str, Any]) -> Any:
        class_name = args["class_name"]
        parse_class_name = args["parse_class_name"]
        return parse_class_name(class_name[3:])
    
    tw_merge = extend_tailwind_merge({
        "experimental_parse_class_name": parse_class_name_fn
    })
    
    assert tw_merge('barpx-2 foopy-1 lolp-3') == 'lolp-3'


def test_ignoring_breakpoint_modifiers():
    """Test ignoring breakpoint modifiers using experimentalParseClassName."""
    breakpoints = {'sm', 'md', 'lg', 'xl', '2xl'}
    
    def parse_class_name_fn(args: Dict[str, Any]) -> Any:
        class_name = args["class_name"]
        parse_class_name = args["parse_class_name"]
        parsed = parse_class_name(class_name)
        
        # Filter out breakpoint modifiers
        filtered_modifiers = [
            modifier for modifier in parsed.modifiers
            if modifier not in breakpoints
        ]
        
        # Create a new ParsedClassName with filtered modifiers and all other attributes preserved
        from tw_merge.lib.types import ParsedClassName
        return ParsedClassName(
            modifiers=filtered_modifiers,
            has_important_modifier=parsed.has_important_modifier,
            base_class_name=parsed.base_class_name,
            maybe_postfix_modifier_position=parsed.maybe_postfix_modifier_position,
            is_external=parsed.is_external
        )
    
    tw_merge = extend_tailwind_merge({
        "experimental_parse_class_name": parse_class_name_fn
    })
    
    assert tw_merge('md:px-2 hover:py-4 py-1 lg:p-3') == 'hover:py-4 lg:p-3' 