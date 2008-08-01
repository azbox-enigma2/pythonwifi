# -*- coding: latin1 -*-
from setuptools import setup, find_packages
setup(
    name = "python-wireless",
    version = "0.3.1",
    packages = find_packages(exclude='tests'),

    # metadata for upload to PyPI
    author = "R�man Joost",
    author_email = "roman@bromeco.de",
    description = """\
Python-Wireless is a Python library that provides access to information
about a W-Lan card's capabilities, like the wireless extensions
written in C.""",
    license = "LGPL",
    keywords = "wireless wlan iwconfig iwtools",
    url = "https://developer.berlios.de/projects/pythonwifi/"
    download_url = "https://developer.berlios.de/projects/pythonwifi/", 
)