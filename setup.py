import os
from pip.req import parse_requirements
from setuptools import find_packages, setup
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def long_description() -> str:
    path = os.path.join(BASE_DIR, 'README.rst')
    with open(path, 'r') as f:
        long_description = f.read()
    return long_description


def requirements() -> List[str]:
    path = os.path.join(BASE_DIR, 'requirements', 'production.txt')
    return [str(r.req) for r in parse_requirements(path, session=False)]


setup(
    author='Brian Myers',
    author_email='brian.carl.myers@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
    ],
    description='',
    install_requires=requirements(),
    keywords='rust',
    license='MIT',
    long_description=long_description(),
    name='rustypy',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    test_suite='tests',
    url='https://www.github.com/bcmyers/rust_extension',
    version='0.1.0',
)
