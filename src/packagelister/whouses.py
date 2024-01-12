import argparse

from pathier import Pathier

import packagelister


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package",
        type=str,
        help=""" Scan the current working directory for project folders that use this package.""",
    )

    parser.add_argument(
        "-i",
        "--ignore",
        nargs="*",
        default=[],
        type=str,
        help=""" Ignore these folders. """,
    )
    args = parser.parse_args()

    return args


def find(root: Pathier, package: str, ignore: list[str] = []) -> list[str]:
    """Find what sub-folders of `root`, excluding those in `ignore`, have files that use `package`."""
    package_users = []
    scan_fails = {}  # Error message: [projects]
    for project in root.iterdir():
        if project.is_dir() and project.stem not in ignore:
            try:
                if package in packagelister.scan_dir(project).unique_packages.names:
                    package_users.append(project.stem)
            except Exception as e:
                err = str(e)
                if err not in scan_fails:
                    scan_fails[err] = [project]
                else:
                    scan_fails[err].append(project)
    print()
    print("The following errors occured during the scan:")
    for fail in scan_fails:
        print(f"ERROR: {fail}:")
        print(*scan_fails[fail], sep="\n")
        print()
    return package_users


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    package_users = find(Pathier.cwd(), args.package, args.ignore)
    print(f"The following folders have files that use {args.package}:")
    print(*package_users, sep="\n")


if __name__ == "__main__":
    main(get_args())
