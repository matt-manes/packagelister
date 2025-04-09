from collections import deque

import argshell
from pathier import Pathier, Pathish
from printbuddies import track
from rich import print
from rich.tree import Tree

from packagelister import packagelister


class LocalDependencyScanner:
    def __init__(self, path: Pathier | Pathish | None = None, recursive: bool = False):
        self._root = Pathier.cwd() if not path else Pathier(path)
        self._globber = self._root.rglob if recursive else self._root.glob
        self._local_modules = self._get_local_module_names()
        self._imports: dict[str, set[str]] = {}

    @property
    def import_graph(self) -> dict[str, set[str]]:
        """Returns a dictionary of local module names and a set of what local modules import them."""
        if not self._imports:
            self.scan()
        return self._imports

    def _get_local_module_names(self) -> list[str]:
        return [path.stem for path in self._globber("*.py")]

    def __invert_imports(self):
        """After running the scan, `_imports` will have keys that are the importing modules
        and values that are the modules it imports.
        This reconstructs the dict so that the keys are modules and the values
        are modules that import the key."""
        inverted: dict[str, set[str]] = {}
        for module, deps in self._imports.items():
            for dep in deps:
                inverted.setdefault(dep, set())
                inverted[dep].add(module)
        self._imports = inverted

    def scan(self):
        """Scan the target directory for '.py' files and build the import graph of local modules."""
        self._imports = {}
        for f in track(self._globber("*.py"), "Scanning files..."):
            try:
                source = f.read_text(encoding="utf-8")
            except Exception as e:
                print(e)
            else:
                packages = packagelister.get_package_names_from_source(source)
                for package in packages:
                    if package in self._local_modules:
                        self._imports.setdefault(f.stem, set())
                        self._imports[f.stem].add(package)
        # `_imports` is currently a module and the modules it imports
        # invert it so the key is a module and the values are modules that import it
        self.__invert_imports()

    def get_refactor_order(self) -> deque[str]:
        """Returns a possible ordering that modules can be modified such that,
        when modifying a given file,
        all files it imports have already been modified."""
        visited: set[str] = set()
        stack: deque[str] = deque()
        if not self._imports:
            self.scan()
        for node in self._imports:
            if node not in visited:
                self._dfs(node, visited, stack)
        return stack

    def _dfs(self, node: str, visited: set[str], stack: deque[str]):
        if node not in visited:
            visited.add(node)
            if node in self._imports:
                for neighbor in self._imports[node]:
                    self._dfs(neighbor, visited, stack)
            stack.appendleft(node)

    def _build_import_tree(self, module: str, branch: Tree):
        if module in self._imports:
            for importer in self._imports[module]:
                self._build_import_tree(importer, branch.add(importer))

    def get_module_tree(self, module: str) -> Tree:
        """Returns a tree representing local modules that import `module`."""
        if not self._imports:
            self.scan()
        tree = Tree(f"Imports {module}", style="deep_pink1")
        self._build_import_tree(module, tree)
        return tree

    def get_import_tree(self) -> Tree:
        """Returns a tree representing local module import structure."""
        if not self._imports:
            self.scan()
        tree = Tree(f"Import tree", style="deep_pink1")
        for module in self._imports:
            self._build_import_tree(module, tree.add(module))
        return tree

    def _build_order_tree(self, module: str, branch: Tree):
        subbranch = branch.add(module)
        if module not in self._imports:
            return
        for submodule in self._imports[module]:
            self._build_order_tree(submodule, subbranch)

    def get_order_tree(self, stack: deque[str]) -> Tree:
        """Returns a full tree representing a refactoring order."""
        if not self._imports:
            self.scan()
        tree = Tree("Refactor order", style="deep_pink1")
        for module in stack:
            self._build_order_tree(module, tree)
        return tree

    def get_unimported_modules(self) -> list[str]:
        """Returns a list of local modules that aren't imported by any other modules."""
        if not self._imports:
            self.scan()
        modules: list[str] = []
        for module in self._local_modules:
            if module not in self._imports:
                modules.append(module)
        return modules


def get_parser() -> argshell.ArgumentParser:
    parser = argshell.ArgumentParser(
        description=""" 
        Provide details about local module imports.
        """
    )
    parser.add_help_preview()

    parser.add_argument(
        "-o",
        "--order",
        action="store_true",
        help="""List local modules in an order such that, when refactoring a given module, 
    the modules it imports will have already been refactored. """,
    )

    parser.add_argument(
        "-m",
        "--module",
        type=str,
        default=None,
        help=""" Show which modules import the provided one.""",
    )

    parser.add_argument(
        "-t",
        "--tree",
        action="store_true",
        help=""" Show full local dependency graph.
        If passed with the `-o/--order` switch, the full graph of the
        refactoring order will be displayed.""",
    )

    parser.add_argument(
        "-u",
        "--unimported",
        action="store_true",
        help=""" Display local modules not imported by any others.""",
    )

    parser.add_argument(
        "-r", "--recursive", action="store_true", help=""" Scan recursively."""
    )
    return parser


def get_args() -> argshell.Namespace:

    parser = get_parser()
    args = parser.parse_args()

    if not args.tree and not args.order and not args.module and not args.unimported:
        parser.print_help()
        exit()

    return args


def main(args: argshell.Namespace | None = None):
    if not args:
        args = get_args()
    scanner = LocalDependencyScanner(None, args.recursive)
    scanner.scan()
    if args.tree and not args.order:
        print(scanner.get_import_tree())
    elif args.module:
        print(scanner.get_module_tree(args.module))
    elif args.order:
        s = scanner.get_refactor_order()
        if not args.tree:
            print("Refactoring order:")
            print(*s, sep="\n")
        else:
            print(scanner.get_order_tree(s))
    elif args.unimported:
        print("Unimported modules:")
        print(*scanner.get_unimported_modules(), sep="\n")
    else:
        print(get_parser().print_help())


if __name__ == "__main__":
    main(get_args())
