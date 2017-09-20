import os

from setuptools import setup


ROOT = os.path.dirname(os.path.realpath(__file__))


setup(
    name='pyboost',
    description="C++Boost as a Python package",

    author="Stefan Zimmermann",
    author_email="user@zimmermann.co",
    url="https://github.com/zimmermanncode/pyboost",

    license='LGPLv3',

    setup_requires=open(os.path.join(ROOT, 'requirements.setup.txt')).read(),
    install_requires=open(os.path.join(ROOT, 'requirements.txt')).read(),

    use_scm_version={
        'local_scheme': lambda _: '',
        'write_to': 'Boost/__version__.py',
    },
    packages=[
        'Boost',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved'
        ' :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    keywords=[
        'pyboost', 'boost', 'python3', 'packaging',
        'c++', 'cpp', 'cxx', 'cplusplus',
        'libraries', 'libs', 'library', 'lib',
        'boostpython',
    ],
)
