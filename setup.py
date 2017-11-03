#
# Copyright Cameron Curry (c) 2017
#

from setuptools import setup, find_packages
from questrade import __version__

install_requires = [
    'requests==2.18.4'
]

setup(
    name='questrade',
    version=__version__,
    author='Cameron Curry',
    description='Python Client for Questrade API',
    install_requires=install_requires,
    packages=find_packages(),
    test_suite='tests'
)
