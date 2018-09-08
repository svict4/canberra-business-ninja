import pytest

from preprocessing import Preprocessing


def test_read_census_data():
    pp = Preprocessing()
    pp.read_census_data()

