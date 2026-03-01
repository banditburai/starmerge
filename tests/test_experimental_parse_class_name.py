from typing import Any

from starmerge import extend_tailwind_merge


def test_default_case():
    def parse_class_name_fn(args: dict[str, Any]) -> Any:
        class_name = args["class_name"]
        parse_class_name = args["parse_class_name"]
        return parse_class_name(class_name)

    tw_merge = extend_tailwind_merge(
        {"experimental_parse_class_name": parse_class_name_fn}
    )

    assert tw_merge("px-2 py-1 p-3") == "p-3"


def test_removing_first_three_characters_from_class():
    def parse_class_name_fn(args: dict[str, Any]) -> Any:
        class_name = args["class_name"]
        parse_class_name = args["parse_class_name"]
        return parse_class_name(class_name[3:])

    tw_merge = extend_tailwind_merge(
        {"experimental_parse_class_name": parse_class_name_fn}
    )

    assert tw_merge("barpx-2 foopy-1 lolp-3") == "lolp-3"


def test_ignoring_breakpoint_modifiers():
    breakpoints = {"sm", "md", "lg", "xl", "2xl"}

    def parse_class_name_fn(args: dict[str, Any]) -> Any:
        class_name = args["class_name"]
        parse_class_name = args["parse_class_name"]
        parsed = parse_class_name(class_name)

        filtered_modifiers = [
            modifier for modifier in parsed.modifiers if modifier not in breakpoints
        ]

        from starmerge.lib.types import ParsedClassName

        return ParsedClassName(
            modifiers=filtered_modifiers,
            has_important_modifier=parsed.has_important_modifier,
            base_class_name=parsed.base_class_name,
            maybe_postfix_modifier_position=parsed.maybe_postfix_modifier_position,
            is_external=parsed.is_external,
        )

    tw_merge = extend_tailwind_merge(
        {"experimental_parse_class_name": parse_class_name_fn}
    )

    assert tw_merge("md:px-2 hover:py-4 py-1 lg:p-3") == "hover:py-4 lg:p-3"
