import pytest
from pathier import Pathier, Pathish

root = Pathier(__file__).parent

import packagelister

# List of packages imported by packagelister.py
builtins = ["ast", "importlib", "sys", "dataclasses"]
third_partys = ["pathier", "printbuddies", "typing_extensions"]
imports = builtins + third_partys
num_packages = len(imports)


def test__get_package_names_from_source():
    file = root.parent / "src" / "packagelister" / "packagelister.py"
    package_names = packagelister.get_package_names_from_source(file.read_text())
    assert len(package_names) == num_packages
    for package in imports:
        assert package in package_names


def test__packagelister_scan_file():
    file = root.parent / "src" / "packagelister" / "packagelister.py"
    scanned_file = packagelister.scan_file(file)
    assert len(scanned_file.packages) == num_packages
    for package in scanned_file.packages.names:
        assert package in imports
    for package in scanned_file.packages.builtin.names:
        assert package in builtins
    for package in scanned_file.packages.third_party.names:
        assert package in third_partys


def test__packagelister_scan_dir():
    path = root.parent
    project = packagelister.scan_dir(path)
    files = path.rglob("*.py")
    assert all(file.path in files for file in project.files)
    assert len(project.requirements) == len(third_partys + ["pytest"])
    print(project.get_formatted_requirements("=="))
    assert project.get_formatted_requirements() == sorted(third_partys + ["pytest"])
    print(project.get_files_by_package())
