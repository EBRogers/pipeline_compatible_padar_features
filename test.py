
if __name__ == '__main__':
    from clize import run
    from padar_features.FeatureExtractor import FeatureExtractor
    from padar_features.features.accelerometer import stats, spectrum, orientation
    import logging
    import sys
    import pandas as pd

    @FeatureExtractor.cmd
    def features(X, sr):
        freq = spectrum.FrequencyFeature(X, sr=sr)
        freq.fft().peaks()
        ori = orientation.OrientationFeature(X, subwins=1800)
        ori.estimate_orientation(unit='deg')

        return pd.concat([
            stats.mean(X),
            stats.std(X),
            stats.positive_amplitude(X),
            stats.negative_amplitude(X),
            stats.amplitude_range(X),
            freq.dominant_frequency(n=1),
            freq.highend_power(),
            freq.dominant_frequency_power_ratio(n=1),
            freq.total_power(),
            ori.median_angles(),
            ori.range_angles(),
            ori.std_angles()
        ], axis=1)

    run(features)
