from scripts.validate_repository import validate_repository


def test_repository_structure_is_valid():
    assert validate_repository() == []
