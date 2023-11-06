"""Tests for the utility functions"""
import utils
import pytest


def test_sumvalues_standard():
    assert utils.sumvalues([1, 2, 3]) == 6


def test_sumvalues_empty_list():
    assert utils.sumvalues([]) == 0


def test_sumvalues_string_list():
    with pytest.raises(TypeError):
        utils.sumvalues(["a", "b", "c"])


def test_maxvalue_standard():
    assert utils.maxvalue([1, 5, 2, 3]) == 1


def test_maxvalue_empty_list():
    with pytest.raises(IndexError):
        utils.maxvalue([])


def test_maxvalue_string_list():
    with pytest.raises(TypeError):
        utils.maxvalue(["a", "b", "c"])


def test_minvalue_multiple_maxs():
    assert utils.maxvalue([7, 1, 7, 5, 7, 4]) == 0


def test_minvalue_standard():
    assert utils.minvalue([7, 1, 5, 2, 3]) == 1


def test_minvalue_multiple_mins():
    assert utils.minvalue([7, 1, 1, 5, 1, 4]) == 1


def test_minvalue_empty_list():
    with pytest.raises(IndexError):
        utils.minvalue([])


def test_minvalue_string_list():
    with pytest.raises(TypeError):
        utils.minvalue(["a", "b", "c"])


def test_meannvalue_standard():
    assert utils.meannvalue([1, 5, 2, 4]) == 3.0


def test_meannvalue_empty_list():
    with pytest.raises(ZeroDivisionError):
        utils.meannvalue([])


def test_meannvalue_string_list():
    with pytest.raises(TypeError):
        utils.meannvalue(["a", "b", "c"])

def test_countvalue_standard():
    assert utils.countvalue([1, 2, 3, 2, 4], 2) == 2


def test_countvalue_empty_list():
    assert utils.countvalue([], 2) == 0


def test_countvalue_not_in_list():
    assert utils.countvalue([1, 2, 3], 4) == 0


def test_length_standard():
    assert utils.length([1, 2, 3]) == 3


def test_length_non_sequence():
    with pytest.raises(TypeError):
        utils.length(123)


def test_length_empty_list():
    assert utils.length([]) == 0


def test_sort_list_standard():
    assert utils.sort_list([3, 1, 2, 4]) == [4, 3, 2, 1]


def test_sort_list_empty_list():
    assert utils.sort_list([]) == []


def test_sort_list_non_numerical():
    with pytest.raises(TypeError):
        utils.sort_list(["b", "a", "c"])


def test_median_standard():
    assert utils.median([3, 1, 2]) == 2


def test_median_empty_list():
    with pytest.raises(IndexError):
        utils.median([])


def test_median_non_numerical():
    with pytest.raises(TypeError):
        utils.median(["a", "b", "c"])

