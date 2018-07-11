"""

Computing features of descriptive statistics

Author: Qu Tang

Date: Jul 10, 2018

"""
import numpy as np
from .. import validator
from .. import formatter


def mean(X):
    _check_input(X)
    X = formatter.as_float64(X)
    return formatter.vec2rowarr(np.nanmean(X, axis=0))


def std(X):
    _check_input(X)
    X = formatter.as_float64(X)
    return formatter.vec2rowarr(np.nanstd(X, axis=0))


def positive_amplitude(X):
    _check_input(X)
    X = formatter.as_float64(X)
    return formatter.vec2rowarr(np.nanmax(X, axis=0))


def negative_amplitude(X):
    _check_input(X)
    X = formatter.as_float64(X)
    return formatter.vec2rowarr(np.nanmin(X, axis=0))


def amplitude_range(X):
    _check_input(X)
    X = formatter.as_float64(X)
    return formatter.vec2rowarr(positive_amplitude(X) - negative_amplitude(X))


def amplitude(X):
    _check_input(X)
    X = formatter.as_float64(X)
    return formatter.vec2rowarr(np.nanmax(np.abs(X), axis=0))


def mean_distance(X):
    '''
    Compute mean distance, the mean of the absolute difference between value
     and mean. Also known as 1st order central moment.
    '''
    _check_input(X)
    X = formatter.as_float64(X)
    return mean(np.abs(X - mean(X)), axis=0)


def _check_input(X):
    if not validator.is_xyz_inertial(X) and not validator.is_vm_inertial(X):
        raise ValueError(
            'Input numpy array must be a 3 axis sensor or in vector magnitude')
