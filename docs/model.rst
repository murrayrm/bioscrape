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
   :toctree: generated/
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

Exporting to SBML
=================

A `Model` can be exported back to SBML with `~Model.write_sbml_model`,
or converted to an in-memory SBML document with
`~Model.generate_sbml_model`.  See also :mod:`bioscrape.sbmlutil` for
the lower-level SBML import/export helpers used internally.
