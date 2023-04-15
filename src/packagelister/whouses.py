import argparse
from pathlib import Path
from packagelister import scan


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package",
        type=str,
        help=""" Scan the current working directory for
        project folders that use this package.""",
    )

    parser.add_argument(
        "-i",
        "--ignore",
        nargs="*",
        default=["pkgs", "envs"],
        type=str,
        help=""" Ignore these folders. """,
    )
    args = parser.parse_args()

    return args


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    package_users = []
    for project in Path.cwd().iterdir():
        if project.is_dir() and project.stem not in args.ignore:
            if args.package in scan(project):
                package_users.append(project.stem)
    print(f"The following packages use {args.package}:")
    print(*package_users, sep="\n")


if __name__ == "__main__":
    main(get_args())
