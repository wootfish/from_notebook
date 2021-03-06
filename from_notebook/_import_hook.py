import ast
import importlib.abc
import json
import re
import sys
import types
from os.path import isfile


SNAKE_CASE_REGEX = re.compile("^{A-Z0-9_}+$")


class NotebookFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("from_notebook."):
            parts = fullname.split(".", 1)
            if isfile(parts[1]+".ipynb"):
                return self._gen_spec(fullname)

    def _gen_spec(self, fullname):
        spec = importlib.machinery.ModuleSpec(fullname, NotebookLoader())
        return spec


class NotebookLoader(importlib.abc.Loader):
    def create_module(self, spec):
        return types.ModuleType(spec.name)

    def exec_module(self, module):
        filename = module.__name__.split(".", 1)[1] + ".ipynb"
        nb_ast = self._get_nb_ast(filename)
        compiled = compile(self._trim_ast_module(nb_ast), "<ast>", "exec")
        exec(compiled, module.__dict__)  # run our notebook code in the new module's namespace

    @staticmethod
    def _get_nb_ast(fname):
        with open(fname) as f:
            nb_json = json.loads(f.read())
        nb_cells = [''.join(cell['source']) for cell in nb_json['cells']
                    if cell['cell_type'] == 'code']
        nb_code = '\n'.join(nb_cells)
        nb_ast = ast.parse(nb_code)
        return nb_ast

    @staticmethod
    def _trim_ast_module(ast_module):
        """
        Takes an ast.Module instance. Builds & returns a "trimmed" version with
        most costly operations removed. Retains only top-level `def` blocks,
        `class` blocks, and `SNAKE_CAPS_CONST = ...` assignments. Statements
        like `a, b = 1, 2` or `a = b = 1` or `a, b = c, d = 1, 2` are trimmed
        regardless of case.
        """

        # this is so fucking cool
        return ast.Module(body=[
            node for node in ast_module.body
            if isinstance(node, ast.ClassDef)
            or isinstance(node, ast.FunctionDef)
            or isinstance(node, ast.Import)
            or isinstance(node, ast.ImportFrom)
            or (isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and SNAKE_CASE_REGEX.match(node.targets[0].id))
            ], type_ignores=[])


def install():
    """
    Helper function for hooking ipynb imports.
    Encapsulates the complexity around setting up and installing the hook.
    """

    for finder in sys.meta_path:
        if isinstance(finder, NotebookFinder):
            return  # already installed - no additional action required

    sys.meta_path.append(NotebookFinder())
