.. currentmodule:: bioscrape.inference

.. _inference_ref:

*********
Inference
*********

Bioscrape can estimate model parameters from experimental data using
Bayesian (Markov Chain Monte Carlo) inference, implemented as a
wrapper around `emcee <https://emcee.readthedocs.io/>`_.  The
user-facing entry point is
`~bioscrape.inference.py_inference`::

    from bioscrape.types import Model
    from bioscrape.inference import py_inference
    import pandas as pd

    M = Model(sbml_filename='toy_sbml_model.xml')
    df = pd.read_csv('test_data.csv', delimiter='\t',
                      names=['X', 'time'], skiprows=1)

    prior = {'d1': ['gaussian', 0.2, 20, 'positive'],
             'k1': ['uniform', 0, 100]}

    sampler, pid = py_inference(
        Model=M, exp_data=df, measurements=['X'], time_column=['time'],
        nwalkers=20, nsteps=5500, params_to_estimate=['d1', 'k1'],
        prior=prior)

`~py_inference` returns the `emcee` sampler object (containing the
full set of MCMC samples) along with an
`~bioscrape.inference_setup.InferenceSetup` object -- the object that
orchestrates the run and, internally, owns the appropriate
`~bioscrape.pid_interfaces.PIDInterface` -- a parameter identification
(PID) interface -- for the requested `sim_type` (described below).
Unless `plot_show=False` is passed,
`~py_inference` also produces plots of the resulting posterior
parameter distributions, and it always writes the raw MCMC samples and
a summary of the fit to ``mcmc_results.csv`` and ``mcmc_results.txt``
in the current directory; pass `filename_csv`/`filename_txt` to write
them elsewhere.

A Worked Example: Fitting a Line to Noisy Data
==============================================

The following is a self-contained, runnable version of the pattern
above, adapted from `emcee's own line-fitting tutorial
<https://emcee.readthedocs.io/en/stable/tutorials/line/>`_: a
one-species bioscrape `Model` defines the line ``y = m*t + b`` as an
assignment rule, some noisy synthetic data is generated from known
"true" parameters, and `~py_inference` is used to recover them.  By
default, `~py_inference` shows two diagnostic plots: the MCMC chains
for each parameter (to check that the walkers have mixed rather than
being stuck away from the rest), and a corner plot of the marginal and
pairwise posterior distributions (using the
`corner <https://corner.readthedocs.io/>`_ package):

