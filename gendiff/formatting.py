def stylish(list_diff, depth=0, inside_removed=False, inside_added=False):
    result = '{'

    for elem in list_diff:
        key, status = elem['key'], elem['status']

        if status == 'removed':
            if 'children' in elem:
                result += '\n' + ' ' * (depth * 4) + f'  - {key}: '
                result += stylish(
                    elem['children'], depth + 1,
                    inside_removed=True,
                    inside_added=False
                )
                result += '\n' + ' ' * (depth * 4 + 4) + '}'
            else:
                if elem['value'] is None:
                    value = 'null'
                else:
                    value = str(elem['value']).lower() if isinstance(elem['value'], bool) else elem['value']
                if inside_removed:
                    result += '\n' + ' ' * (depth * 4 + 4) + f'{key}: {value}'
                else:
                    result += '\n' + ' ' * (depth * 4) + f'  - {key}: {value}'

        elif status == 'added':
            if 'children' in elem:
                result += '\n' + ' ' * (depth * 4) + f'  + {key}: '
                result += stylish(
                    elem['children'], depth + 1,
                    inside_removed=False,
                    inside_added=True
                )
                result += '\n' + ' ' * (depth * 4 + 4) + '}'
            else:
                if elem['value'] is None:
                    value = 'null'
                else:
                    value = str(elem['value']).lower() if isinstance(elem['value'], bool) else elem['value']
                if inside_added:
                    result += '\n' + ' ' * (depth * 4 + 4) + f'{key}: {value}'
                else:
                    result += '\n' + ' ' * (depth * 4) + f'  + {key}: {value}'

        elif status == 'unchanged':
            if 'value' in elem:
                if elem['value'] is None:
                    value = 'null'
                else:
                    value = str(elem['value']).lower() if isinstance(elem['value'], bool) else elem['value']
                result += '\n' + ' ' * (depth * 4 + 4) + f'{key}: {value}'
            elif 'children' in elem:
                result += '\n' + ' ' * (depth * 4 + 4) + key + ': '
                result += stylish(
                    elem['children'], depth + 1,
                    inside_removed, inside_added
                )
                result += '\n' + ' ' * (depth * 4 + 4) + '}'

        elif status == 'changed':
            if elem['old_value'] is None:
                old_value = 'null'
            else:
                old_value = str(elem['old_value']).lower() if isinstance(elem['old_value'], bool) else elem['old_value']
            if elem['new_value'] is None:
                new_value = 'null'
            else:
                new_value = str(elem['new_value']).lower() if isinstance(elem['new_value'], bool) else elem['new_value']
            result += '\n' + ' ' * (depth * 4) + f'  - {key}: {old_value}'
            result += '\n' + ' ' * (depth * 4) + f'  + {key}: {new_value}'

        elif status == 'nested' and 'children' in elem:
            result += '\n' + ' ' * (depth * 4 + 4) + key + ': '
            result += stylish(
                elem['children'], depth + 1,
                inside_removed, inside_added
            )
            result += '\n' + ' ' * (depth * 4 + 4) + '}'

    if depth == 0:
        result += '\n}'
    return result