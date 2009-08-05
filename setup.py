# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name = "python-wifi",
    version = "0.3.1",
    author = "Róman Joost",
    description = """Python WiFi is a Python module that provides read and write access to a 
wireless network card's capabilities using the Linux Wireless Extensions.""",
    packages = ['pythonwifi'],

    # metadata for upload to PyPI
    author_email = "roman@bromeco.de",
    long_description = open('README').read() +
        '\n\n' +
        open('NEWS').read(),
    license = "LGPL",
    keywords = "wifi wireless wlan iwconfig iwtools",
    url = "https://developer.berlios.de/projects/pythonwifi/",
    download_url = "https://developer.berlios.de/projects/pythonwifi/", 
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
)
