import argparse
from pathlib import Path

from packagelister import scan


def main():
    def get_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "project_path",
            nargs="?",
            type=str,
            default=None,
            help=""" The project directory path to scan. """,
        )

        parser.add_argument(
            "-sf",
            "--show_files",
            action="store_true",
            help=""" Show which files imported each of the packages. """,
        )

        parser.add_argument(
            "-gr",
            "--generate_requirements",
            action="store_true",
            help=""" Generate a requirements.txt file in --project_path. """,
        )

        parser.add_argument(
            "-ib",
            "--include_builtins",
            action="store_true",
            help=""" Include built in standard library modules. """,
        )

        args = parser.parse_args()

        if not args.project_path:
            args.project_path = Path.cwd()
        else:
            args.project_path = Path(args.project_path)
        if not args.project_path.is_absolute():
            args.project_path = args.project_path.absolute()

        return args

    args = get_args()
    packages = scan(args.project_path, args.include_builtins)
    if args.generate_requirements:
        req_path = args.project_path / "requirements.txt"
        req_path.write_text(
            "\n".join(
                f"{package}=={packages[package]['version']}"
                if packages[package]["version"]
                else package
                for package in sorted(packages)
            )
        )
    packages = {
        f"{package}=={packages[package]['version']}": packages[package]["files"]
        for package in sorted(packages)
    }

    if args.show_files:
        longest_key = max(len(package) for package in packages)
        packages = [
            f"{package}{' '*(longest_key-len(package)+4)}{', '.join(str(Path(file).relative_to(args.project_path)) for file in packages[package])}"
            for package in packages
        ]

    print(f"Packages used in {args.project_path.stem}:")
    print(
        *packages,
        sep="\n",
    )


if __name__ == "__main__":
    main()
