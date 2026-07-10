.. currentmodule:: bioscrape.types

.. _model_ref:

*****
Model
*****

.. todo::

   This chapter is a placeholder narrative overview.  Expand once
   :class:`~bioscrape.types.Model`'s docstrings have been normalized
   (see :doc:`develop`).  Code examples below are illustrative and not
   yet verified with ``make doctest``.

The central object in bioscrape is :class:`~bioscrape.types.Model`,
which holds everything needed to describe a chemical reaction network:
species, reactions (with their propensities), parameters, rules, and
(optionally) delays.

Loading and Building Models
===========================

A `Model` can be constructed from an SBML file::

    from bioscrape.types import Model
    M = Model(sbml_filename='repressilator_sbml.xml')

or built up programmatically by passing species, reactions,
parameters, and rules directly to the constructor, or by calling
methods such as `~Model.create_reaction`, `~Model.create_parameter`,
and `~Model.create_rule` after construction.

Inspecting a Model
==================

Once a `Model` is constructed, its contents can be inspected using a
family of accessor methods, including:

- `~Model.get_species_list` and `~Model.get_species_dictionary`:
  the species in the model and their current values
- `~Model.get_param_list` and `~Model.get_parameter_dictionary`:
  the parameters in the model and their current values
- `~Model.get_reactions` and `~Model.get_reaction_strings`:
  the reactions in the model
- `~Model.get_propensities` and `~Model.get_delays`:
  the propensity and delay objects associated with each reaction
- `~Model.get_rules`: the rules (assignment/ODE rules) in the model

Parameter and species values can be set with `~Model.set_params` and
`~Model.set_species`, respectively.

Propensities
============

Each reaction in a `Model` has an associated `~bioscrape.types.Propensity`
object describing its rate law.  Bioscrape includes several built-in
propensity types, including:

.. autosummary::
   :nosignatures:

   MassActionPropensity
   PositiveHillPropensity
   NegativeHillPropensity
   PositiveProportionalHillPropensity
   NegativeProportionalHillPropensity
   GeneralPropensity

`~bioscrape.types.GeneralPropensity` allows an arbitrary symbolic
expression (parsed with SymPy) to be used as a propensity function.

Rules and Delays
================

`~bioscrape.types.Rule` objects implement assignment and ODE rules
that update species or parameters outside of the reaction network
(e.g. `~bioscrape.types.AdditiveAssignmentRule`,
`~bioscrape.types.GeneralODERule`).

`~bioscrape.types.Delay` objects implement stochastic reaction delays
(e.g. `~bioscrape.types.FixedDelay`,
`~bioscrape.types.GaussianDelay`, `~bioscrape.types.GammaDelay`) used
by the delayed simulators described in :doc:`simulation`.

A delay is attached to a reaction through `~Model.create_reaction`'s
`delay_type`, `delay_reactants`, `delay_products`, and
`delay_param_dict` arguments, rather than through a separate object.
The reaction's ordinary `reactants`/`products` fire immediately (as
usual); the `delay_reactants`/`delay_products` fire `delay_type` time
units later.  For example, a delayed transcription reaction -- where
mRNA appears a fixed time after the reaction "starts" rather than
immediately, following the gene expression model in [Pan+23]_ --
can be built as follows::

    from bioscrape.types import Model

    M = Model()
    M.create_reaction(
        reactants=[], products=[],
        propensity_type='massaction', propensity_param_dict={'k': 'beta'},
        delay_type='fixed', delay_reactants=[], delay_products=['mRNA'],
        delay_param_dict={'delay': 'tx_delay'})
    M.create_reaction(
        reactants=['mRNA'], products=[],
        propensity_type='massaction', propensity_param_dict={'k': 'delta'})
    M.set_parameter('beta', 2)
    M.set_parameter('delta', 0.2)
    M.set_parameter('tx_delay', 10)
    M.set_species({'mRNA': 0})

The first reaction has no immediate reactants or products; the gene
itself is not modeled as a species, so its (constant) copy number is
absorbed into the rate constant `beta`, and the only effect is that
`mRNA` is produced `tx_delay` time units after each firing.  The
second reaction is an ordinary (undelayed) first-order degradation of
`mRNA`.  Since delay simulations are always stochastic, simulate this
model with `delay=True` (see :doc:`simulation`)::

    from bioscrape.simulator import py_simulate_model
    import numpy as np

    timepoints = np.linspace(0, 50, 200)
    result = py_simulate_model(timepoints, Model=M, stochastic=True, delay=True)

.. [Pan+23] Pandey A, Poole W, Swaminathan A, Hsiao V, Murray RM (2023)
   Fast and flexible simulation and parameter estimation for synthetic
   biology using bioscrape. *Journal of Open Source Software* 8(83):5057.
   https://doi.org/10.21105/joss.05057

Exporting to SBML
=================

A `Model` can be exported back to SBML with `~Model.write_sbml_model`,
or converted to an in-memory SBML document with
`~Model.generate_sbml_model`.  See also :mod:`bioscrape.sbmlutil` for
the lower-level SBML import/export helpers used internally.
