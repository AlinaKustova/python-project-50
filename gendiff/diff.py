from gendiff.parser import read_file


def generate_diff(path1, path2):
    file1 = read_file(path1)
    file2 = read_file(path2)

    diff = '{'

    union_keys = sorted(set(file1.keys()) | set(file2.keys()))

    for key in union_keys:
        if key in file1 and key in file2:
            value1, value2 = file1[key], file2[key]
            if value1 == value2:
                diff += f'\n    {key}: {str(value1).lower()}'
            else:
                diff += f'\n  - {key}: {str(value1).lower()}'
                diff += f'\n  + {key}: {str(value2).lower()}'
        elif key in file1 and key not in file2:
            value1 = file1[key]
            diff += f'\n  - {key}: {str(value1).lower()}'
        elif key in file2 and key not in file1:
            value2 = file2[key]
            diff += f'\n  + {key}: {str(value2).lower()}'
    
    diff += '\n}'
    
    return diff