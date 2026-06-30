def build_diff(file1, file2, path='', inside_removed=False, inside_added=False):
    result = []
    union_keys = sorted(set(file1.keys()) | set(file2.keys()))

    for key in union_keys:
        current_path = path + '.' + key if path else key
        temp_dict = {'key': key}

        if key in file1 and key not in file2:
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

        elif key not in file1 and key in file2:
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

        elif key in file1 and key in file2:
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
                result.append(removed_node)
                result.append(added_node)
                continue
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
                result.append(removed_node)
                result.append(added_node)
                continue
            else:
                if file1[key] == file2[key]:
                    temp_dict['status'] = 'unchanged'
                    temp_dict['value'] = file1[key]
                else:
                    temp_dict['status'] = 'changed'
                    temp_dict['old_value'] = file1[key]
                    temp_dict['new_value'] = file2[key]

        result.append(temp_dict)

    return result