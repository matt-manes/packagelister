import pytest
from pathier import Pathier, Pathish

root = Pathier(__file__).parent

from packagelister import packagelister

# List of packages imported by packagelister.py
builtins = ["ast", "importlib", "sys", "dataclasses"]
third_partys = ["pathier", "printbuddies", "typing_extensions", "younotyou"]
imports = builtins + third_partys
num_packages = len(imports)
test_path = root.parent / "src" / "packagelister" / "packagelister.py"


def test__is_builtin():
    assert packagelister.is_builtin("sys")
    assert not packagelister.is_builtin("pathier")


def test__Package():
    package = packagelister.Package.from_name("pathier")
    assert package.name == "pathier"
    assert package.distribution_name == "pathier"
    assert package.version
    assert not package.builtin
    assert (
        package.get_formatted_requirement("==")
        == f"{package.distribution_name}=={package.version}"
    )


def test__Package_from_distribution():
    package = packagelister.Package.from_distribution_name("pathier")
    assert package.name == ""
    assert package.distribution_name == "pathier"
    assert package.version
    assert not package.builtin


def test__get_package_names_from_source():
    file = test_path
    package_names = packagelister.get_package_names_from_source(file.read_text())
    assert len(package_names) == num_packages
    for package in imports:
        assert package in package_names


def test__packagelister_scan_file():
    file = test_path
    scanned_file = packagelister.scan_file(file)
    assert len(scanned_file.packages) == num_packages
    for package in scanned_file.packages.names:
        assert package in imports
    for package in scanned_file.packages.builtin.names:
        assert package in builtins
    for package in scanned_file.packages.third_party.names:
        assert package in third_partys
    for package in scanned_file.packages.third_party.distribution_names:
        assert package in third_partys


def test__packagelister_scan_dir():
    path = root.parent
    project = packagelister.scan_dir(path)
    files = path.rglob("*.py")
    other_third_party = ["pytest", "rich", "argshell"]
    assert all(file.path in files for file in project.files)
    assert len(project.requirements) == len(third_partys + other_third_party)
    print(project.get_formatted_requirements("=="))
    assert project.get_formatted_requirements() == sorted(
        third_partys + other_third_party
    )
    print(project.get_files_by_package())
