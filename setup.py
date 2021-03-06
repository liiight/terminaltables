#!/usr/bin/env python
"""Setup script for the project."""

from __future__ import print_function

import codecs
import os
import re

from setuptools import Command, setup

AUTHOR = '@Robpol86'
INSTALL_REQUIRES = []
LICENSE = 'MIT'
NAME = IMPORT = 'terminaltables'
VERSION = '3.0.0'


def readme(path='README.rst'):
    """Try to read README.rst or return empty string if failed.

    :param str path: Path to README file.

    :return: File contents.
    :rtype: str
    """
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    handle = None
    url_prefix = 'https://raw.githubusercontent.com/Robpol86/{name}/v{version}/'.format(name=NAME, version=VERSION)
    try:
        handle = codecs.open(path, encoding='utf-8')
        return handle.read(131072).replace('.. image:: docs', '.. image:: {0}docs'.format(url_prefix))
    except IOError:
        return ''
    finally:
        getattr(handle, 'close', lambda: None)()


class CheckVersion(Command):
    """Make sure version strings and other metadata match here, in module/package, tox, and other places."""

    description = 'verify consistent version/etc strings in project'
    user_options = []

    @classmethod
    def initialize_options(cls):
        """Required by distutils."""
        pass

    @classmethod
    def finalize_options(cls):
        """Required by distutils."""
        pass

    @classmethod
    def run(cls):
        """Check variables."""
        project = __import__(IMPORT)
        for expected, var in [(AUTHOR, '__author__'), (LICENSE, '__license__'), (VERSION, '__version__')]:
            if getattr(project, var) != expected:
                raise SystemExit('Mismatch: {0}'.format(var))
        # Check changelog.
        if not re.compile(r'^%s - \d{4}-\d{2}-\d{2}$' % VERSION, re.MULTILINE).search(readme()):
            raise SystemExit('Version not found in readme/changelog file.')
        # Check tox.
        if INSTALL_REQUIRES:
            in_tox = re.findall(r'\ninstall_requires =\n(?:    ([^=]+)==[\w\d.-]+\n)+?', readme('tox.ini'))
            if set(INSTALL_REQUIRES) != set(in_tox):
                raise SystemExit('Missing pinned dependencies in tox.ini.')


setup(
    author=AUTHOR,
    author_email='robpol86@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Markup',
    ],
    cmdclass=dict(check_version=CheckVersion),
    description='Generate simple tables in terminals from a nested list of strings.',
    install_requires=INSTALL_REQUIRES,
    keywords='Shell Bash ANSI ASCII terminal tables',
    license=LICENSE,
    long_description=readme(),
    name=NAME,
    packages=[IMPORT],
    url='https://github.com/{0}/{1}'.format(AUTHOR, NAME),
    version=VERSION,
    zip_safe=True,
)
