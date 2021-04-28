from pgfinder import utils

def test_allowed_modifications():
    assert(isinstance(utils.allowed_modifications(), list))