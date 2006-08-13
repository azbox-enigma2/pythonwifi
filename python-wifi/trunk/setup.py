# -*- coding: latin1 -*-
from setuptools import setup, find_packages
setup(
    name = "python-wireless",
    version = "0.3",
    packages = find_packages(exclude='tests'),

    # metadata for upload to PyPI
    author = "Róman Joost",
    author_email = "roman@bromeco.de",
    description = """\
Python-Wireless is a Python library that provides access to information
about a W-Lan card's capabilities, like the wireless extensions
written in C.""",
    license = "LGPL",
    keywords = "wireless wlan iwconfig iwtools",
    url = "http://www.romanofski.de/downloads/pywifi", 
    download_url = "http://www.romanofski.de/downloads/pywifi", 
)
