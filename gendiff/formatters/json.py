def json_format(list_diff):
    result = []

    for elem in list_diff:
        status = elem['status']

        if status == 'nested' and 'children' in elem:
            result.append(
                {
                    'key': elem['key'],
                    'status': elem['status'],
                    'children': json_format(elem['children'])
                }
            )
        
        elif (
            status == 'added'
            or status == 'removed'
            or status == 'unchanged'
            or status == 'changed'
        ):
            result.append(elem)
    
    return result