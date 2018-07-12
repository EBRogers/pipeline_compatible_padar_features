"""

Feature extractor top-level interface

"""
import pandas as pd
from clize import run
import numpy as np


def rowarr2df(X, st, et):
    df = pd.DataFrame(index=[0], data=X, columns=range(0, X.shape[1]))
    df.insert(0, 'START_TIME', st)
    df.insert(1, 'STOP_TIME', et)
    df = df.set_index(['START_TIME', 'STOP_TIME'])
    return df


class FeatureExtractor:
    def __init__(self, segment='sliding',
                 window_size=12.8, step_size=12.8):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self._segment = segment
        self._ws = window_size
        self._ss = step_size

    def import_data(self, file_path, sensor_type):
        self._file_path = file_path
        self._sensor_type = sensor_type
        if self._sensor_type == 'accelerometer':
            self._data = pd.read_csv(self._file_path, parse_dates=[0],
                                     infer_datetime_format=True,
                                     usecols=range(0, 4))
            self._data.columns = ['HEADER_TIME_STAMP', 'X', 'Y', 'Z']

    def _no_segment(self, func):
        data = self._data.set_index(self._data.columns[0])
        result_arr = func(data.values)
        result_df = rowarr2df(
            result_arr, st=data.index.values[0],
            et=data.index.values[-1])
        result_df.columns = [func.__name__.upper(
        ) + '_' + str(col) for col in result_df.columns]
        return result_df

    def _segment_by_sliding(self, func):
        data = self._data.set_index(self._data.columns[0])
        freq = str(self._ws * 1000) + 'L'
        result_df = data.groupby(pd.Grouper(level='HEADER_TIME_STAMP',
                                            freq=freq,
                                            closed='right')).apply(
            lambda rows: rowarr2df(
                func(rows.values), st=rows.index.values[0],
                et=rows.index.values[-1])
        )
        result_df.columns = [func.__name__.upper(
        ) + '_' + str(col) for col in result_df.columns]
        return result_df

    def compute(self, func):
        if self._segment == 'no':
            return self._no_segment(func)
        elif self._segment == 'sliding':
            return self._segment_by_sliding(func)
        else:
            raise NotImplementedError("Other segment mode is not implemented")

    @staticmethod
    def cmd(func):
        def wrapped_func(file_path, *,
                         sensor_type='accelerometer',
                         segment='sliding',
                         window_size=12.8, step_size=12.8):
            extractor = FeatureExtractor(
                segment=segment, window_size=window_size, step_size=step_size)
            extractor.import_data(file_path, sensor_type)
            result = extractor.compute(func)
            print(result.describe())
            return result
        return wrapped_func


if __name__ == '__main__':

    @FeatureExtractor.cmd
    def mean(X):
        return np.reshape(np.mean(X, axis=0), (1, 3))

    run(mean)
