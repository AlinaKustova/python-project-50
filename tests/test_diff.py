from gendiff.diff import generate_diff


def test_generate_diff():
    file1 = 'tests/test_data/file1.json'
    file2 = 'tests/test_data/file2.json'

    with open('tests/test_data/result.txt') as file:
        expected = file.read().strip()
    result = generate_diff(file1, file2)

    assert result == expected