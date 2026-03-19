import pytest

from solution.board import sum_numbers, random_location


def test_sum_numbers():
    assert sum_numbers(2, 3) == 5
    assert sum_numbers(-1, 1) == 0
    assert sum_numbers(0, 0) == 0

def test_random_location():
    result = random_location()
    assert 0 <= result[0] < 10
    assert 0 <= result[1] < 10

def test_random_location_with_occupied():
    result = random_location(occupied=[(1, 1)], max_retries=10, width=3, height=3)
    assert result != (1, 1)
    assert result[0] < 3
    assert result[1] < 3

def test_random_location_failed():
    """This call fails because there are no empty locations on the board."""
    with pytest.raises(RuntimeError):
        random_location(occupied=[(0, 0), (0, 1), (1, 0), (1, 1)], max_retries=1, width=2, height=2)