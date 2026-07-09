# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Modeled after the BioCRNpyler documentation
# (https://github.com/BuildACell/BioCRNpyler/blob/main/docs/conf.py), which
# is a sibling project maintained by the same group.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import inspect
import os
import re
import sys
import sphinx

sys.path.insert(0, os.path.abspath('..'))

# Use the readthedocs.org theme if installed
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    try:
        import sphinx_rtd_theme  # noqa: F401

        html_theme = 'sphinx_rtd_theme'
    except ImportError:
        html_theme = 'default'

# -- Project information -----------------------------------------------------

project = 'Bioscrape'
copyright = '2026, Biocircuits'
author = 'Ayush Pandey, William Poole, Anandh Swaminathan, Richard M. Murray'

# Import the package
#
# Note: this requires that the compiled bioscrape extension modules
# (random/types/simulator/inference) match the Python interpreter used to
# build the docs.  See docs/develop.rst for build environment notes.
import bioscrape

# bioscrape does not (yet) use setuptools-scm; the version lives as a
# static string in pyproject.toml, so read it from there instead of
# relying on package metadata (which may not be installed/current).
try:
    import tomllib
except ImportError:  # Python < 3.11
    import tomli as tomllib

with open(os.path.abspath('../pyproject.toml'), 'rb') as f:
    _pyproject = tomllib.load(f)
release = _pyproject['project']['version']

