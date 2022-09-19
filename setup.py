#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

#requirements = ''

test_requirements = 'pytest>=3'

setup(
    author="Jose Pedro Godinho Rodrigues Conceicao",
    author_email='pedrogodinhoc@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Demo project for a bank app",
    entry_points={
        'console_scripts': [
            'py_bank=py_bank.cli:main',
        ],
    },
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='py_bank',
    name='py_bank',
    packages=find_packages(include=['py_bank', 'py_bank.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ZordoC/py_bank',
    version='0.1.0',
    zip_safe=False,
)
