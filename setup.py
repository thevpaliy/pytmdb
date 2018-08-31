from setuptools import setup
import os
import re

base_path = os.path.dirname(__file__)

with open(os.path.join(base_path, 'tmdb', '__init__.py')) as fp:
    VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(fp.read()).group(1)

version = VERSION

setup(
    name='pytmdb',
    version=version,
    description='A wrapper for the TMDB API',
    author='Vasyl Paliy',
    author_email='vpaliy97@gmail.com',
    url='https://github.com/thevpaliy/pytmdb',
    license='MIT',
    packages=['tmdb'],
    include_package_data=True,
    install_requires=[
        'requests>=2.0',
        'simplejson>=2.0',
    ],
    test_suite='test',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
)
