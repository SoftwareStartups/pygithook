"""Testsuite for vfgithook.pylint"""

from vfgithook import pylint


def test_parse_score():
    """Test pylint.parse_score"""

    text = 'Your code has been rated at 8.51/10'
    assert pylint.parse_score(text) == 8.51

    text = 'Your code has been rated at 8.51'
    assert pylint.parse_score(text) == 0.0
