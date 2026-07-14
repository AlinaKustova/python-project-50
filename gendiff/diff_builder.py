def build_diff(file1, file2, path='', inside_removed=False, inside_added=False):
    result = []
    union_keys = sorted(set(file1.keys()) | set(file2.keys()))

    for key in union_keys:
        current_path = path + '.' + key if path else key
        temp_dict = {'key': key}

        if key in file1 and key not in file2:
            temp_dict = process_removed_key(
                file1, key, current_path, inside_removed
            )
        elif key not in file1 and key in file2:
            temp_dict = process_added_key(
                file2, key, current_path, inside_added
            )
        elif key in file1 and key in file2:
            temp_dict, extra_nodes = process_common_key(
                file1, file2, key, current_path, inside_removed, inside_added
            )
            if extra_nodes:
                result.extend(extra_nodes)
                continue

        result.append(temp_dict)

    return result


def process_removed_key(file1, key, current_path, inside_removed):
    temp_dict = {'key': key}
    
    if inside_removed:
        if isinstance(file1[key], dict):
            temp_dict['status'] = 'unchanged'
            temp_dict['children'] = build_diff(
                file1[key], {}, current_path,
                inside_removed=True,
                inside_added=False
            )
        else:
            temp_dict['status'] = 'unchanged'
            temp_dict['value'] = file1[key]
    elif isinstance(file1[key], dict):
        temp_dict['status'] = 'removed'
        temp_dict['children'] = build_diff(
            file1[key], {}, current_path,
            inside_removed=True,
            inside_added=False
        )
    else:
        temp_dict['status'] = 'removed'
        temp_dict['value'] = file1[key]
    
    return temp_dict


def process_added_key(file2, key, current_path, inside_added):
    temp_dict = {'key': key}
    
    if inside_added:
        if isinstance(file2[key], dict):
            temp_dict['status'] = 'unchanged'
            temp_dict['children'] = build_diff(
                {}, file2[key], current_path,
                inside_removed=False,
                inside_added=True
            )
        else:
            temp_dict['status'] = 'unchanged'
            temp_dict['value'] = file2[key]
    elif isinstance(file2[key], dict):
        temp_dict['status'] = 'added'
        temp_dict['children'] = build_diff(
            {}, file2[key], current_path,
            inside_removed=False,
            inside_added=True
        )
    else:
        temp_dict['status'] = 'added'
        temp_dict['value'] = file2[key]
    
    return temp_dict


def process_common_key(
        file1, file2, key, current_path,
        inside_removed, inside_added):
    temp_dict = {'key': key}
    extra_nodes = []

    if isinstance(file1[key], dict) and isinstance(file2[key], dict):
        temp_dict['status'] = 'nested'
        temp_dict['children'] = build_diff(
            file1[key], file2[key], current_path,
            inside_removed, inside_added
        )
    elif isinstance(file1[key], dict) and not isinstance(file2[key], dict):
        removed_node = {
            'key': key,
            'status': 'removed',
            'children': build_diff(
                file1[key], {}, current_path,
                inside_removed=True,
                inside_added=False
            )
        }
        added_node = {
            'key': key,
            'status': 'added',
            'value': file2[key]
        }
        extra_nodes = [removed_node, added_node]
    elif not isinstance(file1[key], dict) and isinstance(file2[key], dict):
        removed_node = {
            'key': key,
            'status': 'removed',
            'value': file1[key]
        }
        added_node = {
            'key': key,
            'status': 'added',
            'children': build_diff(
                {}, file2[key], current_path,
                inside_removed=False,
                inside_added=True
            )
        }
        extra_nodes = [removed_node, added_node]
    else:
        if file1[key] == file2[key]:
            temp_dict['status'] = 'unchanged'
            temp_dict['value'] = file1[key]
        else:
            temp_dict['status'] = 'changed'
            temp_dict['old_value'] = file1[key]
            temp_dict['new_value'] = file2[key]

    return temp_dict, extra_nodes