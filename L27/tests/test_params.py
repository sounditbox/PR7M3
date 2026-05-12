import pytest


def power(base, exp=None):
    if exp is None:
        exp = 2
    return base ** exp


@pytest.mark.parametrize('b, e, res', [
    (2, 3, 8),
    (3, 2, 9),
    (4, None, 16),
])
def test_power(b, e, res):
    assert power(b, e) == res
    assert power(b) == b ** 2
