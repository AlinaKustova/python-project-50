from gendiff.diff_builder import build_diff
from gendiff.formatters.stylish import stylish
from gendiff.parser import read_file
from gendiff.formatters.plain import plain


def generate_diff(path1, path2, format_name='stylish'):
    file1 = read_file(path1)
    file2 = read_file(path2)

    diff = build_diff(file1, file2)
    
    if format_name == 'stylish':
        return stylish(diff)
    
    elif format_name == 'plain':
        return '\n'.join(plain(diff))
    
    return diff