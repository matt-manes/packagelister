from pathlib import Path

import pytest

import packagelister


def test_packagelister_scan():
    packages = packagelister.scan(Path(__file__).parent.parent / "src")
    assert "pathcrawler" in packages
    assert "printbuddies" in packages
    assert "importlib" not in packages
    assert "sys" not in packages
    assert "pathlib" not in packages
    assert "argparse" not in packages
    packages = packagelister.scan(Path(__file__).parent.parent / "src", True)
    assert "pathcrawler" in packages
    assert "printbuddies" in packages
    assert "importlib" in packages
    assert "sys" in packages
    assert "pathlib" in packages
    assert "argparse" in packages


def test_packagelister_cli_main():
    ...


def test_packagelister_cli_get_args():
    ...
