Small Python utility for importing functions, classes, and constants from .ipynb files. A few other packages offer to provide similar functionality; I wrote this because none of them worked on the first try for me.

Notebooks can be imported from other notebooks or from normal Python scripts. The target notebook is assumed to be located in the current working directory.

You simply import the notebook as if it was a submodule of ``from_notebook``. So to import definitions from ``example.ipynb``, any of the following will work:

``import from_notebook.example``

``import from_notebook.example as example``

``from from_notebook.example import example_function, ExampleClass``

No notebook code is executed except for imports, ``class`` and ``def`` statements, and ``SNAKE_CAPS = ...`` assignments. All of these will be executed, so make sure they don't set off any unwanted side effects.
