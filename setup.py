"""Setup for helot mysql library.

The setup is using implicit namespace packages from PEP 420 so exported
packages exported packages must be explicitly listed using the packages
parameter of the setup function ( find_packages will not work as expected
for more you can read here:
https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

"""
from setuptools import setup

setup(
    name="helot_mysql",
    description="Exposes a mysql wrapper.",
    long_description="Exposes a mysql wrapper",
    url="https://github.com/jpazarzis/helot_mysql",
    author="John Pazarzis",
    install_requires=[
        "helot_common",
    ],
    packages=["helot.mysql"],
    version='0.0.1',
)
