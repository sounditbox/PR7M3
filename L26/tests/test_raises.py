import pytest


def my_func():
    raise ValueError('Test error')


def test_raises():
    with pytest.raises(ValueError) as e:
        my_func()
    assert e.value.args[0] == 'Test error'
