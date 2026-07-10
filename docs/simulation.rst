.. currentmodule:: bioscrape.simulator

.. _simulation_ref:

**********
Simulation
**********

.. todo::

   This chapter is a placeholder narrative overview.  Expand once the
   simulator docstrings have been normalized (see :doc:`develop`).

The simplest way to simulate a :class:`~bioscrape.types.Model` is the
`~bioscrape.simulator.py_simulate_model` convenience function, which
selects and configures the appropriate simulator based on its keyword
arguments::

    from bioscrape.simulator import py_simulate_model
    import numpy as np

    timepoints = np.linspace(0, 256, 100)
    result = py_simulate_model(timepoints, Model=M, stochastic=True)

By default `~py_simulate_model` returns a `pandas.DataFrame` indexed
by species and parameter name; pass `return_dataframe=False` to get
the underlying result object instead (e.g.
`~bioscrape.simulator.SSAResult`).

Deterministic vs. Stochastic Simulation
=======================================

- `stochastic=False` (default) runs a deterministic (ODE)
  simulation via `~bioscrape.simulator.DeterministicSimulator`
  (using :func:`scipy.integrate.odeint`).
- `stochastic=True` runs a stochastic simulation using Gillespie's
  Stochastic Simulation Algorithm via
  `~bioscrape.simulator.SSASimulator`.

Delayed Reactions
=================

Passing `delay=True` selects a delay-aware simulator
(`~bioscrape.simulator.DelaySSASimulator`), which uses a
`~bioscrape.simulator.DelayQueue` to schedule the completion of
delayed reactions (see the `~bioscrape.types.Delay` classes described
in :doc:`model`).

Volume and Lineage Simulation
=============================

Passing `volume=True` enables cell-volume tracking, used for
simulating growing and dividing cells (see
`~bioscrape.simulator.VolumeSSASimulator`,
`~bioscrape.simulator.DelayVolumeSSASimulator`, and the
`~bioscrape.simulator.VolumeSplitter` classes that determine how
species partition between daughter cells at division).  Full
population-level lineage tracking is provided by the
:mod:`bioscrape.lineage` subpackage; see :doc:`lineage`.

Simulator Classes
=================

.. autosummary::
   :toctree: generated/
   :nosignatures:

   DeterministicSimulator
   SSASimulator
   DelaySSASimulator
   VolumeSSASimulator
   DelayVolumeSSASimulator

Simulation Interfaces
=====================

`~bioscrape.simulator.CSimInterface` and its subclasses
(`~bioscrape.simulator.ModelCSimInterface`,
`~bioscrape.simulator.SafeModelCSimInterface`) adapt a
`~bioscrape.types.Model` into the low-level form used internally by
the simulators.  Most users will not need to construct these directly
-- `~py_simulate_model` creates one automatically -- but they can be
reused across repeated simulations of the same model for performance
(the `Interface` keyword argument), or replaced with a
`~bioscrape.simulator.SafeModelCSimInterface` (via `safe=True`) to get
warnings about ill-conditioned situations such as negative
propensities.
