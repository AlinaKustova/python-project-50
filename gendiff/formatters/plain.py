def plain(data, path=''):
    result = []

    for elem in data:
        key, status = elem['key'], elem['status']
        current_path = path + '.' + key if path else key

        if status == 'added':
            if 'children' in elem:
                result.append(format_added('children', current_path))
            else:
                result.append(format_added(elem['value'], current_path))
        
        elif status == 'removed':
            result.append(format_removed(current_path))
        
        elif status == 'changed':
            result.append(
                format_changed(
                    elem['old_value'],
                    elem['new_value'],
                    current_path
                )
            )
        
        elif status == 'nested':
            result.extend(plain(elem['children'], current_path))

    return merge(result)
            

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


def format_removed(path):
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


def merge(result):
    merged = []
    i = 0
    while i < len(result):
        line = result[i]
        
        if i + 1 < len(result):
            next_line = result[i + 1]
            
            if 'removed' in line and 'added' in next_line:
                path1 = line[
                    line.find("'") + 1:
                    line.find("'", line.find("'") + 1)
                ]
                path2 = next_line[
                    next_line.find("'") + 1:
                    next_line.find("'", next_line.find("'") + 1)
                ]
                
                if path1 == path2:
                    value_start = next_line.find(": ") + 2
                    new_value = next_line[value_start:]
                    merged.append(
                        f"Property '{path1}' was updated. "
                        f"From [complex value] to {new_value}"
                    )
                    i += 2
                    continue
        
        merged.append(line)
        i += 1
    
    return merged