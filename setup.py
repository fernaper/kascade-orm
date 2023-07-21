#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List
from pathlib import Path
from setuptools import setup, find_packages


def requirements(name: str) -> List[str]:
    root = Path(__file__).parent / 'requirements'
    return root.joinpath(name).read_text().splitlines()


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

version = ''
with open('src/kascade/__init__.py', encoding='utf-8') as f:
    match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    )
    if not match:
        raise RuntimeError('version is not set')

    version = match.group(1)

if not version:
    raise RuntimeError('version is not set')


extras = {
    'mysql': requirements('mysql.txt'),
    'postgresql': requirements('postgresql.txt'),
    'sqlite': requirements('sqlite.txt'),
}

setup(
    name='kascade',
    version=version,
    author='Fernando Pérez',
    author_email='fernaperg@gmail.com',
    maintainer='Fernando Pérez',
    license='Mit',
    url='https://github.com/fernaper/kascade-orm',
    description='Python ORM for SQL Databases based on Pydantic',
    install_requires=requirements('base.txt'),
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(
        where='src',
        include=['kascade', 'kascade.*',],
    ),
    package_dir={'': 'src'},
    python_requires='>=3.10.6',
    #package_data={'': ['generator/templates/**/*.py.jinja', 'py.typed']},
    include_package_data=True,
    zip_safe=False,
    extras_require={
        **extras,
        'all': [
            req for requirements in extras.values() for req in requirements
        ],
    },
    entry_points={
        'console_scripts': [
            'kascade=kascade.cli:main',
        ],
        'kascade': [],
    },
    project_urls={
        'Documentation': 'https://kascade.readthedocs.io',
        'Source': 'https://github.com/fernaper/kascade-orm',
        'Tracker': 'https://github.com/fernaper/kascade-orm/issues',
    },
    keywords=[
        'orm',
        'mysql',
        'typing',
        'pydantic',
        'kascade',
        'sqlite',
        'database',
        'postgresql',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Typing :: Typed',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
    ],
)