
from setuptools import setup, find_packages


setup(
    name = "dtrove",
    version = "0.1",
    packages = find_packages(),
    #install_requires = ['docutils>=0.3'],
    package_data = {
        '': ['*.html'],
    },
)
