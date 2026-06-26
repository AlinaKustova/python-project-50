from gendiff.parser import read_file


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