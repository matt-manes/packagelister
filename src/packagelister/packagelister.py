import importlib
import inspect
import sys
from pathlib import Path

from printbuddies import ProgBar


def get_packages_from_source(source: str, recursive: bool = False) -> list[str]:
    """Scan `source` and extract the names of imported packages/modules.

    #### :params:

    `recursive`: Extract modules/packages that are imported by `source`'s imports
    and those imports' imports and those imports' imports..."""
    import_lines = [
        line.split()[1]
        for line in source.split("\n")
        if line.startswith(("from", "import"))
    ]
    packages = []
    for line in import_lines:
        module = None
        if line.startswith("."):
            module = line[1:]
        elif "." in line:
            module = line[: line.find(".")]
        if "," in line:
            module = line[:-1]
        if not module:
            module = line
        try:
            imported_module = importlib.import_module(module)
        except Exception as e:
            ...
        else:
            try:
                source_file = Path(inspect.getsourcefile(imported_module))
                packages.append(
                    source_file.parent.stem
                    if source_file.stem == "__init__"
                    else source_file.stem
                )
            except Exception as e:
                packages.append(module)
    packages = sorted(list(set(packages)))
    if recursive:
        i = 0
        while i < len(packages):
            module = importlib.import_module(packages[i])
            try:
                for package in get_packages_from_source(inspect.getsource(module)):
                    if package not in packages:
                        packages.append(package)
            except Exception as e:
                ...
            i += 1
    return packages


def remove_builtins(packages: list[str]) -> list[str]:
    """Remove built in packages/modules from a list of package names."""
    builtins = list(sys.stdlib_module_names)
    return filter(lambda x: x not in builtins, packages)


def scan(project_dir: Path | str = None, include_builtins: bool = False) -> dict:
    """Recursively scans a directory for python files to determine
    what packages are in use, as well as the version number
    if applicable.

    Returns a dictionary where the keys are package
    names and the values are the version number of the package if there is one
    (None if there isn't) and a list of the files that import the package.

    :param project_dir: Can be an absolute or relative path
    to a directory or a single file (.py).
    If it is relative, it will be assumed to be relative to
    the current working directory.
    If an argument isn't given, the current working directory
    will be scanned.
    If the path doesn't exist, an empty dictionary is returned."""
    if not project_dir:
        project_dir = Path.cwd()
    elif type(project_dir) is str or project_dir.is_file():
        project_dir = Path(project_dir)
    if not project_dir.is_absolute():
        project_dir = project_dir.absolute()

    # Raise error if project_dir doesn't exist
    if not project_dir.exists():
        raise FileNotFoundError(
            f"Can't scan directory that doesn't exist: {project_dir}"
        )
    # You can scan a non python file one at a time if you reeeally want to.
    if project_dir.is_file():
        files = [project_dir]
    else:
        files = list(project_dir.rglob("*.py"))

    bar = ProgBar(len(files), width_ratio=0.33)
    used_packages = {}
    for file in files:
        bar.display(suffix=f"Scanning {file.name}")
        source = file.read_text(encoding="utf-8")
        packages = get_packages_from_source(source)
        if not include_builtins:
            packages = remove_builtins(packages)
        for package in packages:
            if file.with_stem(package) not in files:
                if (
                    package in used_packages
                    and str(file) not in used_packages[package]["files"]
                ):
                    used_packages[package]["files"].append(str(file))
                else:
                    try:
                        package_version = importlib.metadata.version(package)
                    except Exception as e:
                        package_version = None
                    used_packages[package] = {
                        "files": [str(file)],
                        "version": package_version,
                    }
    return used_packages
