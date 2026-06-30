from gendiff.diff import generate_diff


def test_generate_diff_json():
    file1 = 'tests/test_data/file1.json'
    file2 = 'tests/test_data/file2.json'

    with open('tests/test_data/result_json.txt') as file:
        expected = file.read().strip()
    result = generate_diff(file1, file2)

    assert result == expected

def test_generate_diff_yaml():
    file1 = 'tests/test_data/file1.yml'
    file2 = 'tests/test_data/file2.yml'

    with open('tests/test_data/result_yaml.txt') as file:
        expected = file.read().strip()
    result = generate_diff(file1, file2)

    assert result == expected

def test_empty_yaml_files():
    file1 = 'tests/test_data/empty_file1.yaml'
    file2 = 'tests/test_data/empty_file2.yaml'

    result = generate_diff(file1, file2)

    assert result == '{\n}'

def test_without_signs_json():
    file1 = 'tests/test_data/file1_identity.json'
    file2 = 'tests/test_data/file2_identity.json'

    with open('tests/test_data/result_identity.txt') as file:
        expected = file.read().strip()
    result = generate_diff(file1, file2)

    assert result == expected

def test_nested_json():
    file1 = 'tests/test_data/file1_nested.json'
    file2 = 'tests/test_data/file2_nested.json'

    with open('tests/test_data/result_nested.txt') as file:
        expected = file.read().strip()
    result = generate_diff(file1, file2)

    assert result == expected

def test_nested_yaml():
    file1 = 'tests/test_data/file1_nested.yaml'
    file2 = 'tests/test_data/file2_nested.yaml'

    with open('tests/test_data/result_nested.txt') as file:
        expected = file.read().strip()
    result = generate_diff(file1, file2)

    assert result == expected