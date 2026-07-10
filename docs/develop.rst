.. currentmodule:: bioscrape

***************
Developer Notes
***************

This chapter contains notes for developers who wish to contribute to
the bioscrape package, including the plan for bringing its docstrings
up to the standard needed for this documentation to render well.  It
follows the same structure as `BioCRNpyler's developer notes
<https://biocrnpyler.readthedocs.io/en/latest/develop.html>`_, a
sibling project maintained by the same group.

Package Structure
=================

The bioscrape package is maintained on GitHub:

  * Source code repository: https://github.com/biocircuits/bioscrape
  * Issue tracker: https://github.com/biocircuits/bioscrape/issues

GitHub repository file and directory layout:
  - **bioscrape/** - main repository

    * LICENSE, MANIFEST.in, pyproject.toml, setup.py, README.md -
      package information

    * **bioscrape/** - primary package source code (Cython)

      + ``__init__.py`` - imports the compiled submodules and seeds
        the RNG

      + ``types.pyx`` - `~bioscrape.types.Model` and the propensity,
        delay, rule, and volume class hierarchies

      + ``simulator.pyx`` - deterministic/stochastic/delay/volume
        simulators and simulation interfaces

      + ``inference.pyx`` - data and likelihood classes for Bayesian
        inference

      + ``pid_interfaces.py``, ``analysis.py``, ``sbmlutil.py`` -
        pure-Python inference wrapper, sensitivity analysis, and SBML
        import/export helpers

      + ``random.pyx`` - random number generation

    * **lineage/** - the optional lineage/population-simulation
      extension (``lineage.pyx``), installed separately
      (``python setup.py install lineage``, or via the ``lineage``
      argument at the bottom of ``setup.py``)

    * **docs/** - user guide and reference manual (this documentation)

      + ``index.rst`` - main documentation index

      + ``conf.py``, ``Makefile`` - Sphinx configuration files

      + ``intro.rst``, ``model.rst``, ``simulation.rst``,
        ``inference.rst``, ``sensitivity.rst``, ``lineage.rst``,
        ``tutorials.rst`` - User Guide chapters

      + ``library.rst``, ``develop.rst`` - Reference Manual

      + ``examples/``, ``inference_examples/``, ``lineage_examples/``
        - symlinks to the corresponding ``*.ipynb`` files in the
        top-level example directories, so ``nbsphinx`` can render them
        without duplicating content

    * **examples/**, **inference examples/**, **lineage examples/**
      - Jupyter notebooks and example SBML/data files (note the
      spaces in the two latter directory names)

    * **tests/**, **lineage tests/** - pytest test suites


Build Environment for the Docs
==============================

Because bioscrape's public API is implemented in Cython
(``cdef class`` objects compiled to platform-specific ``.so`` files),
``sphinx.ext.autodoc`` must be able to ``import bioscrape`` -- which
means the extension must be built for the same Python interpreter used
to run ``sphinx-build``. This is different from a pure-Python package
and needs to be accounted for both locally and in the Read the Docs
build configuration (a build step that runs ``pip install .`` before
the Sphinx build, rather than just installing ``docs/requirements.txt``).


Naming Conventions and Code Style
=================================

Generally speaking, standard Python naming conventions are used
throughout the package, with the caveat that ``.pyx`` files mix
Python-visible members (``def``/``cpdef`` methods, and class/``__init__``
docstrings) with C-only internals (``cdef`` methods and attributes)
that are invisible to Python introspection -- and therefore to
autodoc. Only ``def``/``cpdef`` methods and class/``__init__``
docstrings can appear in the generated documentation; treat ``cdef``
methods as the package's equivalent of a leading-underscore "private"
convention.

Adding new functionality
------------------------

Bioscrape's core areas (propensities, delays, rules, volumes, volume
splitters, priors/likelihoods, and PID interfaces) are each built
around a base class with a family of interchangeable subclasses -- see
:doc:`intro`. New functionality should follow this pattern: add a
subclass of the relevant base class (`~bioscrape.types.Propensity`,
`~bioscrape.types.Delay`, `~bioscrape.types.Rule`,
`~bioscrape.types.Volume`, `~bioscrape.simulator.VolumeSplitter`,
`~bioscrape.inference.Distribution`, `~bioscrape.inference.Likelihood`,
`~bioscrape.pid_interfaces.PIDInterface`) rather than special-casing
new behavior into an existing class. This keeps each class focused on
one variant of its interface and keeps the package extensible without
requiring changes to unrelated code.


Documentation Guidelines
========================

Reference documentation (class and function descriptions, with
details on parameters) should all go in docstrings. User documentation
in more narrative form should be in the ``.rst`` files in ``docs/``,
where it can be incorporated into the User Guide.

Current state and target convention
-----------------------------------

As of this writing, docstrings in the codebase use **three different,
mutually incompatible conventions**:

* Sphinx field-list style (``:param x: ...``) in ``types.pyx`` and
  ``simulator.pyx`` -- renders correctly today with plain autodoc.
* Google style (``Args:``/``Returns:``) in ``analysis.py`` -- renders
  correctly today via ``sphinx.ext.napoleon`` (Google support is
  enabled by default).
* An ad hoc bullet-list style (`` * `param_name` : description ``) in
  ``pid_interfaces.py`` and most of ``inference.pyx`` -- **not**
  parsed by any Sphinx convention; renders as plain, unlinked bullet
  text.

Going forward, new and updated docstrings should follow the
**numpydoc** convention (as BioCRNpyler does), since this project and
BioCRNpyler share maintainers, contributors, and (increasingly)
audience:

* Python PEP 257 (docstrings): https://peps.python.org/pep-0257/
* Numpydoc Style guide: https://numpydoc.readthedocs.io/en/latest/format.html

Migrating the ad hoc bullet-style docstrings (``pid_interfaces.py``,
most of ``inference.pyx``) to numpydoc is the highest-priority
cleanup, since those currently render as unstructured text with no
parameter linking. The Sphinx field-list and Google-style docstrings
already render acceptably and can be migrated opportunistically.

General docstring info
----------------------

The guiding principle, consistent with the `numpydoc style guide
<https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_:

   A guiding principle is that human readers of the text are given
   precedence over contorting docstrings so our tools produce nice
   output.

* Use single backticks around all Python objects. This documentation
  sets Sphinx's ``default_role`` to ``py:obj``, so a single backtick
  renders in code form and links to the object's documentation if it
  exists.

  - Parameter names should also be in single backticks, even though
    they will not generate a link.

* Use double backticks for inline code, such as short Python
  fragments.

* Mathematical equations can be written using LaTeX syntax. Inline
  equations should be enclosed in a single set of dollar signs (``$``),
  with no space before or after (so ``$A + B --> C$``). The
  docstring preprocessor defined in ``conf.py`` (ported from
  BioCRNpyler) converts several plain-text substitutions inside
  equations for readability in raw docstrings:

  - ``-->`` becomes :math:`\rightarrow`
  - ``<-->`` becomes :math:`\rightleftharpoons`
  - ``...`` becomes :math:`\dots`
  - ``>>`` / ``<<`` become :math:`\gg` / :math:`\ll`
  - text in single quotes becomes upright text (e.g. for chemical
    species names inside an equation)

* Built-in Python objects (True, False, None) should be written with
  no backticks and properly capitalized.

* Strings used as arguments should be in single (forward) ticks
  (``'eval'``, ``'uniform'``) and do not need to be rendered as code.

Function docstrings
-------------------

Follow numpydoc format with the following additional details:

* All functions should have a short (< 64 character) summary line
  that starts with a capital letter and ends with a period.
* All parameter descriptions should start with a capital letter and
  end with a period.
* All parameters and keyword arguments must be documented.
* Include an "Examples" section for non-trivial functions, ideally in
  a form that can eventually be checked with ``make doctest``.

Class docstrings
----------------

Follow numpydoc format with the following additional details:

* Parameters used in creating an object should go in the class
  docstring, not the ``__init__`` docstring. Today, most bioscrape
  classes document their constructor arguments on ``__init__``
  instead -- ``conf.py`` sets ``autoclass_content = 'both'`` so both
  are shown in the meantime; this should be revisited once the
  docstrings move to the class docstring, at which point
  ``autoclass_content`` can switch to ``'class'`` to match
  BioCRNpyler.
* Parameters that are also attributes only need to be documented once.
* Attributes created within a class that are of interest to users
  should be documented in an "Attributes" section.
* Classes should not include a "Returns" section.
* Functions and attributes not intended for user access should start
  with an underscore (or, for Cython classes, be implemented as
  ``cdef`` rather than ``def``/``cpdef`` -- see "Build environment for
  the docs" above).

User Guide
----------

The purpose of the User Guide is to provide a *narrative* description
of the key functions of the package. It is not expected to cover every
command, but should allow someone familiar with stochastic simulation
and SBML to get up and running quickly.

Sphinx files guidelines:

* Each file should declare `currentmodule` at or near the top.
* Unlike docstrings, the documentation in the User Guide should use
  backticks and ``:math:`` more liberally when it helps to highlight
  or format code properly.

Reference Manual
----------------

The Reference Manual (:doc:`library`) should provide a reasonably
comprehensive listing of every user-facing class and function. It is
currently hand-written (grouped by defining module) rather than
auto-generated, since bioscrape's modules are large single files
(``types.pyx``, ``simulator.pyx``, ``inference.pyx``) rather than the
one-class-per-file layout BioCRNpyler's ``generate_library_docs.py``
script assumes. If the codebase is reorganized into smaller,
per-class files in the future, an equivalent auto-generation script
could be adopted.

Contributing and Releases
=========================

Releasing new versions
----------------------

Unlike BioCRNpyler, bioscrape does not currently use setuptools-scm;
the version is a static string in ``pyproject.toml``
(``project.version``). Package wheels/sdists are built and published
to PyPI via the manually-triggered ``pypi_release.yml`` GitHub Actions
workflow, and tests run on every push/PR to `master` via
``deploy_bioscrape.yml``. When cutting a release:

1. Ensure the working tree is clean and CI is green.
2. Update ``docs/`` as needed.
3. Bump ``project.version`` in ``pyproject.toml``.
4. Commit and push the version bump.
5. Run the ``PyPI Release`` workflow from GitHub Actions (manual
   ``workflow_dispatch`` trigger).
6. Verify from a fresh environment::

     python -m pip install -U Bioscrape
     python -c "import bioscrape"
