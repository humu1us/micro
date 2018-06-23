import os
import re
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*folders):
    with codecs.open(os.path.join(here, *folders), encoding='utf-8') as f:
        return f.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("ERROR: version not found")


def get_requirements(file_name):
    requires_file = read('requirements', file_name)
    return requires_file.splitlines()


long_description = read('README.rst')

setup(
    name='Micro',

    version=find_version('micro', '__init__.py'),

    description='Celery platform to create microservices',
    long_description=long_description,

    url='https://github.com/humu1us/micro',

    author='Felipe Ortiz, Pablo Ahumada',
    author_email='fortizc@gmail.com, pablo.ahumadadiaz@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: System',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='microservices celery',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=get_requirements('default.txt'),
    setup_requires=get_requirements('test.txt'),
    test_suite='tests',
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={'console_scripts': ['micro = micro.__main__:main']}
)
