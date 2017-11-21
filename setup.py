from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='notifier',

    version='0.0.1',

    description='Celery application to notify anything to elsewhere',
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

    keywords='Messages',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