# Short X.Y
version = '.'.join(release.split('.', 2)[:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.linkcode',
    'sphinx.ext.doctest',
    'sphinx_math_dollar',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
    'sphinx_toggleprompt',
    'nbsphinx',
    'nbsphinx_link',
    'recommonmark',
    'numpydoc',
]

source_suffix = ['.rst']

# scan documents for autosummary directives and generate stub pages for each.
autosummary_generate = True

# list of autodoc directive flags that should be automatically applied
# to all autodoc directives.
autodoc_default_options = {
    #    'members': True,
    #    'inherited-members': True,
    #    'special-members': True,
    'exclude-members': '__init__, __weakref__, __repr__, __str__, __hash__',
}

# For classes, include both the class docstring and the init docstring.
# Unlike BioCRNpyler, bioscrape's `cdef class` objects currently document
# their constructor arguments on __init__ rather than on the class, so we
# keep both until the docstrings are normalized (see docs/develop.rst).
autoclass_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# This config value contains the locations and names of other projects that
# should be linked to in this documentation.
intersphinx_mapping = {
    'scipy': ('https://docs.scipy.org/doc/scipy', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'python': ('https://docs.python.org/3/', None),
    # bioscrape and biocrnpyler are sibling projects; cross-link them.
    'biocrnpyler': ('https://biocrnpyler.readthedocs.io/en/latest/', None),
}

# Don't generate external links to (local) keywords
intersphinx_disabled_reftypes = ["py:keyword"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Set the default role to render items in backticks as code
default_role = 'py:obj'

# Use mathjax for formatting equations
sphinx_version = tuple(int(x) for x in sphinx.__version__.split('.')[:2])
if sphinx_version >= (4, 0):
    mathjax3_config = {
        "tex": {
            "inlineMath": [['\\(', '\\)']],
            "displayMath": [["\\[", "\\]"]],
        }
    }
else:
    mathjax_config = {
        'tex2jax': {
            'inlineMath': [["\\(", "\\)"]],
            'displayMath': [["\\[", "\\]"]],
        },
    }

# Skip prompts when using copy button
copybutton_prompt_text = r'>>> |\.\.\. '
copybutton_prompt_is_regexp = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ['_static']
html_css_files = ['css/custom.css']

# Don't automatically show all members of class in Methods & Attributes section
numpydoc_show_class_members = False

# Don't create a Sphinx TOC for the lists of class methods and attributes
numpydoc_class_members_toctree = False

# Leave Attributes documentation right after Parameters
napoleon_use_ivar = False
napoleon_custom_sections = [
    ('Attributes', 'params_style'),
]

# Aliases to allow objects to avoid including module names.
#
# Unlike BioCRNpyler, bioscrape does not expose a single flat top-level
# namespace (there is no `import bioscrape as bs; bs.Model`-style alias),
# so we walk the individual submodules that make up the public API.
napoleon_use_param = True
napoleon_preprocess_types = True  # convert refs in types to std form
napoleon_type_aliases = dict()

_bioscrape_submodules = [
    'bioscrape.types',
    'bioscrape.simulator',
    'bioscrape.inference',
    'bioscrape.analysis',
    'bioscrape.pid_interfaces',
    'bioscrape.sbmlutil',
]
for _modname in _bioscrape_submodules:
    try:
        _mod = __import__(_modname, fromlist=['dummy'])
    except ImportError:
        continue
    for name, obj in inspect.getmembers(_mod):
        if inspect.isclass(obj) and obj.__module__ == _modname:
            napoleon_type_aliases[name] = f":class:`~{_modname}.{name}`"

# Set autodoc aliases here to avoid recompiling everything every time
autodoc_type_aliases = {
    k: napoleon_type_aliases[k] for k in sorted(napoleon_type_aliases)
}

#
# Docstring pre-processing
#
# Same LaTeX-friendly substitutions used by BioCRNpyler, so that reaction
# notation (-->, <-->, ...) can be written in plain text in docstrings and
# rendered as proper math in the built documentation.

eqn_substitutions = [
    (r'<-->', r'\\rightleftharpoons'),
    (r'-->', r'\\rightarrow'),
    (r'\.\.\.', r'\\dots'),
    (r':', r'\\mathord{:}'),
    (r'\{\}', r'\\emptyset'),
    (r' >> ', r' \\gg '),
    (r' << ', r' \\ll '),
    (r"'([\w -]+)'", r'{\\text{\1}}'),  # literal text (incl _, -)
    (r"\[([\w -]+)\]", r'[\\text{\1}]'),  # concentration
    (r'^[ ]+', r''),  # remove leading blanks
    (r'\$[ ]+', r'$'),  # remove blanks after $
    (r'&    ', r'& \\qquad'),  # indented text
]

txt_substitutions = [
    (r'<-->', r'$\\rightleftharpoons$'),
    (r'-->', r'$\\rightarrow$'),
    (r'\{\}', r'$\\emptyset$'),
    (r' >> ', r' $\\gg$ '),
    (r' << ', r' $\\ll$ '),
]


def _process_string(s, subs):
    for pattern, repl in subs:
        s = re.sub(pattern, repl, s)
    return s


def preprocess_docstring(app, what, name, obj, options, lines):
    """
    Preprocess docstrings before Sphinx renders them.

    Parameters
    ----------
    app : Sphinx application object
    what : the type of object (e.g., 'module', 'class', 'function')
    name : the fully qualified name of the object
    obj : the object itself
    options : the options given to the directive
    lines : the lines of the docstring (list of strings, modified in-place)
    """
    in_equation = False
    for i, line in enumerate(lines):
        # Keep track of whether we are in "math" mode
        eqn_iter = re.finditer(r'\$[^$]+\$', line)  # $...$ or $$...$$
        eqn_list = list(eqn_iter)
        if re.match(r'^[ ]*\$\$$', line):  # $$ on its own line
            in_equation = not in_equation

        if in_equation:
            # Process everything in this line
            line = _process_string(line, eqn_substitutions)
        elif eqn_list:
            # Process each equation separately
            line, offset = '', 0
            for m in eqn_list:
                # Include the text up to this point
                line += _process_string(
                    lines[i][offset : m.start()], txt_substitutions
                )
                offset = m.end()

                # Process the text in the equation
                eqn = _process_string(m.group(0), eqn_substitutions)
                line += eqn

            # Add the suffix
            line += _process_string(
                lines[i][eqn_list[-1].end() :], txt_substitutions
            )
        else:
            line = _process_string(line, txt_substitutions)

        lines[i] = line


def setup(app):
    """Connect the preprocessing function to Sphinx."""
    app.connect('autodoc-process-docstring', preprocess_docstring)


# -----------------------------------------------------------------------------
# Source code links (from numpy, via BioCRNpyler)
# -----------------------------------------------------------------------------

import inspect
from os.path import dirname, relpath


def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    # Get the filename for the function
    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return None

    # Ignore re-exports as their source files are not within the bioscrape repo
    module = inspect.getmodule(obj)
    if module is not None and not module.__name__.startswith('bioscrape'):
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    fn = relpath(fn, start=dirname(bioscrape.__file__))

    if lineno:
        linespec = '#L%d-L%d' % (lineno, lineno + len(source) - 1)
    else:
        linespec = ''

    base_url = "https://github.com/biocircuits/bioscrape/blob/"
    if release != version:  # development release
        return base_url + 'master/bioscrape/%s%s' % (fn, linespec)
    else:  # specific version
        return base_url + 'v%s/bioscrape/%s%s' % (release, fn, linespec)


# -- Options for doctest ----------------------------------------------

doctest_global_setup = """
import numpy as np
from bioscrape.types import Model
"""
