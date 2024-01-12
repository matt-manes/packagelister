import argparse

from pathier import Pathier

from packagelister import packagelister


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="packagelister",
        description=""" Scan the current directory for imported packages. """,
    )

    parser.add_argument(
        "-f",
        "--files",
        action="store_true",
        help=""" Show which files imported each of the packages. """,
    )

    parser.add_argument(
        "-g",
        "--generate_requirements",
        action="store_true",
        help=""" Generate a requirements.txt file in the current directory. """,
    )

    parser.add_argument(
        "-v",
        "--versions",
        type=str,
        default=None,
        choices=["==", "<", "<=", ">", ">=", "~="],
        help=""" When generating a requirements.txt file, include the versions of the packages using this relation.
            (You may need to put quotes around some of the options.)""",
    )

    parser.add_argument(
        "-b",
        "--builtins",
        action="store_true",
        help=""" Include built in standard library modules in terminal display. """,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help=""" Print the Package objects found during the scan. """,
    )

    args = parser.parse_args()

    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    project = packagelister.scan_dir(Pathier.cwd())
    print(f"Packages imported by {Pathier.cwd().stem}:")
    print(
        *(
            project.get_formatted_requirements(args.versions)
            if not args.builtins
            else project.packages.names
        ),
        sep="\n",
    )
    if args.generate_requirements:
        print("Generating `requirements.txt`.")
        (Pathier.cwd() / "requirements.txt").join(
            project.get_formatted_requirements(args.versions)
        )
    if args.files:
        print("Files importing each package:")
        files_by_package = project.get_files_by_package()
        for package, files in files_by_package.items():
            print(f"{package}:")
            print(*[f"  {file}" for file in files], sep="\n")
    if args.debug:
        print(*project.packages, sep="\n")


if __name__ == "__main__":
    main(get_args())
