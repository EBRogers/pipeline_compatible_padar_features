from scipy import signal
import numpy as np

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
    # if freq_range is not None:
    #     interpolate_f = interpolate(freq, Sxx)
    #     Sxx_interpolated = interpolate_f(freq_range)
    # else:
    #     freq_range = freq
    #     Sxx_interpolated = Sxx
    # Sxx_interpolated = np.squeeze(Sxx_interpolated)
    # return (freq_range, Sxx_interpolated)
    return freq, time, Sxx

fs = 10e3
N = 1e5
amp = 2 * np.sqrt(2)
noise_power = 0.01 * fs / 2
time = np.arange(N) / float(fs)
mod = 500*np.cos(2*np.pi*0.25*time)
carrier = amp * np.sin(2*np.pi*3e3*time + mod)
noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
noise *= np.exp(-time/5)
x = carrier + noise

f, t, Sxx = _spectrum(x, fs)
print(f.shape)
print(Sxx.shape)