def plain(data, path=''):
    result = []
    i = 0
    while i < len(data):
        elem = data[i]
        key = elem['key']
        status = elem['status']
        current_path = path + '.' + key if path else key

        if status == 'added':
            if 'children' in elem:
                result.append(format_added('children', current_path))
            else:
                result.append(format_added(elem['value'], current_path))
            i += 1
        elif status == 'removed':
            merged = merge_removed_added(data, i, current_path)
            if merged is not None:
                result.append(merged)
                i += 2
            else:
                result.append(format_removed(current_path))
                i += 1
        elif status == 'changed':
            result.append(format_changed(
                elem['old_value'], elem['new_value'], current_path
            ))
            i += 1
        elif status == 'nested':
            result.extend(plain(elem['children'], current_path))
            i += 1
        else:
            i += 1

    return result


def merge_removed_added(data, i, current_path):
    """Пытается объединить removed + added в одну строку updated."""
    if i + 1 >= len(data):
        return None
    next_elem = data[i + 1]
    if next_elem['status'] != 'added' or next_elem['key'] != data[i]['key']:
        return None

    removed = data[i]
    added = next_elem
    old_complex = 'children' in removed
    new_complex = 'children' in added

    if old_complex:
        old_str = '[complex value]'
    else:
        old_str = format_simple_value(removed.get('value'))

    if new_complex:
        new_str = '[complex value]'
    else:
        new_str = format_simple_value(added.get('value'))

    return (f"Property '{current_path}' was updated. "
            f"From {old_str} to {new_str}")


def format_simple_value(value):
    """Форматирует простое значение с кавычками для строк (кроме спец. слов)."""
    formatted = format_value(value)
    if isinstance(formatted, str) and formatted not in (
        'true', 'false', 'null', "''"
    ):
        return f"'{formatted}'"
    return formatted


def format_added(value, path):
    if value == 'children':
        return f"Property '{path}' was added with value: [complex value]"
    else:
        value = format_value(value)
    
    if (
        isinstance(value, str)
        and value != 'true'
        and value != 'false'
        and value != 'null'
    ):
        return f"Property '{path}' was added with value: '{value}'"
    
    return f"Property '{path}' was added with value: {value}"


def format_removed(path, is_complex=False):
    if is_complex:
        return f"Property '{path}' was removed with value: [complex value]"
    return f"Property '{path}' was removed"


def format_changed(old_value, new_value, path):
    if isinstance(old_value, dict):
        old_value = '[complex value]'
    else:
        old_value = format_value(old_value)
    
    if isinstance(new_value, dict):
        new_value = '[complex value]'
    else:
        new_value = format_value(new_value)
    
    if (
        isinstance(old_value, str)
        and old_value not in ('true', 'false', 'null', '[complex value]', "''")
    ):
        old_value = f"'{old_value}'"
    
    if (
        isinstance(new_value, str)
        and new_value not in ('true', 'false', 'null', '[complex value]', "''")
    ):
        new_value = f"'{new_value}'"
    
    return (f"Property '{path}' was updated. "
            f"From {old_value} to {new_value}")


def format_value(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str) and value == '':
        return "''"
    return value