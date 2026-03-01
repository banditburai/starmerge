from typing import Protocol

from starmerge.lib.parse_class_name import IMPORTANT_MODIFIER
from starmerge.lib.types import AnyClassGroupIds


class ConfigUtils(Protocol):
    def parse_class_name(self, class_name: str) -> ...: ...
    def get_class_group_id(self, class_name: str) -> AnyClassGroupIds | None: ...
    def get_conflicting_class_group_ids(
        self, class_group_id: AnyClassGroupIds, has_postfix_modifier: bool
    ) -> list[AnyClassGroupIds]: ...
    def sort_modifiers(self, modifiers: list[str]) -> list[str]: ...


def merge_class_list(class_list: str, config_utils: ConfigUtils) -> str:
    parse_class_name = config_utils.parse_class_name
    get_class_group_id = config_utils.get_class_group_id
    get_conflicting_class_group_ids = config_utils.get_conflicting_class_group_ids
    sort_modifiers = config_utils.sort_modifiers

    class_groups_in_conflict: set[str] = set()
    result = ""

    for original_class_name in reversed(class_list.split()):
        parsed = parse_class_name(original_class_name)

        if parsed.is_external:
            result = f"{original_class_name} {result}" if result else original_class_name
            continue

        has_postfix_modifier = parsed.maybe_postfix_modifier_position is not None
        base_class_name = parsed.base_class_name

        if has_postfix_modifier:
            class_group_id = get_class_group_id(base_class_name[:parsed.maybe_postfix_modifier_position])
        else:
            class_group_id = get_class_group_id(base_class_name)

        if not class_group_id:
            if not has_postfix_modifier:
                result = f"{original_class_name} {result}" if result else original_class_name
                continue

            class_group_id = get_class_group_id(base_class_name)

            if not class_group_id:
                result = f"{original_class_name} {result}" if result else original_class_name
                continue

            has_postfix_modifier = False

        variant_modifier = ":".join(sort_modifiers(parsed.modifiers)) if parsed.modifiers else ""
        modifier_id = variant_modifier + IMPORTANT_MODIFIER if parsed.has_important_modifier else variant_modifier
        class_id = modifier_id + class_group_id

        if class_id in class_groups_in_conflict:
            continue

        class_groups_in_conflict.add(class_id)

        for conflict_group in get_conflicting_class_group_ids(class_group_id, has_postfix_modifier):
            class_groups_in_conflict.add(modifier_id + conflict_group)

        result = f"{original_class_name} {result}" if result else original_class_name

    return result
