# from_notebook
Small Python utility for importing functions, classes, and constants from .ipynb files.

Allows definitions from one notebook to be used in Python files or other notebooks.

By default only `def` and `class` blocks' definitions are made available.

To specify that global variables with `SNAKE_CAPS` names should be made available as well, call `from_notebook.include_constants()`. To countermand this directive, call `from_notebook.exclude_constants()`. The default behavior is to exclude these variables.
