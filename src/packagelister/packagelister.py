import importlib
import inspect
import sys
from pathlib import Path

from pathcrawler import crawl
from printbuddies import ProgBar


def get_packages_from_source(source: str) -> list[str]:
    """Scan `source` and extract the names of imported packages/modules."""
    import_lines = [
        line.split()[1]
        for line in source.split("\n")
        if line.startswith(("from", "import"))
    ]
    # print(import_lines)
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
        imported_module = importlib.import_module(module)
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
    return packages


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
    elif type(project_dir) is str:
        project_dir = Path(project_dir)
    if not project_dir.is_absolute():
        project_dir = project_dir.absolute()

    # Return empty dict if project_dir doesn't exist
    if not project_dir.exists():
        return {}
    # You can scan a non python file one at a time if you reeeally want to.
    if project_dir.is_file():
        files = [project_dir]
    else:
        files = [file for file in crawl(project_dir) if file.suffix == ".py"]

    bar = ProgBar(len(files), width_ratio=0.33)
    # If scanning one file, the progress bar will show 0% complete if bar.counter == 0
    if len(files) == 1:
        bar.counter = 1
    packages = {}
    standard_lib = list(sys.stdlib_module_names) if not include_builtins else []
    for file in files:
        bar.display(suffix=f"Scanning {file.name}")
        source = file.read_text(encoding="utf-8")
        packages = get_packages_from_source(source)
        for package in packages:
            if file.with_stem(package) not in files and package not in standard_lib:
                if package in packages and str(file) not in packages[package]["files"]:
                    packages[package]["files"].append(str(file))
                else:
                    try:
                        package_version = importlib.metadata.version(package)
                    except Exception as e:
                        package_version = None
                    packages[package] = {
                        "files": [str(file)],
                        "version": package_version,
                    }
    return packages