.. plot::

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import tempfile, os
    from bioscrape.types import Model
    from bioscrape.inference import py_inference

    np.random.seed(123)
    m_true, b_true = -0.9594, 4.294

    M = Model(species=['y'], parameters={'m': m_true, 'b': b_true},
              rules=[('assignment', {'equation': 'y = m*t + b'})],
              initial_condition_dict={'y': 0})

    # Generate synthetic data from the true line, with noise.
    N = 50
    x = np.sort(10 * np.random.rand(N))
    yerr = 0.1 + 0.6 * np.random.rand(N)
    y = m_true * x + b_true + yerr * np.random.randn(N)
    exp_data = pd.DataFrame({'x': x, 'y': y})

    # Write the (always-written) results files to a temporary
    # directory instead of the current directory; see the note above.
    csv_path = os.path.join(tempfile.gettempdir(), 'mcmc_results.csv')
    txt_path = os.path.join(tempfile.gettempdir(), 'mcmc_results.txt')

    prior = {'m': ['gaussian', m_true, 500], 'b': ['gaussian', b_true, 1000]}
    sampler, pid = py_inference(
        Model=M, exp_data=exp_data, measurements=['y'], time_column=['x'],
        params_to_estimate=['m', 'b'], prior=prior, sim_type='deterministic',
        nwalkers=16, nsteps=500, discard=100, init_seed=1e-4,
        filename_csv=csv_path, filename_txt=txt_path)

    # The flattened, post-burn-in chain gives the recovered parameters.
    flat_samples = sampler.get_chain(discard=100, flat=True)
    m_fit, b_fit = flat_samples.mean(axis=0)

    plt.figure(figsize=(6, 4))
    plt.errorbar(x, y, yerr=yerr, fmt='.', color='0.5', label='Synthetic data')
    xs = np.linspace(0, 10, 100)
    plt.plot(xs, m_true * xs + b_true, 'k--', label='True line')
    plt.plot(xs, m_fit * xs + b_fit, lw=2, label='Recovered fit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

Data Types
==========

Experimental data is held in one of the `~bioscrape.inference.Data`
subclasses, each corresponding to one of the three kinds of
measurement commonly made on a gene circuit:

.. list-table::
   :header-rows: 1
   :widths: 26 22 52

   * - Data class
     - Measurement
     - Description
   * - `~bioscrape.inference.BulkData`
     - Bulk time series
     - A single output measured for a whole culture over time (e.g.
       total fluorescence or optical density from a plate reader),
       where the measured value is effectively summed or averaged over
       all the cells.
   * - `~bioscrape.inference.FlowData`
     - Population snapshot
     - A *distribution* of single-cell outputs at one or more time
       points, with individual cells not tracked from one time point
       to the next (e.g. flow cytometry or mRNA FISH).
   * - `~bioscrape.inference.StochasticTrajectories`
     - Single-cell time series
     - One or more individual cells tracked over time (e.g. time-lapse
       microscopy).

These carry progressively more information: a time series can be
treated as a set of snapshots by ignoring the time ordering, and a
snapshot can be reduced to a bulk value by taking its mean.  The type
of data you have should also guide the choice of model -- if all you
have is bulk data, for instance, a deterministic model may describe it
adequately and a stochastic single-cell model may be unnecessary.

When using the high-level `~py_inference` entry point, the `sim_type`
argument selects the data type and likelihood together:
``sim_type='deterministic'`` (the default) uses
`~bioscrape.inference.BulkData` with
`~bioscrape.inference.DeterministicLikelihood`, and
``sim_type='stochastic'`` uses
`~bioscrape.inference.StochasticTrajectories` with
`~bioscrape.inference.StochasticTrajectoriesLikelihood`.  The other
data and likelihood classes -- population-snapshot
`~bioscrape.inference.FlowData` and the moment-matching likelihood
described below -- are used by constructing the likelihood objects
directly rather than through `~py_inference`.

Likelihoods
===========

Each `~bioscrape.inference.Data` type is paired with a
`~bioscrape.inference.Likelihood` implementation that computes the
log-likelihood of a parameter set given the data:

.. autosummary::
   :nosignatures:

   DeterministicLikelihood
   StochasticTrajectoriesLikelihood
   StochasticTrajectoryMomentLikelihood
   StochasticStatesLikelihood

They differ in what they compare and therefore in the kind of data
they suit:

- `~bioscrape.inference.DeterministicLikelihood` compares a single
  deterministic (ODE) simulation against bulk time-series data.
- `~bioscrape.inference.StochasticTrajectoriesLikelihood` runs several
  stochastic simulations (see the `N_simulations` option) and scores
  how close the simulated single-cell trajectories are to the measured
  ones.  This is the likelihood used when `~py_inference` is called
  with ``sim_type='stochastic'``.
- `~bioscrape.inference.StochasticTrajectoryMomentLikelihood` is a
  variant of the previous one that compares the *moments* of the
  trajectories -- their means with ``Moments=1``, or means and second
  moments with ``Moments=2`` -- rather than individual trajectories.
  This suits data that is a large collection of trajectories best
  summarized by its statistics.
- `~bioscrape.inference.StochasticStatesLikelihood` compares the
  *distribution* of simulated states to a measured distribution at each
  time point, and is the likelihood paired with population-snapshot
  `~bioscrape.inference.FlowData`.

Priors
======

Priors are specified as a dictionary mapping each parameter name to a
list whose first element names the prior type and whose remaining
elements are its arguments, e.g. ``{'k1': ['uniform', 0, 100]}`` or
``{'d1': ['gaussian', 0.2, 20, 'positive']}``.  Adding the flag
'positive' anywhere in the list constrains the parameter to
non-negative values.  The built-in prior types are:

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Type
     - Specification
     - Notes
   * - 'uniform'
     - ``['uniform', lower, upper]``
     - Uniform on ``[lower, upper]``.
   * - 'gaussian'
     - ``['gaussian', mean, std]``
     - Normal distribution.
   * - 'exponential'
     - ``['exponential', rate]``
     - Exponential with the given rate (mean ``1 / rate``).
   * - 'gamma'
     - ``['gamma', shape, rate]``
     - Gamma distribution with shape and rate parameters.
   * - 'beta'
     - ``['beta', a, b]``
     - Beta distribution (the parameter value is expected in
       ``[0, 1]``).
   * - 'log-uniform'
     - ``['log-uniform', lower, upper]``
     - Log-uniform; ``lower`` and ``upper`` must be positive.
   * - 'log-gaussian'
     - ``['log-gaussian', mean, std]``
     - Log-normal; ``mean`` and ``std`` are those of the underlying
       normal distribution.
   * - 'custom'
     - ``['custom', func]``
     - A user-supplied callable; see below.

A custom prior is given as ``['custom', func]``, where ``func`` is the
last element of the list and is a callable with signature
``func(param_name, param_value)`` that returns the log-prior
probability (returning ``numpy.inf`` rejects the value).  The built-in
prior types are implemented as methods on
`~bioscrape.pid_interfaces.PIDInterface`.

PID Interfaces
==============

`~bioscrape.pid_interfaces.PIDInterface` and its subclasses connect a
`~bioscrape.types.Model`, a set of parameters to estimate, and a prior
specification to the appropriate `~bioscrape.inference.Likelihood`:

.. currentmodule:: bioscrape.pid_interfaces

.. autosummary::
   :nosignatures:

   PIDInterface
   StochasticInference
   DeterministicInference
   LMFitInference

`~bioscrape.pid_interfaces.LMFitInference` provides a
least-squares/maximum-likelihood alternative to MCMC sampling, built
on `lmfit <https://lmfit.github.io/lmfit-py/>`_, for cases where a
point estimate (rather than a full posterior) is sufficient.

Real-world example
==================

For a worked example of these inference tools applied to experimental
data, see [Pan+23b]_, which uses `~py_inference` to fit a model of
integrase- and excisionase-mediated DNA recombination to cell-free
expression data, as part of a broader modeling and analysis pipeline
for characterizing engineered biological systems.

.. [Pan+23b] Pandey A, Rodriguez ML, Poole W, Murray RM (2023)
   Characterization of integrase and excisionase activity in a
   cell-free protein expression system using a modeling and analysis
   pipeline. *ACS Synthetic Biology* 12(2):511-523.
   https://doi.org/10.1021/acssynbio.2c00534
