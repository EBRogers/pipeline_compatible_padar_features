from padar_features.libs.signal_generator import SignalGenerator
from padar_features.features.accelerometer.spectrum import FrequencyFeature
from padar_features.FeatureExtractor import FeatureExtractor
import sys
from bokeh.plotting import show
from clize import run


def SpectrumInspector(file_path):
    data = FeatureExtractor._import_data(file_path, 'accelerometer')
    data = data.set_index(data.columns[0])
    show(FrequencyFeature(data.values, 80).fft().peaks().visualize())


if __name__ == '__main__':
    run(SpectrumInspector)