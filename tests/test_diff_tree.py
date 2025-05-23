from gendiff.diff_tree import build_diff


def test_build_diff_empty():
    assert build_diff({}, {}) == []


def test_build_diff_added():
    data1 = {}
    data2 = {'key': 'value'}
    result = build_diff(data1, data2)
    assert len(result) == 1
    assert result[0]['name'] == 'key'
    assert result[0]['action'] == 'added'
    assert result[0]['value'] == 'value'


def test_build_diff_deleted():
    data1 = {'key': 'value'}
    data2 = {}
    result = build_diff(data1, data2)
    assert len(result) == 1
    assert result[0]['name'] == 'key'
    assert result[0]['action'] == 'deleted'
    assert result[0]['value'] == 'value'


def test_build_diff_unchanged():
    data1 = {'key': 'value'}
    data2 = {'key': 'value'}
    result = build_diff(data1, data2)
    assert len(result) == 1
    assert result[0]['name'] == 'key'
    assert result[0]['action'] == 'unchanged'
    assert result[0]['value'] == 'value'


def test_build_diff_modified():
    data1 = {'key': 'old_value'}
    data2 = {'key': 'new_value'}
    result = build_diff(data1, data2)
    assert len(result) == 1
    assert result[0]['name'] == 'key'
    assert result[0]['action'] == 'modified'
    assert result[0]['old_value'] == 'old_value'
    assert result[0]['new_value'] == 'new_value'


def test_build_diff_nested():
    data1 = {
        'key': {
            'nested_key': 'value'
        }
    }
    data2 = {
        'key': {
            'nested_key': 'new_value'
        }
    }
    result = build_diff(data1, data2)
    assert len(result) == 1
    assert result[0]['name'] == 'key'
    assert result[0]['action'] == 'nested'
    assert len(result[0]['children']) == 1
    assert result[0]['children'][0]['name'] == 'nested_key'
    assert result[0]['children'][0]['action'] == 'modified'
    assert result[0]['children'][0]['old_value'] == 'value'
    assert result[0]['children'][0]['new_value'] == 'new_value'


def test_build_diff_complex():
    data1 = {
        'common': {
            'setting1': 'Value 1',
            'setting2': 200,
            'setting3': True,
            'setting6': {
                'key': 'value',
                'doge': {
                    'wow': ''
                }
            }
        },
        'group1': {
            'baz': 'bas',
            'foo': 'bar',
            'nest': {
                'key': 'value'
            }
        },
        'group2': {
            'abc': 12345,
            'deep': {
                'id': 45
            }
        }
    }
    data2 = {
        'common': {
            'setting1': 'Value 1',
            'setting2': 300,
            'setting3': 'true',
            'setting6': {
                'key': 'value',
                'ops': 'vops'
            }
        },
        'group1': {
            'baz': 'bars',
            'nest': 'str'
        },
        'group3': {
            'fee': 100500,
            'deep': {
                'id': {
                    'number': 45
                }
            }
        }
    }
    result = build_diff(data1, data2)
    
    assert len(result) == 4
    
    common = next(item for item in result if item['name'] == 'common')
    assert common['action'] == 'nested'
    common_children = common['children']
    assert len(common_children) == 4
    
    group1 = next(item for item in result if item['name'] == 'group1')
    assert group1['action'] == 'nested'
    group1_children = group1['children']
    assert len(group1_children) == 3
    
    group2 = next(item for item in result if item['name'] == 'group2')
    assert group2['action'] == 'deleted'
    
    group3 = next(item for item in result if item['name'] == 'group3')
    assert group3['action'] == 'added' 