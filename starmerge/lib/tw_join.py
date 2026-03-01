type ClassNameValue = list['ClassNameValue'] | str | None | bool | int


def tw_join(*class_lists: ClassNameValue) -> str:
    result = []
    for argument in class_lists:
        if argument:
            value = _to_value(argument)
            if value:
                result.append(value)
    return ' '.join(result)


def _to_value(mix: ClassNameValue) -> str:
    if isinstance(mix, str):
        return mix
    if not isinstance(mix, list):
        return ''
    result = []
    for item in mix:
        if not item:
            continue
        if isinstance(item, list):
            value = _to_value(item)
        elif isinstance(item, str):
            value = item
        else:
            value = str(item)
        if value:
            result.append(value)
    return ' '.join(result)
