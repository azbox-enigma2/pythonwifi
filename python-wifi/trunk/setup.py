# -*- coding: latin1 -*-
from setuptools import setup, find_packages


setup(
    name = "python-wireless",
    version = "0.3.1",
    packages = ['pythonwifi'],

    # metadata for upload to PyPI
    author = "Róman Joost",
    author_email = "roman@bromeco.de",
    description = """\
Python-Wireless is a Python library that provides access to information
about a W-Lan card's capabilities, like the wireless extensions
written in C.""",
    long_description = open('README.txt').read() +
        '\n\n' +
        open('NEWS').read(),
    license = "LGPL",
    keywords = "wireless wlan iwconfig iwtools",
    url = "https://developer.berlios.de/projects/pythonwifi/",
    download_url = "https://developer.berlios.de/projects/pythonwifi/", 
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)
