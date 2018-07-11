"""
=======================================================================
Frequency features
=======================================================================
'''Frequency domain features for numerical time series data'''
"""
from scipy import signal, interpolate
import numpy as np
from ...libs.signal_processing.detect_peaks import detect_peaks
from .. import validator
from .. import formatter


def frequency_features(X, sr, freq_range=None, top_n_dominant=1, want='all'):
    '''compute frequency features for each axis, result will be aligned in the 
    order of f1,f2,...,p1,p2,..,pt for each axis
    '''
    freq, Sxx = _spectrum(X, sr, freq_range)
    Sxx = formatter.vec2colarr
    result = []
    if len(Sxx.shape) == 1:
        Sxx = np.reshape(Sxx, (Sxx.shape[0], 1))
    elif len(Sxx.shape) == 0:
        return result

    for n in range(0, Sxx.shape[1]):
        # Get dominant frequencies
        freq_peaks, Sxx_peaks = _peaks(Sxx[:, n], freq)
        result_freq = freq_peaks[0:top_n_dominant]
        result_Sxx = Sxx_peaks[0:top_n_dominant]
        if result_freq.shape[0] < top_n_dominant:
            result_freq = np.append(result_freq, np.zeros(
                (top_n_dominant - result_freq.shape[0],)))
            result_Sxx = np.append(result_Sxx, np.zeros(
                (top_n_dominant - result_Sxx.shape[0],)))
        # Get total power
        total_power = [np.sum(Sxx[:, n])]

        # Get power of band > 3.5Hz
        highend_power = [np.sum(Sxx[freq > 3.5, n])]

        result = np.concatenate(
            (result, result_freq, result_Sxx, total_power, highend_power))
    return result


def _check_input(X):
    if not validator.is_xyz_inertial(X) and not validator.is_vm_inertial(X):
        raise ValueError(
            'Input numpy array must be a 3 axis sensor or in vector magnitude')


def _want(result, want='all'):



def _spectrum(X, sr, freq_range=None):
    freq, time, Sxx = signal.spectrogram(
        X,
        fs=sr,
        window='hamming',
        nperseg=X.shape[0],
        noverlap=0,
        detrend='constant',
        return_onesided=True,
        scaling='density',
        axis=0,
        mode='psd')
    # interpolate to get values in the freq_range
    if freq_range is not None:
        interpolate_f = interpolate(freq, Sxx)
        Sxx_interpolated = interpolate_f(freq_range)
    else:
        freq_range = freq
        Sxx_interpolated = Sxx
    Sxx_interpolated = np.squeeze(Sxx_interpolated)
    return (freq_range, Sxx_interpolated)


def _peaks(y, x, sort='descend'):
    y = y.flatten()
    locs = detect_peaks(y)
    y_peaks = y[locs]
    x_peaks = x[locs]
    sorted_locs = np.argsort(y_peaks, kind='quicksort')
    if sort == 'descend':
        sorted_locs = sorted_locs[::-1][:len(sorted_locs)]
    y_sorted_peaks = y_peaks[sorted_locs]
    x_sorted_peaks = x_peaks[sorted_locs]
    return (x_sorted_peaks, y_sorted_peaks)
