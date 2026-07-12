.. currentmodule:: bioscrape.types

.. _model_ref:

*****
Model
*****

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

For example, the following builds a simple birth-death model in which
a species ``X`` is produced at a constant rate and degrades in a
first-order reaction::

    from bioscrape.types import Model

    M = Model()
    # Constitutive production of X (zero reactants, one product)
    M.create_reaction(reactants=[], products=['X'],
                      propensity_type='massaction',
                      propensity_param_dict={'k': 'k_prod'})
    # First-order degradation of X (one reactant, no products)
    M.create_reaction(reactants=['X'], products=[],
                      propensity_type='massaction',
                      propensity_param_dict={'k': 'k_deg'})
    M.set_parameter('k_prod', 10.0)
    M.set_parameter('k_deg', 0.5)
    M.set_species({'X': 0})

Species are added automatically as they are referenced in reactions,
so they do not need to be declared separately; `~Model.set_species`
sets their initial values (any species left unset defaults to 0).
The model can then be simulated directly (see :doc:`simulation`)::

    from bioscrape.simulator import py_simulate_model
    import numpy as np

    result = py_simulate_model(np.linspace(0, 20, 100), Model=M)

The value supplied for a key in a propensity or delay parameter
dictionary may be given either way: as the *name* of a model parameter
(a string, whose value is set separately) or as a literal *number*.
A literal number is turned into an automatically-named parameter set
to that value, so both ``{'k': 'k_tx'}`` and ``{'k': 2.0}`` are valid
-- the first refers to a parameter ``k_tx`` you define elsewhere, and
the second creates a fixed-value parameter for you.

.. note::

   Species and parameter names should be alphanumeric (underscores are
   allowed) and begin with a letter.  The names ``t`` and ``volume``
   are reserved for the simulation time and the cell volume: a species
   or parameter named either one is treated as that keyword rather than
   as its own quantity.  For the same reason, avoid the function names
   used by general propensities (``exp``, ``log``, ``Abs``, ``Max``,
   ``Min``, ``heaviside``) as species or parameter names.

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

The ``propensity_type`` string passed to `~Model.create_reaction`
(or `~Model.create_propensity`) selects the rate law, and the
accompanying ``propensity_param_dict`` supplies its parameters:

.. list-table::
   :header-rows: 1
   :widths: 24 32 30

   * - ``propensity_type``
     - Rate
     - ``propensity_param_dict`` keys
   * - 'massaction'
     - :math:`k \prod_i x_i`
     - `k` (reactant species are taken from the reaction's reactant
       list)
   * - 'hillpositive'
     - :math:`k (x_1/K)^n / (1 + (x_1/K)^n)`
     - `k`, `K`, `n`, `s1`
   * - 'hillnegative'
     - :math:`k / (1 + (x_1/K)^n)`
     - `k`, `K`, `n`, `s1`
   * - 'proportionalhillpositive'
     - :math:`k\, d\, (x_1/K)^n / (1 + (x_1/K)^n)`
     - `k`, `K`, `n`, `s1`, `d`
   * - 'proportionalhillnegative'
     - :math:`k\, d / (1 + (x_1/K)^n)`
     - `k`, `K`, `n`, `s1`, `d`
   * - 'general'
     - arbitrary expression
     - `rate`

Here `s1` names the Hill input species $x_1$, `K` is its half-maximal
constant $K$, `n` the Hill coefficient, and `d` a second species that
the proportional Hill rates scale linearly with (e.g. an enzyme or
polymerase).  For a mass-action reaction the reactant species are read
from the reaction's reactant list, so only `k` needs to be given in
the parameter dictionary; a species that appears more than once (e.g.
a dimerization with reactants ``['A', 'A']``) contributes the expected
combinatorial factor $x(x-1)\cdots$ in stochastic simulations.

General propensities
--------------------

`~bioscrape.types.GeneralPropensity` (``propensity_type='general'``)
lets the rate be an arbitrary symbolic expression of species,
parameters, numbers, ``t`` (the current simulation time), and
``volume`` (the current cell volume; see :doc:`simulation`), supplied
as a string under the `rate` key and parsed with SymPy.  In addition
to the usual arithmetic operators (``+ - * /`` and ``**`` or ``^`` for
exponentiation), the following functions are available:

- ``exp(x)`` and ``log(x)`` (natural exponential and logarithm),
- ``heaviside(x)`` (the step function: 1 when ``x >= 0`` and 0
  otherwise),
- ``Abs(x)`` (absolute value), and
- ``Max(x, y, ...)`` and ``Min(x, y, ...)``.

Capitalization matters: ``Abs``, ``Max``, and ``Min`` must be
capitalized as shown, while ``exp``, ``log``, and ``heaviside`` are
lowercase.  Because the expression can reference ``t``, general
propensities can encode explicitly time-dependent rates -- for
example, 'heaviside(t - 60) * beta' describes a reaction that is
off until time 60 and then fires at the constant rate ``beta``.

General propensities are the most flexible option but are somewhat
slower to evaluate than the built-in mass-action and Hill rates, so
prefer a specific type when one applies.

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

Importing and Exporting SBML
============================

Passing ``sbml_filename`` to the `Model` constructor (as shown above)
reads a model's species, parameters, reactions, and assignment rules
from an SBML file.  Because SBML is a large and general standard while
bioscrape models only a subset of it, the import has some limitations
to be aware of:

- *Delays* are not part of standard SBML.  Bioscrape records the
  delays in its own models using a bioscrape-specific annotation when
  writing SBML, and reads them back on import, so a bioscrape model
  with delays round-trips through SBML correctly; but a generic SBML
  file from another tool will not carry any delays.
- *Events, compartments, and unit definitions* are not represented
  in a bioscrape `Model`.  They are ignored on import (a warning is
  issued unless the model appears to have been written by bioscrape or
  BioCRNpyler).  In particular, a model with more than one compartment,
  or a changing compartment volume, is imported as if it had a single
  fixed volume.
- Only *assignment rules* are imported; algebraic and other SBML rule
  types are skipped with a warning.
- Each reaction's rate law must be parseable by SymPy.  Rates with the
  appropriate bioscrape annotation are imported as their specific
  propensity type (e.g. a Hill function); any other rate is imported as
  a general propensity, which requires that its formula parse cleanly
  (standard arithmetic and the functions listed under `General
  propensities`_ above).
- A species' initial value is taken from its ``initialAmount`` when
  that is set and nonzero, and otherwise from its
  ``initialConcentration``.

.. note::

   `BioCRNpyler <https://biocrnpyler.readthedocs.io/en/latest/>`_ has a
   notion of compartments, which can make bioscrape's lack of one
   confusing.  BioCRNpyler represents a species' compartment by
   appending the compartment's name to the species name, so a species
   ``X`` in the cytoplasm and an ``X`` in the membrane become two
   distinct species (``X_cytoplasm`` and ``X_membrane``).  When
   BioCRNpyler writes SBML it does also emit SBML ``<compartment>``
   elements, but because bioscrape drops those on import, it is these
   distinct species names that carry the compartmentalization through.
   A compartmentalized BioCRNpyler model therefore simulates in
   bioscrape as an ordinary model whose compartment-tagged species are
   treated as independent species: the species stay separate, but the
   compartments' sizes and geometry are not represented, and bioscrape
   applies no compartment-based rate scaling.

A `Model` can be exported back to SBML with `~Model.write_sbml_model`,
or converted to an in-memory SBML document with
`~Model.generate_sbml_model`.  See also :mod:`bioscrape.sbmlutil` for
the lower-level SBML import/export helpers used internally.
