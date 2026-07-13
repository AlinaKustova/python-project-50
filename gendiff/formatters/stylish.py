def stylish(list_diff, depth=0, inside_removed=False, inside_added=False):
    result = '{'

    for elem in list_diff:
        status = elem['status']

        if status == 'removed':
            result += format_removed(elem, depth, inside_removed)
        elif status == 'added':
            result += format_added(elem, depth, inside_added)
        elif status == 'unchanged':
            result += format_unchanged(
                elem, depth, inside_removed, inside_added
                )
        elif status == 'changed':
            result += format_changed(elem, depth)
        elif status == 'nested' and 'children' in elem:
            result += format_nested(elem, depth, inside_removed, inside_added)

    if depth == 0:
        result += '\n}'
    return result


def format_removed(elem, depth, inside_removed):
    key = elem['key']
    if 'children' in elem:
        result = '\n' + ' ' * (depth * 4) + f'  - {key}: '
        result += stylish(
            elem['children'], depth + 1,
            inside_removed=True,
            inside_added=False
        )
        result += '\n' + ' ' * (depth * 4 + 4) + '}'
    else:
        value = format_value(elem['value'])
        if inside_removed:
            result = '\n' + ' ' * (depth * 4 + 4) + f'{key}: {value}'
        else:
            result = '\n' + ' ' * (depth * 4) + f'  - {key}: {value}'
    return result


def format_added(elem, depth, inside_added):
    key = elem['key']
    if 'children' in elem:
        result = '\n' + ' ' * (depth * 4) + f'  + {key}: '
        result += stylish(
            elem['children'], depth + 1,
            inside_removed=False,
            inside_added=True
        )
        result += '\n' + ' ' * (depth * 4 + 4) + '}'
    else:
        value = format_value(elem['value'])
        if inside_added:
            result = '\n' + ' ' * (depth * 4 + 4) + f'{key}: {value}'
        else:
            result = '\n' + ' ' * (depth * 4) + f'  + {key}: {value}'
    return result


def format_unchanged(elem, depth, inside_removed, inside_added):
    key = elem['key']
    if 'value' in elem:
        value = format_value(elem['value'])
        return '\n' + ' ' * (depth * 4 + 4) + f'{key}: {value}'
    elif 'children' in elem:
        result = '\n' + ' ' * (depth * 4 + 4) + key + ': '
        result += stylish(
            elem['children'], depth + 1,
            inside_removed, inside_added
        )
        result += '\n' + ' ' * (depth * 4 + 4) + '}'
        return result
    return ''


def format_changed(elem, depth):
    key = elem['key']
    old_value = format_value(elem['old_value'])
    new_value = format_value(elem['new_value'])
    result = '\n' + ' ' * (depth * 4) + f'  - {key}: {old_value}'
    result += '\n' + ' ' * (depth * 4) + f'  + {key}: {new_value}'
    return result


def format_nested(elem, depth, inside_removed, inside_added):
    key = elem['key']
    result = '\n' + ' ' * (depth * 4 + 4) + key + ': '
    result += stylish(
        elem['children'], depth + 1,
        inside_removed, inside_added
    )
    result += '\n' + ' ' * (depth * 4 + 4) + '}'
    return result


def format_value(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    return value