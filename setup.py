# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name = "python-wifi",
    version = "0.3.1",
    author = "Róman Joost",
    author_email = "roman@bromeco.de",
    maintainer = "Sean Robinson",
    maintainer_email = "pythonwifi-dev@lists.berlios.de",
    description = """Python WiFi is a Python module that provides read and write access to a 
wireless network card's capabilities using the Linux Wireless Extensions.""",
    packages = ['pythonwifi'],

    # metadata for upload to PyPI
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
