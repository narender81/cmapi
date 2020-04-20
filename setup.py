from distutils.core import setup

from v1 import __version__


setup(
    name="covidapi",
    version=__version__,
    packages=["v1"],
    install_requires=[" "],
    long_description=open("README.txt").read(),
    author="",
)
