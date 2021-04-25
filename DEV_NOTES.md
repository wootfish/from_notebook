This library relies on a couple of Python's lesser-used features: import path
meta hooks and native AST support. Not everyone is familiar with these, so I
thought I'd write some quick notes about how everything fits together here.

We start by adding a hook to `sys.meta_hooks`. This allows us to add new
features to Python's import functionality; you can read more about how this
works [here](https://docs.python.org/3/reference/import.html#the-meta-path).

Our hook will examine imports for submodules of `from_notebook`, and will
assume these are meant as references to notebook files. For example, `import
from_notebook.train_model` will be interpreted as an import from a file called
`train_model.ipynb`. It is assumed that this file is present in the current
working directory (though this is not a hard technical requirement - it would
be pretty easy to add support for a full search path if anyone wants that). If
the notebook file is not found, the import fails.

If the notebook is found, we return a `NotebookLoader`, which is a subclass of
`importlib.abc.Loader`. This is responsible for creating and initializing a
`types.ModuleType` object which will eventually be inserted into `sys.modules`.

This class has two methods: `create_module` and `exec_module`. You can read
about how these are used [here](https://docs.python.org/3/reference/import.html#loading).
`create_module` is pretty much a stub method that shadows the default behavior.
All our interesting logic is in `exec_module`. This method does the following:

* Reconstructs the notebook's name based on the module name
* Opens this notebook (which is just a big blob of JSON) and deserializes it
* Concatenates all the notebook's code cells into one big string of Python code
* Parses this code to get an `ast.Module` object representing the notebook's full abstract syntax tree
  * Note that this does not involve executing any notebook code
* Filters this `ast.Module`'s body to remove everything except:
  * `import` and `from ... import ...` statements
  * `class` and `def` statements
  * `SNAKE_CAPS = ...` assignments for all-caps variable names (assumed to be constants with low-cost evaluation)
    * We already know, if AST parsing succeeded, that these names are valid, so we can match them with a simple regex: `^{A-Z0-9_}+$`
* Loads this filtered body into a new `ast.Module` object and compiles it
* Executes this compiled code in our new module's namespace

And that's all it takes! Our module now provides every class, function, and
snake-caps constant from the given notebook. As long as all these definitions
are cheap and free of side effects (as they should be), we're good to go!

## Misc Notes

* You probably can't use notebooks whose names are shadowed by names defined in
  `from_notebook.__init__.py`. So if you have a notebook named `_install.ipynb`
  or `_import_hook.ipynb`, I'm guessing you're out of luck. But frankly, if
  your notebooks have names like those, you probably have bigger problems.
  
* Relatedly, you can't import any notebook whose name isn't a valid Python name. So notebooks with spaces in their names are out, for instance. We could add name mangling to support this, but that would open the possibility of name collisions, so I see it as being more trouble than it's worth. Just use underscores instead of spaces or dashes in your filenames tbh.

* There aren't any config options yet. This is a scratch-your-own-itch project
  and I don't need any config. That said, these would be easy to add; if you
  need config, feel free to file an issue or take a go at it yourself.

  * At a bare minimum, it would make sense to add a search path and the ability
    to toggle constant imports (as these might, in some cases, be expensive or
    have side effects). If we wanted to really go big, it might be neat to
    support adding arbitrary filter predicates.

* The import process is not quite instantaneous. I wonder if it would be
  faster, especially for really big notebooks, to perform ast filtering
  per-cell rather than doing it after concatenating all the cells together.
