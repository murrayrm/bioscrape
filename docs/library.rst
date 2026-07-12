*********************
The Bioscrape Library
*********************

This chapter contains reference documentation for the classes and
functions that make up the bioscrape package, grouped by the module
in which they are defined.  Unlike some sibling packages, bioscrape
does not re-export everything under a single flat top-level namespace,
so objects should be imported from their defining submodule (e.g.
``from bioscrape.types import Model``).

.. todo::

   Many of the docstrings referenced below are not yet in numpydoc
   format (see :doc:`develop`); the generated pages will render
   correctly but will look inconsistent (mixed ``Args:``/``:param:``
   styles) until that pass is done.

Model (bioscrape.types)
=======================

.. automodule:: bioscrape.types

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Model

Propensities
------------

Propensities define the rate law associated with a reaction.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Propensity
   ConstitutivePropensity
   UnimolecularPropensity
   BimolecularPropensity
   MassActionPropensity
   PositiveHillPropensity
   NegativeHillPropensity
   PositiveProportionalHillPropensity
   NegativeProportionalHillPropensity
   GeneralPropensity

Delays
------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Delay
   NoDelay
   FixedDelay
   GaussianDelay
   GammaDelay

Rules
-----

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Rule
   AdditiveAssignmentRule
   GeneralAssignmentRule
   GeneralODERule

Volume
------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Volume
   StochasticTimeThresholdVolume
   StateDependentVolume

Symbolic expression terms
-------------------------

These classes implement the internal parse-tree representation used
by `~bioscrape.types.GeneralPropensity` and
`~bioscrape.types.GeneralODERule` to evaluate arbitrary symbolic rate
expressions. They are not normally constructed directly by users.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Term
   ConstantTerm
   SpeciesTerm
   ParameterTerm
   VolumeTerm
   BinaryTerm
   SumTerm
   ProductTerm
   MaxTerm
   MinTerm
   PowerTerm
   ExpTerm
   LogTerm
   StepTerm
   AbsTerm
   TimeTerm

Simulation (bioscrape.simulator)
================================

.. automodule:: bioscrape.simulator

.. autosummary::
   :toctree: generated/
   :nosignatures:

   py_simulate_model

Simulators
----------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   RegularSimulator
   DeterministicSimulator
   SSASimulator
   DelaySimulator
   DelaySSASimulator
   VolumeSimulator
   VolumeSSASimulator
   DelayVolumeSimulator
   DelayVolumeSSASimulator

Simulation interfaces
---------------------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   CSimInterface
   ModelCSimInterface
   SafeModelCSimInterface

Results and cell state
----------------------

Returned by the simulator classes above; not normally constructed
directly by users.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   SSAResult
   DelaySSAResult
   VolumeSSAResult
   DelayVolumeSSAResult
   CellState
   DelayCellState
   VolumeCellState
   DelayVolumeCellState

Volume splitters and delay queues
---------------------------------

Used internally by the volume- and delay-aware simulators to
implement division and delayed-reaction scheduling.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   VolumeSplitter
   DelayVolumeSplitter
   PerfectBinomialVolumeSplitter
   GeneralVolumeSplitter
   PerfectBinomialDelayVolumeSplitter
   CustomSplitter
   DelayQueue
   ArrayDelayQueue

Inference (bioscrape.inference, bioscrape.inference_setup, bioscrape.pid_interfaces)
======================================================================================

.. automodule:: bioscrape.inference

.. autosummary::
   :toctree: generated/
   :nosignatures:

   py_inference

Data and likelihoods
--------------------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Data
   BulkData
   FlowData
   StochasticTrajectories
   Distribution
   UniformDistribution
   Likelihood
   ModelLikelihood
   DeterministicLikelihood
   StochasticTrajectoriesLikelihood
   StochasticTrajectoryMomentLikelihood
   StochasticStatesLikelihood

Parameter identification (PID) interfaces
-----------------------------------------

.. automodule:: bioscrape.pid_interfaces

.. autosummary::
   :toctree: generated/
   :nosignatures:

   PIDInterface
   StochasticInference
   DeterministicInference
   LMFitInference

Inference orchestration
------------------------

`~bioscrape.inference.py_inference` constructs and returns an
`~bioscrape.inference_setup.InferenceSetup`, which holds the model,
data, and settings for a run and provides
`~bioscrape.inference_setup.InferenceSetup.run_mcmc` and
`~bioscrape.inference_setup.InferenceSetup.run_lmfit` to perform it.

.. automodule:: bioscrape.inference_setup

.. autosummary::
   :toctree: generated/
   :nosignatures:

   initialize_inference
   InferenceSetup

Sensitivity Analysis (bioscrape.analysis)
=========================================

.. automodule:: bioscrape.analysis

.. autosummary::
   :toctree: generated/
   :nosignatures:

   py_sensitivity_analysis
   py_get_jacobian
   py_get_sensitivity_to_parameter
   SensitivityAnalysis

SBML Utilities (bioscrape.sbmlutil)
===================================

.. automodule:: bioscrape.sbmlutil

Helper functions used internally by `~bioscrape.types.Model` to
import and export SBML; most users will interact with these
indirectly through `Model(sbml_filename=...)` and
`~bioscrape.types.Model.write_sbml_model` rather than calling them
directly.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   read_model_from_sbml
   import_sbml
   create_sbml_model
   add_species
   add_parameter
   add_reaction
   add_rule
   SetIdFromNames

Lineage (bioscrape.lineage)
===========================

.. automodule:: bioscrape.lineage

Simulation entry points
-----------------------

Module-level functions for running lineage simulations; see
:doc:`lineage` for how they differ.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   py_SimulateCellLineage
   py_PropagateCells
   py_SingleCellLineage
   py_SimulateSingleCell
   py_SimulateTurbidostat
   py_set_up_InteractingLineage
   py_PropagateInteractingCells
   py_SimulateInteractingCellLineage

Population model and simulators
-------------------------------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   LineageModel
   LineageSSASimulator
   InteractingLineageSSASimulator
   LineageCSimInterface
   SafeLineageCSimInterface

Events and rules
----------------

Per-cell events (volume change, division, death) and the rules that
govern them.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   Event
   VolumeEvent
   LinearVolumeEvent
   MultiplicativeVolumeEvent
   GeneralVolumeEvent
   DivisionEvent
   DeathEvent
   LineageRule
   VolumeRule
   LinearVolumeRule
   MultiplicativeVolumeRule
   AssignmentVolumeRule
   ODEVolumeRule
   DivisionRule
   TimeDivisionRule
   VolumeDivisionRule
   DeltaVDivisionRule
   GeneralDivisionRule
   DeathRule
   SpeciesDeathRule
   ParamDeathRule
   GeneralDeathRule

Results and internals
---------------------

.. autosummary::
   :toctree: generated/
   :nosignatures:

   SingleCellSSAResult
   LineageVolumeCellState
   LineageVolumeSplitter
   CappedStateQueue
