from pgfinder import vaildation

def test_allowed_modifications():
    assert(isinstance(vaildation.allowed_modifications(), list))