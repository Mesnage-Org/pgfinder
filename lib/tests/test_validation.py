"""Test validation functions"""

from pgfinder import validation


def test_allowed_modifications():
    assert isinstance(validation.allowed_modifications(), list)
