"""

Computing features about accelerometer orientations

Author: Qu Tang

Date: Jul 10, 2018
"""
import numpy as np
from numpy.linalg import norm
from .. import formatter
from .. import operator
from .. import validator
import logging


logger = logging.getLogger()


def median_orientation_xyz(X, subwins=4, want='xyz'):
    result = operator.apply_over_subwins(X, _orientation_xyz, subwins=subwins)
    angles = np.concatenate(result, axis=0)
    median_angles = np.nanmedian(angles, axis=0)
    return formatter.want_axis(median_angles, want=want)


def range_orientation_xyz(X, subwins=4, want='xyz'):
    result = operator.apply_over_subwins(X, _orientation_xyz, subwins=subwins)
    angles = np.concatenate(result, axis=0)
    range_angles = np.nanmax(angles, axis=0) - np.nanmin(angles, axis=0)
    return formatter.want_axis(range_angles, want=want)


def std_orientation_xyz(X, subwins=4, want='xyz'):
    result = operator.apply_over_subwins(X, _orientation_xyz, subwins=subwins)
    angles = np.concatenate(result, axis=0)
    std_angles = np.nanstd(angles, axis=0)
    return formatter.want_axis(std_angles, want=want)


def _orientation_xyz(X):
    _check_input(X)
    X = formatter.as_float64(X)
    if not validator.has_enough_samples(X):
        logger.warning(
            '''One of sub windows do not have enough samples, will ignore in
             feature computation''')
        orientation_xyz = np.array([np.nan, np.nan, np.nan])
    else:
        gravity = np.array(np.mean(X, axis=0), dtype=np.float)
        orientation_xyz = np.arccos(
            gravity / norm(gravity, ord=2, axis=0))
    return formatter.vec2rowarr(orientation_xyz)


def _check_input(X):
    if not validator.is_xyz_inertial(X):
        raise ValueError(
            'Input numpy array must be a 3 axis sensor')
