# from_notebook

Small Python utility for importing functions, classes, and constants from .ipynb files.


Imports can be made from other notebooks or from normal Python scripts. The target notebook is assumed to be located in the current working directory. You simply import the notebook as if it was a submodule of `from_notebook`. So to import definitions from `./example.ipynb`: `import from_notebook.example`.

All import forms are supported, eg `import from_notebook.example as example`, `from from_notebook.example import example_function, ExampleClass`, and so on.

Does not execute any notebook code except for imports, `class` and `def` statements, and `SNAKE_CAPS = ...` assignments. All of these will be executed, so consider taking a quick look to make sure they don't set off any unwanted side effects.

See [DEV_NOTES.md](./DEV_NOTES.md) for a more detailed discussion of how this all works.
