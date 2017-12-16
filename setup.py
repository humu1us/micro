from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='Micro',

    version='0.0.1',

    description='Celery platform to create microservices',
    long_description=long_description,

    url='',

    author='Felipe Ortiz, Pablo Ahumada',
    author_email='fortizc@gmail.com, pablo.ahumadadiaz@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='Microservices celery',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={'console_scripts': ['micro = micro.__main__:main']}
)
