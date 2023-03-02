import pytest

from city import DistrictGrid


def test_city_grid_bad_location():
    locs = {
        'school': [(-1, 1), (3, 3)],
        'hospital': [(3, 7)],
        'leisure': [(2, 4), (5, 5)]
    }
    with pytest.raises(ValueError):
        DistrictGrid('dist1', 10, 10, False, locs)


def test_city_grid_repeated_location():
    locs = {
        'school': [(0, 1), (3, 3)],
        'hospital': [(0, 1)],
        'leisure': [(2, 4), (5, 5)]
    }
    with pytest.raises(ValueError):
        DistrictGrid('dist1', 10, 10, False, locs)


def test_city_grid_busy():
    locs = {
        'school': [(0, 1), (3, 3)],
        'hospital': [(1, 1)],
        'leisure': [(2, 4), (5, 5)]
    }
    city = DistrictGrid('dist1', 10, 10, False, locs)
    assert city.is_busy(0, 1)
    assert city.is_busy(1, 1)
    assert city.is_busy(5, 5)

    assert not city.is_busy(2, 2)
    city.add_location('school', 2, 2)
    assert city.is_busy(2, 2)

    assert not city.is_busy(4, 3)
    city.add_location('bar', 4, 3)
    assert city.is_busy(4, 3)
    