"""
setup.py for bluesteel-graphics
"""
import re

from pathlib import Path

from setuptools import setup, find_packages


version_path = Path(__file__).parent.joinpath(
    'bluesteel', 'graphics', '__init__.py')
version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                    version_path.read_text(encoding='utf-8'),
                    re.M)

setup(
    name='bluesteel-graphics',
    version=version,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[''],
    extras_require={
        'test': ['pytest-flake8'],
    },
)
