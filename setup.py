from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def get_requirements(file_name):
    req_path = path.join(here + '/requirements', file_name)
    with open(req_path, encoding='utf-8') as f:
        return f.read().splitlines()


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

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
    install_requires=get_requirements('default.txt'),
    setup_requires=get_requirements('test.txt'),
    test_suite='tests',
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={'console_scripts': ['micro = micro.__main__:main']}
)
