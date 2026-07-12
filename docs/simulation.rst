.. currentmodule:: bioscrape.simulator

.. _simulation_ref:

**********
Simulation
**********

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

The two agree on average but not trajectory-by-trajectory: for the
birth-death model built in :doc:`model`, a single stochastic
trajectory fluctuates around the deterministic solution rather than
following it exactly, with fluctuations that are largest (relative to
the mean) when molecule counts are small:

.. plot::

    from bioscrape.types import Model
    from bioscrape.simulator import py_simulate_model
    import numpy as np
    import matplotlib.pyplot as plt
    import bioscrape.random
    bioscrape.random.py_seed_random(0)

    M = Model()
    M.create_reaction(reactants=[], products=['X'],
                      propensity_type='massaction',
                      propensity_param_dict={'k': 'k_prod'})
    M.create_reaction(reactants=['X'], products=[],
                      propensity_type='massaction',
                      propensity_param_dict={'k': 'k_deg'})
    M.set_parameter('k_prod', 10.0)
    M.set_parameter('k_deg', 0.5)
    M.set_species({'X': 0})

    timepoints = np.linspace(0, 40, 200)
    det = py_simulate_model(timepoints, Model=M, stochastic=False)
    sto = py_simulate_model(timepoints, Model=M, stochastic=True)

    plt.plot(timepoints, sto['X'], color='0.6', label='Stochastic (SSA)')
    plt.plot(timepoints, det['X'], lw=2, label='Deterministic (ODE)')
    plt.xlabel('Time')
    plt.ylabel('X')
    plt.legend()

Delayed Reactions
=================

Passing `delay=True` selects a delay-aware simulator
(`~bioscrape.simulator.DelaySSASimulator`), which uses a
`~bioscrape.simulator.DelayQueue` to schedule the completion of
delayed reactions (see the `~bioscrape.types.Delay` classes described
in :doc:`model`).

Delay changes the shape of the dynamics, not just their timing:
without delay, a reaction's products can appear as soon as the
reaction fires, but with delay, nothing changes until the first
delayed products complete, after which the delayed trajectory
resembles the undelayed one shifted forward in time.  For the delayed
transcription model built in :doc:`model`, comparing simulations of
the same model with and without delay makes this visible directly:

.. plot::

    from bioscrape.types import Model
    from bioscrape.simulator import py_simulate_model
    import numpy as np
    import matplotlib.pyplot as plt
    import bioscrape.random

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

    timepoints = np.linspace(0, 50, 200)

    # Re-seeding before each run means both share the same sequence of
    # reaction firings, isolating the effect of the delay itself.
    bioscrape.random.py_seed_random(0)
    no_delay = py_simulate_model(timepoints, Model=M, stochastic=True, delay=False)
    bioscrape.random.py_seed_random(0)
    with_delay = py_simulate_model(timepoints, Model=M, stochastic=True, delay=True)

    plt.plot(timepoints, no_delay['mRNA'], label='No delay')
    plt.plot(timepoints, with_delay['mRNA'], label='Fixed delay = 10')
    plt.xlabel('Time')
    plt.ylabel('mRNA')
    plt.legend()

`~py_simulate_model` builds and manages the delay queue for you, so
most users never touch it directly.  When constructing a simulation by
hand (or when the initial state includes reactions that are already
"in flight"), the queue is an
`~bioscrape.simulator.ArrayDelayQueue`, created with::

    from bioscrape.simulator import ArrayDelayQueue

    q = ArrayDelayQueue.setup_queue(num_reactions, queue_length, dt)

This tracks queued reactions up to ``dt * queue_length`` time units
into the future, on a grid of spacing `dt`.  Smaller `dt` gives finer
timing of delayed reactions but uses more memory and runs more slowly
(the cost is most noticeable in lineage simulations with cell
division), so choose `dt` for the accuracy you need and then
`queue_length` large enough that ``dt * queue_length`` covers the
longest delay in the model.  Because the initial state of a delayed
simulation includes any reactions already queued to fire, you can
pre-load such reactions with
``q.py_add_reaction(time, reaction_id, amount)``, where `reaction_id`
indexes the reaction in the model's stoichiometry and `amount` is the
number of firings scheduled at `time`.

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

