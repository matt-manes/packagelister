import pytest
from pathier import Pathier

from packagelister import whouses

root = Pathier(__file__).parent


def test_find():
    package = "pathier"
    package_users = whouses.find(root - 1, package)
    assert root.stem in package_users
    assert "src" in package_users
    assert len(package_users) == 2
