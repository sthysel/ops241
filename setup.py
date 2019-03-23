# -*- encoding: utf-8 -*-
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ops241-radar',
    license='MIT',
    version='0.0.1',
    description='OPS241 Radar',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'ops241=ops241.cli:cli',
        ],
    },
    install_requires=[
        'click',
        'pygame',
        'pyserial',
    ],
    author='sthysel',
    author_email='sthysel@gmail.com',
    url='https://github.com/sthysel/ops241',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    keywords=[],
    extras_require={},
    setup_requires=[],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    zip_safe=False,
)
