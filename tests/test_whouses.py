import pytest
from pathier import Pathier

from packagelister import whouses

root = Pathier(__file__).parent


def test_find():
    package = "fakepackage"
    package_users = whouses.find(root - 2, package, ["pkgs", "envs"])
    assert "fakeproject" in package_users
    assert len(package_users) == 1
