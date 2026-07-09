.. currentmodule:: bioscrape

************
Introduction
************

This chapter provides a brief introduction to bioscrape.

.. todo::

   This chapter is a placeholder.  Expand with a proper motivation and
   overview section once the reference documentation (docstrings) has
   been normalized -- see :doc:`develop` for the plan.

Motivation and Background
==========================

Bioscrape ("Biological Stochastic Simulation of Single Cell Reactions
and Parameter Estimation") is a Python package, written in Cython for
performance, for simulating and fitting chemical reaction network
(CRN) models of biological systems.  It reads models from the Systems
Biology Markup Language (SBML) or from a native model-building API,
and simulates them deterministically (ODE) or stochastically
(Gillespie's Stochastic Simulation Algorithm), including support for
delayed reactions and cell volume/lineage dynamics.  Bioscrape also
provides Bayesian parameter inference tools for fitting model
parameters to experimental data.

Bioscrape is designed to be usable on its own, or as the simulation
and inference back end for higher-level model-construction tools such
as `BioCRNpyler <https://biocrnpyler.readthedocs.io/en/latest/>`_,
which compiles high-level circuit specifications into SBML models that
can be simulated directly with bioscrape.

The Bioscrape Framework
=========================

Bioscrape is organized around a small number of core concepts:

**Models** (:class:`~bioscrape.types.Model`) hold the species,
reactions, propensities, parameters, rules, and (optionally) delays
that define a CRN.  Models can be constructed programmatically or
loaded from SBML.  See :doc:`model` for details.

**Simulators** (:mod:`bioscrape.simulator`) take a model and produce
simulated trajectories, either deterministically or stochastically,
with optional support for reaction delays and dividing-cell volume
dynamics.  See :doc:`simulation`.

**Inference** (:mod:`bioscrape.inference`,
:mod:`bioscrape.pid_interfaces`) fits model parameters to experimental
data (bulk, flow cytometry, or single-cell trajectories) using
Bayesian (MCMC) methods, with a library of built-in priors and
likelihood functions. See :doc:`inference`.

**Sensitivity Analysis** (:mod:`bioscrape.analysis`) computes the
local sensitivity of simulated trajectories to model parameters. See
:doc:`sensitivity`.

**Lineage** (:mod:`bioscrape.lineage`) extends the simulation
machinery to populations of dividing and interacting cells. See
:doc:`lineage`.

Documentation Conventions
===========================

This documentation follows the same conventions as `BioCRNpyler's
documentation
<https://biocrnpyler.readthedocs.io/en/latest/intro.html#documentation-conventions>`_,
which bioscrape shares maintainers and code style with:

* The left panel displays the table of contents, divided into the
  User Guide (a narrative description of the package with examples)
  and the Reference Manual (documentation for all classes, functions,
  and other detailed information).

* Classes, functions, and methods with additional documentation appear
  in a bold, code font that links to the Reference Manual. Example:
  `~bioscrape.types.Model`.

* Links to other sections appear in blue. Example: :doc:`model`.

* Parameters appear in a (non-bold) code font, as do code fragments.

* Example code is contained in code blocks that can be copied using
  the copy icon in the top right corner of the code block.
