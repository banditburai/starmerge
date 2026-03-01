from collections.abc import Callable

from starmerge.lib.types import AnyConfig, ParsedClassName, ExperimentalParseClassNameParam

IMPORTANT_MODIFIER = '!'
MODIFIER_SEPARATOR = ':'


def create_parse_class_name(config: AnyConfig) -> Callable[[str], ParsedClassName]:
    prefix = config.get('prefix')
    experimental_parse_class_name = config.get('experimental_parse_class_name')

    def parse_class_name(class_name: str) -> ParsedClassName:
        modifiers = []
        _sep = MODIFIER_SEPARATOR

        bracket_depth = 0
        paren_depth = 0
        modifier_start = 0
        postfix_modifier_position: int | None = None

        for index, char in enumerate(class_name):
            if bracket_depth == 0 and paren_depth == 0:
                if char == _sep:
                    modifiers.append(class_name[modifier_start:index])
                    modifier_start = index + 1
                    continue

                if char == '/':
                    postfix_modifier_position = index
                    continue

            if char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1
            elif char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1

        base_with_important = (
            class_name if not modifiers else class_name[modifier_start:]
        )
        base_class_name = strip_important_modifier(base_with_important)
        has_important_modifier = base_class_name != base_with_important
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
    if base_class_name.endswith(IMPORTANT_MODIFIER):
        return base_class_name[:-1]
    # Tailwind CSS v3 compat: important modifier at start
    if base_class_name.startswith(IMPORTANT_MODIFIER):
        return base_class_name[1:]
    return base_class_name
