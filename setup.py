from setuptools import setup, find_packages

setup(
    name='parakyt',
    version='1.0.0',
    description='A utility for easily embarrassingly parallelizing for loops using Dask.',
    long_description='A context-managed utility built on Dask to simplify the parallel execution of functions over an iterable list.',
    author='Keenan M Stone',
    author_email='lemma137@gmail.com',
    url='https://github.com/Keenan-M-Stone/parakyt',
    packages=find_packages(), 
    install_requires=[
        # Core Dask package
        'dask>=2025.7.0', 
        # Distributed scheduler for multiprocessing/threading
        'distributed>=2025.7.0', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.11.13',
)
