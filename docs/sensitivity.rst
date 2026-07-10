.. currentmodule:: bioscrape.analysis

.. _sensitivity_ref:

********************
Sensitivity Analysis
********************

.. todo::

   This chapter is a placeholder narrative overview.  Expand once the
   `~bioscrape.analysis` docstrings have been normalized (see
   :doc:`develop`).

Bioscrape can compute the local sensitivity of a model's trajectories
to its parameters, i.e. the coefficients
:math:`s_{ij} = \partial x_i / \partial p_j` at each simulated time
point, where :math:`x_i` is a state (species) and :math:`p_j` is a
parameter.  The user-facing entry point is
`~bioscrape.analysis.py_sensitivity_analysis`::

    from bioscrape.analysis import py_sensitivity_analysis
    import numpy as np

    timepoints = np.linspace(0, 100, 100)
    S = py_sensitivity_analysis(M, timepoints, normalize=False)

When `normalize=True`, each coefficient is divided by :math:`x_i /
p_j`, giving a dimensionless relative sensitivity.

Two lower-level helpers are also available for computing sensitivities
at a single point rather than along a full trajectory:

- `~bioscrape.analysis.py_get_jacobian`: the Jacobian :math:`\partial
  f/\partial x` of the model's right-hand side at a given state
- `~bioscrape.analysis.py_get_sensitivity_to_parameter`: the
  sensitivity :math:`\partial f/\partial p` to a single named
  parameter at a given state

Both `~py_sensitivity_analysis` and the two helper functions are
implemented on top of `~bioscrape.analysis.SensitivityAnalysis`, a
`~bioscrape.types.Model` subclass that adds finite-difference
computation of Jacobians and parameter sensitivities using a
deterministic simulation of the model.

.. autosummary::
   :nosignatures:

   SensitivityAnalysis
