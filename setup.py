from setuptools import setup, find_packages

setup(
    name='pf4pipeline',
    version='0.0.4',
    packages=find_packages(),
    include_package_data=True,
    description='Modification for pipeline of padar_features, an extension of feature computation to be used in padar package.',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas>=0.23.0",
        "numpy>=1.15.1,<=1.20.3,",
        "scipy>=1.1.0",
        "bokeh>=0.13.0"
    ],
)
