.. currentmodule:: bioscrape.inference

.. _inference_ref:

*********
Inference
*********

.. todo::

   This chapter is a placeholder narrative overview.  Expand once the
   inference docstrings have been normalized (see :doc:`develop`).

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
full set of MCMC samples) along with a `~bioscrape.pid_interfaces.PIDInterface`
object providing utilities for further analysis, and produces plots of
the resulting posterior parameter distributions.

Data Types
============

Experimental data is represented with one of the
`~bioscrape.inference.Data` subclasses, selected automatically by
`~py_inference` based on the shape of `exp_data`:

.. autosummary::
   :toctree: generated/
   :nosignatures:

   BulkData
   FlowData
   StochasticTrajectories

Likelihoods
=============

Each `~bioscrape.inference.Data` type is paired with a
`~bioscrape.inference.Likelihood` implementation that computes the
log-likelihood of a parameter set given the data:

.. autosummary::
   :toctree: generated/
   :nosignatures:

   DeterministicLikelihood
   StochasticTrajectoriesLikelihood
   StochasticTrajectoryMomentLikelihood
   StochasticStatesLikelihood

Priors
========

Priors are specified as a dictionary mapping parameter name to a list
describing the prior distribution, e.g.
``{'k1': ['uniform', 0, 100]}`` or
``{'d1': ['gaussian', 0.2, 20, 'positive']}`` (the optional trailing
``'positive'`` flag constrains the parameter to non-negative values).
Built-in prior types are implemented on
`~bioscrape.pid_interfaces.PIDInterface`; custom priors can be
supplied as a callable.

PID Interfaces
================

`~bioscrape.pid_interfaces.PIDInterface` and its subclasses connect a
`~bioscrape.types.Model`, a set of parameters to estimate, and a prior
specification to the appropriate `~bioscrape.inference.Likelihood`:

.. currentmodule:: bioscrape.pid_interfaces

.. autosummary::
   :toctree: generated/
   :nosignatures:

   PIDInterface
   StochasticInference
   DeterministicInference
   LMFitInference

`~bioscrape.pid_interfaces.LMFitInference` provides a
least-squares/maximum-likelihood alternative to MCMC sampling, built
on `lmfit <https://lmfit.github.io/lmfit-py/>`_, for cases where a
point estimate (rather than a full posterior) is sufficient.
