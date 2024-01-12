import argparse

from pathier import Pathier

from packagelister import packagelister


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f",
        "--show_files",
        action="store_true",
        help=""" Show which files imported each of the packages. """,
    )

    parser.add_argument(
        "-g",
        "--generate_requirements",
        action="store_true",
        help=""" Generate a requirements.txt file. """,
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
        "-i",
        "--include_builtins",
        action="store_true",
        help=""" Include built in standard library modules. """,
    )

    parser.add_argument("-d", "--debug", action="store_true")

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
            if not args.include_builtins
            else project.unique_packages.names
        ),
        sep="\n",
    )
    if args.generate_requirements:
        print("Generating `requirements.txt`.")
        (Pathier.cwd() / "requirements.txt").join(
            project.get_formatted_requirements(args.versions)
        )
    if args.show_files:
        print("Files importing each package:")
        files_by_package = project.get_files_by_package()
        for package, files in files_by_package.items():
            print(f"{package}:")
            print(*[f"  {file}" for file in files], sep="\n")
    if args.debug:
        print(*project.unique_packages, sep="\n")


if __name__ == "__main__":
    main(get_args())
