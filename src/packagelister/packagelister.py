import ast
import importlib.metadata
import sys
from dataclasses import dataclass

from pathier import Pathier, Pathish
from printbuddies import ProgBar
from typing_extensions import Self

packages_distributions = importlib.metadata.packages_distributions()


def is_builtin(package_name: str) -> bool:
    return package_name in sys.stdlib_module_names


@dataclass
class Package:
    name: str
    distribution_name: str | None
    version: str | None
    builtin: bool

    def format_requirement(self, version_specifier: str):
        return f"{self.distribution_name}{version_specifier}{self.version}"

    @classmethod
    def from_name(cls, package_name: str) -> Self:
        distributions = packages_distributions.get(package_name)
        if distributions:
            distribution_name = distributions[0]
            version = importlib.metadata.version(distribution_name)
        else:
            distribution_name = None
            version = None
        return cls(package_name, distribution_name, version, is_builtin(package_name))


class PackageList(list[Package]):
    @property
    def names(self) -> list[str]:
        return [package.name for package in self]

    @property
    def third_party(self) -> Self:
        return self.__class__(
            [
                package
                for package in self
                if not package.builtin and package.distribution_name
            ]
        )

    @property
    def builtin(self) -> Self:
        return self.__class__([package for package in self if package.builtin])


@dataclass
class File:
    path: Pathier
    packages: PackageList


@dataclass
class Project:
    files: list[File]

    @property
    def unique_packages(self) -> PackageList:
        packages = []
        for file in self.files:
            for package in file.packages:
                if package not in packages:
                    packages.append(package)
        return PackageList(sorted(packages, key=lambda p: p.name))

    @property
    def requirements(self) -> PackageList:
        return self.unique_packages.third_party

    def get_formatted_requirements(
        self, version_specifier: str | None = None
    ) -> list[str]:
        return [
            requirement.format_requirement(version_specifier)
            if version_specifier
            else requirement.distribution_name or requirement.name
            for requirement in self.requirements
        ]

    def get_files_by_package(self) -> dict[Package, list[Pathier]]:
        files_by_package = {}
        for package in self.unique_packages:
            for file in self.files:
                name = package.name
                if name in file.packages.names:
                    if name not in files_by_package:
                        files_by_package[name] = [file.path]
                    else:
                        files_by_package[name].append(file.path)
        return files_by_package


def get_package_names_from_source(source: str) -> list[str]:
    """Scan `source` and extract the names of imported packages/modules."""
    tree = ast.parse(source)
    packages = []
    for node in ast.walk(tree):
        type_ = type(node)
        package = ""
        if type_ == ast.Import:
            package = node.names[0].name  # type: ignore
        elif type_ == ast.ImportFrom:
            package = node.module  # type: ignore
        if package:
            if "." in package:
                package = package[: package.find(".")]
            packages.append(package)
    return sorted(list(set(packages)))


def scan_file(file: Pathish) -> File:
    file = Pathier(file) if not type(file) == Pathier else file
    source = file.read_text(encoding="utf-8")
    packages = get_package_names_from_source(source)
    used_packages = PackageList(
        [
            Package.from_name(package)
            for package in packages
            if package
            not in file.parts  # don't want to pick up modules in the scanned directory
        ]
    )
    return File(file, used_packages)


def scan_dir(path: Pathish) -> Project:
    path = Pathier(path) if not type(path) == Pathier else path
    files = list(path.rglob("*.py"))
    print(f"Scanning {path}...")
    with ProgBar(len(files)) as bar:
        project = Project(
            [bar.display(return_object=scan_file(file)) for file in files]
        )
    return project
