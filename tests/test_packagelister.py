from pathier import Pathier

import pytest

import packagelister


def test_packagelister_scan():
    print()
    packages = packagelister.scan(Pathier(__file__).parent.parent / "src")
    assert "printbuddies" in packages
    assert "importlib" not in packages
    assert "sys" not in packages
    assert "pathlib" not in packages
    assert "argparse" not in packages
    assert "packagelister" not in packages
    packages = packagelister.scan(Pathier(__file__).parent.parent / "src", True)
    assert "printbuddies" in packages
    assert "importlib" in packages
    assert "sys" in packages
    assert "pathlib" in packages
    assert "argparse" in packages
    assert "packagelister" not in packages


def test__get_packages_from_source():
    print()
    text = (
        Pathier(__file__).parent.parent / "src" / "packagelister" / "packagelister.py"
    ).read_text()
    packages = packagelister.get_packages_from_source(text)
    for package in [
        "importlib",
        "inspect",
        "pathlib",
        "printbuddies",
        "sys",
    ]:
        assert package in packages
