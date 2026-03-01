from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from starmerge.lib.types import (
    AnyClassGroupIds,
    ClassValidator,
    Config,
    ThemeGetter,
)

type ClassGroupGetter = Callable[[str], AnyClassGroupIds | None]
type ConflictGetter = Callable[[AnyClassGroupIds, bool], list[AnyClassGroupIds]]

MAX_RECURSION_DEPTH = 100


@dataclass(frozen=True, slots=True)
class ClassValidatorObject:
    class_group_id: AnyClassGroupIds
    validator: ClassValidator


@dataclass(slots=True)
class ClassPartObject:
    next_part: dict[str, 'ClassPartObject'] = field(default_factory=dict)
    validators: list[ClassValidatorObject] = field(default_factory=list)
    class_group_id: AnyClassGroupIds | None = None


def create_class_group_utils(config: Config) -> tuple[ClassGroupGetter, ConflictGetter]:
    class_map = _create_class_map(config)

    conflicting_class_groups = config.get('conflicting_class_groups', {})
    conflicting_class_group_modifiers = config.get('conflicting_class_group_modifiers', {})

    def get_class_group_id(class_name: str) -> AnyClassGroupIds | None:
        class_parts = class_name.split('-')

        # Leading `-` (e.g. `-inset-1`) produces empty first part
        if class_parts[0] == '' and len(class_parts) > 1:
            class_parts = class_parts[1:]

        return (_get_group_recursive(class_parts, class_map) or
                _get_group_id_for_arbitrary_property(class_name))

    def get_conflicting_class_group_ids(
        class_group_id: AnyClassGroupIds,
        has_postfix_modifier: bool,
    ) -> list[AnyClassGroupIds]:
        conflicts = conflicting_class_groups.get(class_group_id, [])

        if has_postfix_modifier and class_group_id in conflicting_class_group_modifiers:
            return conflicts + conflicting_class_group_modifiers[class_group_id]

        return conflicts

    return get_class_group_id, get_conflicting_class_group_ids


def _get_group_recursive(
    class_parts: list[str],
    class_part_object: ClassPartObject,
    index: int = 0,
) -> AnyClassGroupIds | None:
    if index >= len(class_parts):
        return class_part_object.class_group_id

    current_class_part = class_parts[index]
    if next_obj := class_part_object.next_part.get(current_class_part):
        if group := _get_group_recursive(class_parts, next_obj, index + 1):
            return group

    if not class_part_object.validators:
        return None

    class_rest = '-'.join(class_parts[index:])
    for validator_obj in class_part_object.validators:
        if validator_obj.validator(class_rest):
            return validator_obj.class_group_id

    return None


def _get_group_id_for_arbitrary_property(class_name: str) -> str | None:
    if class_name.startswith('[') and class_name.endswith(']') and len(class_name) > 2:
        inner = class_name[1:-1]
        if ':' in inner:
            # Two dots: one is used as prefix for class groups in plugins
            return f'arbitrary..{inner.split(":", 1)[0]}'
    return None


def _create_class_map(config: Config) -> ClassPartObject:
    theme = config.get('theme', {})
    class_groups = config.get('class_groups', {})
    class_map = ClassPartObject()

    for class_group_id, class_group in class_groups.items():
        _process_classes_recursively(class_group, class_map, class_group_id, theme)

    return class_map


def _process_classes_recursively(
    class_definition: dict | list | ClassValidator | str,
    class_part_object: ClassPartObject,
    class_group_id: AnyClassGroupIds | None = None,
    theme: dict[str, Any] | None = None,
    depth: int = 0,
    visited: set[str] | None = None,
) -> None:
    if depth > MAX_RECURSION_DEPTH:
        return

    if visited is None:
        visited = set()

    if theme is None:
        theme = {}

    match class_definition:
        case str():
            target = (
                class_part_object
                if class_definition == ''
                else _get_part(class_part_object, class_definition, depth + 1, visited)
            )
            target.class_group_id = class_group_id

        case _ if callable(class_definition):
            if _is_theme_getter(class_definition):
                _process_classes_recursively(
                    class_definition(theme),
                    class_part_object,
                    class_group_id,
                    theme,
                    depth + 1,
                    visited,
                )
            else:
                class_part_object.validators.append(
                    ClassValidatorObject(
                        class_group_id=class_group_id,
                        validator=class_definition,
                    )
                )

        case list():
            for sub_def in class_definition:
                _process_classes_recursively(
                    sub_def, class_part_object, class_group_id, theme, depth + 1, visited,
                )

        case dict():
            for key, sub_group in class_definition.items():
                key_visited = visited.copy()
                _process_classes_recursively(
                    sub_group,
                    _get_part(class_part_object, key, depth + 1, key_visited),
                    class_group_id,
                    theme,
                    depth + 1,
                    key_visited,
                )


def _get_part(
    class_part_object: ClassPartObject,
    path: str,
    depth: int = 0,
    visited: set[str] | None = None,
) -> ClassPartObject:
    if depth > MAX_RECURSION_DEPTH:
        raise RecursionError("Maximum recursion depth exceeded in _get_part")

    visited = visited or set()

    if path in visited:
        return class_part_object

    visited.add(path)

    current_object = class_part_object
    for path_part in path.split('-'):
        current_object = current_object.next_part.setdefault(path_part, ClassPartObject())

    return current_object


def _is_theme_getter(func: ClassValidator | ThemeGetter) -> bool:
    return getattr(func, 'is_theme_getter', False)
