#!/usr/bin/env python
from cloudwatch import __version__

sdict = {
    'name': 'cloudwatchplugins',
    'version': __version__,
    'description': 'Collection of plugins for custom CloudWatch metrics.',
    'url': 'http://github.com/brooklynpacket/cloudwatch-plugins',
    'author': 'Trevor Rundell',
    'author_email': 'trun@tinyco.com',
    'maintainer': 'Trevor Rundell',
    'maintainer_email': 'trun@tinyco.com',
    'packages': ['cloudwatch'],
    'scripts': [ 'bin/cloudwatch-monitor'],
    'install_requires': [
        'boto >=2.1.1',
        'requests >= 0.7.6',
    ],
}

from setuptools import setup

setup(**sdict)
