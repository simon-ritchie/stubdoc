"""The module that implements PyPI settings.
"""

from setuptools import find_packages, setup
from stubdoc import __version__

_DESCRIPTION: str = (
    'stubdoc is a Python library that append docstring to stub files.'
    '\nNotes: currently developing.'
)

_LONG_DESCRIPTION: str = (
    'stubdoc is a Python library that append docstring to stub files.'
    ' For more details, please see Github repository:'
    ' https://github.com/simon-ritchie/stubdoc/tree/main'
)

setup(
    name='stubdoc',
    version=__version__,
    url='https://github.com/simon-ritchie/stubdoc/tree/main',
    maintainer='simon-ritchie',
    maintainer_email='',
    description=_DESCRIPTION,
    long_description=_LONG_DESCRIPTION,
    packages=find_packages(
        exclude=('tests', 'samples'),
    ),
    install_requires=[],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'stubdoc = stubdoc.cli:main',
        ],
    }
)

