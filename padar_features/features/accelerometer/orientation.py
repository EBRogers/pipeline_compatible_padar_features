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


class OrientationFeature:
    def __init__(self, X, subwins=4):
        OrientationFeature.check_input(X)
        self._X = X
        self._subwins = 4

    @staticmethod
    def check_input(X):
        if not validator.is_xyz_inertial(X):
            raise ValueError(
                'Input numpy array must be a 3 axis sensor')

    @staticmethod
    def orientation_xyz(X):
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

    def estimate_orientation(self):
        result = operator.apply_over_subwins(
            self._X, OrientationFeature.orientation_xyz, subwins=self._subwins)
        self._orientations = np.concatenate(result, axis=0)
        return self

    def median_x_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([median_angles[0]]))

    def median_y_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([median_angles[1]]))

    def median_z_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([median_angles[2]]))

    def range_x_angle(self):
        range_angles = np.nanmax(angles, axis=0) - np.nanmin(angles, axis=0)
        return formatter.vec2rowarr(np.array([median_angles[0]]))

    def range_y_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([median_angles[1]]))

    def range_z_angle(self):
        median_angles = np.nanmedian(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([median_angles[2]]))

    def std_x_angle(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([std_angles[0]]))

    def std_x_angle(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([std_angles[1]]))

    def std_x_angle(self):
        std_angles = np.nanstd(self._orientations, axis=0)
        return formatter.vec2rowarr(np.array([std_angles[2]]))