Volume-dependent rates
----------------------

When a volume is present, species are counts of molecules but the
reaction rates depend on their *concentrations*, so bioscrape rescales
the propensities by the current volume $V$.  This happens automatically
when `volume=True`; you write the same rate laws as in a volumeless
simulation, and the following adjustments are applied under the hood:

- A *zeroth-order* (constitutive) mass-action rate scales as $V$: a
  fixed concentration of product is made per unit time, so the number
  of molecules produced grows with the cell.
- A *first-order* (unimolecular) mass-action rate is unchanged: it
  depends only on the count of the single reactant.
- A *second-order* (bimolecular) mass-action rate scales as $1/V$:
  two molecules are less likely to find each other in a larger volume.
- More generally, an $n$-th order mass-action rate scales as
  $1/V^{\,n-1}$.
- In a *Hill* propensity, the input species count is divided by $V$,
  i.e. the rate is computed from the species' *concentration* rather
  than its count, because it is the concentration that sets the
  equilibrium binding (for example of a transcription factor to a
  promoter).

Because these conversions are automatic, a rate constant fit or chosen
for a volumeless simulation may need to be re-scaled when the same
model is simulated with a volume, and vice versa.

Checking a Stochastic Simulation
================================

For a simple enough model, the stochastic simulator's output can be
checked directly against a known analytical result, which is a useful
way to build confidence in a new model or a modified reaction network.
The birth-death model above is a textbook example: at steady state,
its species count `X` follows a Poisson distribution with mean and
variance both equal to `k_prod` / `k_deg` [Pan+23c]_.  Simulating it
stochastically for long enough, and comparing the distribution of `X`
values (after discarding an initial transient) against that Poisson
distribution, confirms that bioscrape's SSA implementation reproduces
the expected statistics:

.. plot::

    from bioscrape.types import Model
    from bioscrape.simulator import py_simulate_model
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import poisson
    import bioscrape.random
    bioscrape.random.py_seed_random(0)

    M = Model()
    M.create_reaction(reactants=[], products=['X'],
                      propensity_type='massaction',
                      propensity_param_dict={'k': 'k_prod'})
    M.create_reaction(reactants=['X'], products=[],
                      propensity_type='massaction',
                      propensity_param_dict={'k': 'k_deg'})
    M.set_parameter('k_prod', 10.0)
    M.set_parameter('k_deg', 0.5)
    M.set_species({'X': 0})

    timepoints = np.linspace(0, 2000, 20000)
    result = py_simulate_model(timepoints, Model=M, stochastic=True)
    X = result['X'].values

    # Discard the transient before the distribution reaches steady state.
    X_steady_state = X[timepoints > 200].astype(int)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.plot(timepoints[timepoints < 100], X[timepoints < 100])
    ax1.set_xlabel('Time')
    ax1.set_ylabel('X')
    ax1.set_title('Stochastic trajectory')

    counts = np.bincount(X_steady_state)
    xs = np.arange(len(counts))
    ax2.bar(xs, counts / counts.sum(), color='0.7', label='Empirical')
    ax2.plot(xs, poisson.pmf(xs, mu=10.0 / 0.5), lw=2, label='Poisson(20)')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Probability')
    ax2.set_title('Steady-state distribution')
    ax2.legend()

    plt.tight_layout()

`~bioscrape.simulator.SSAResult` provides some of this analysis
directly, including `~bioscrape.simulator.SSAResult.py_first_moment`
and `~bioscrape.simulator.SSAResult.py_correlations` for computing
means and correlations from a simulated trajectory without the manual
post-processing shown above.  For a more complete worked example,
including statistics of a multi-species model, see the *Fast
Statistics for SSA Trajectories* notebook in :doc:`tutorials`.

.. [Pan+23c] Pandey A, Poole W, Swaminathan A, Hsiao V, Murray RM (2023)
   Fast and flexible simulation and parameter estimation for synthetic
   biology using bioscrape. *Journal of Open Source Software* 8(83):5057.
   https://doi.org/10.21105/joss.05057

Simulator Classes
=================

.. autosummary::
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
