# from_notebook

Available on pypi! `pip install from-notebook`

Small Python utility for importing functions, classes, and constants from .ipynb files. A few other packages claim similar functionality; I wrote this because none of them worked on the first try for me.

Notebooks can be imported from other notebooks or from normal Python scripts. The target notebook is assumed to be located in the current working directory.

You just import the notebook as if it was a submodule of `from_notebook`. So to import definitions from `example.ipynb`, any of the following will work:

```python
import from_notebook.example
```
```python
import from_notebook.example as example
```
```python
from from_notebook.example import example_function, ExampleClass
```

No notebook code is executed except for imports, `class` and `def` statements, and `SNAKE_CAPS = ...` assignments. All of these will be executed, so make sure they don't set off any unwanted side effects.

See [DEV_NOTES.md](./DEV_NOTES.md) for a more detailed discussion of how this all works.
