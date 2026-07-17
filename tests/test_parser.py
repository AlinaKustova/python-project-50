from gendiff.scripts.parser import read_file


def test_read_file1_json():
    path1 = 'tests/test_data/file1.json'
    file1 = read_file(path1)

    assert isinstance(file1, dict)
    assert file1["host"] == "hexlet.io"
    assert file1["proxy"] == "123.234.53.22"

def test_read_file2_json():
    path2 = 'tests/test_data/file2.json'
    file2 = read_file(path2)

    assert isinstance(file2, dict)
    assert file2["host"] == "hexlet.io"

def test_read_file1_yaml():
    path1 = 'tests/test_data/file1.yml'
    file1 = read_file(path1)

    assert isinstance(file1, dict)
    assert file1['proxy'] == '123.234.53.22'

def test_read_file2_yaml():
    path2 = 'tests/test_data/file2.yml'
    file2 = read_file(path2)

    assert isinstance(file2, dict)
    assert file2['host'] == 'hexlet.io'

def test_nested1_json():
    path1 = 'tests/test_data/file1_nested.json'
    file1 = read_file(path1)

    assert 'common' in file1.keys()
    assert isinstance(file1['common']['setting6'], dict) and 'doge' in file1['common']['setting6'].keys()

def test_nested2_json():
    path2= 'tests/test_data/file2_nested.json'
    file2 = read_file(path2)

    assert 'common' in file2.keys()
    assert isinstance(file2['common']['setting6'], dict) and 'doge' in file2['common']['setting6'].keys()

def test_nested1_yaml():
    path1 = 'tests/test_data/file1_nested.yaml'
    file1 = read_file(path1)

    assert 'common' in file1.keys()
    assert isinstance(file1['common']['setting6'], dict) and 'doge' in file1['common']['setting6'].keys()

def test_nested2_yaml():
    path2= 'tests/test_data/file2_nested.yaml'
    file2 = read_file(path2)

    assert 'common' in file2.keys()
    assert isinstance(file2['common']['setting6'], dict) and 'doge' in file2['common']['setting6'].keys()