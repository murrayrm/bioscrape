.. currentmodule:: bioscrape.lineage

.. _lineage_ref:

*******
Lineage
*******

.. todo::

   This chapter is a placeholder narrative overview.  Expand once the
   `~bioscrape.lineage` docstrings have been normalized (see
   :doc:`develop`).  Note that ``lineage`` is currently an optional,
   separately-installed extension (``python setup.py install lineage``)
   -- see :doc:`develop` for build notes.

The :mod:`bioscrape.lineage` subpackage extends bioscrape's simulation
machinery to populations of growing and dividing cells, tracking the
full lineage tree of a population over time.

`~bioscrape.lineage.LineageModel` extends
`~bioscrape.types.Model` with volume dynamics and three kinds of
per-cell events, each governed by a corresponding rule class:

- **Volume events/rules** (`~VolumeEvent`, `~LinearVolumeRule`,
  `~MultiplicativeVolumeRule`, `~AssignmentVolumeRule`,
  `~ODEVolumeRule`) describe how a cell's volume changes over time.
- **Division events/rules** (`~DivisionEvent`, `~TimeDivisionRule`,
  `~VolumeDivisionRule`, `~DeltaVDivisionRule`,
  `~GeneralDivisionRule`) describe when a cell divides into two
  daughters, and (via `~LineageVolumeSplitter` and its subclasses in
  :mod:`bioscrape.simulator`) how species and volume partition between
  them.
- **Death events/rules** (`~DeathEvent`, `~SpeciesDeathRule`,
  `~ParamDeathRule`, `~GeneralDeathRule`) describe when a cell is
  removed from the simulation.

Simulation of a `~LineageModel` is carried out by
`~bioscrape.lineage.LineageSSASimulator`, which produces a
`~bioscrape.lineage.SingleCellSSAResult` per cell and assembles the
full population lineage.
`~bioscrape.lineage.InteractingLineageSSASimulator` extends this to
populations of cells that can interact with one another (e.g. through
a shared extracellular environment).

Key Classes
===========

.. autosummary::
   :toctree: generated/
   :nosignatures:

   LineageModel
   LineageSSASimulator
   InteractingLineageSSASimulator
   SingleCellSSAResult
