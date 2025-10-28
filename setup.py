from setuptools import setup, find_packages

setup(
    name='dask_par_for_util',
    version='0.1.0',
    description='A utility for easily embarrassingly parallelizing for loops using Dask.',
    long_description='A context-managed utility built on Dask to simplify the parallel execution of functions over an iterable list.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/dask_par_for_util',
    # List the actual Python files to be included
    py_modules=['par_for'], 
    install_requires=[
        # Core Dask package
        'dask>=2024.1.0', 
        # Distributed scheduler for multiprocessing/threading
        'distributed>=2024.1.0', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
)