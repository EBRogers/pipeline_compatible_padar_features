from setuptools import setup, find_packages

setup(
    name='padar_features',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    description='Extension of feature computation to be used in padar package, modified for Pipeline',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas>=0.23.0",
        "numpy>=1.15.1",
        "scipy>=1.1.0",
        "bokeh>=0.13.0"
    ],
)
