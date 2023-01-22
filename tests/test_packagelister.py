from pathlib import Path

import pytest

import packagelister


def test_packagelister_scan():
    packages = packagelister.scan(Path(__file__).parent.parent / "src")
    assert "pathcrawler" in packages
    assert "printbuddies" in packages


def test_packagelister_cli_main():
    ...


def test_packagelister_cli_get_args():
    ...
