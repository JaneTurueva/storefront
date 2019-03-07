import os
from importlib.machinery import SourceFileLoader

from setuptools import setup, find_packages


module_name = 'storefront'

module = SourceFileLoader(
    module_name,
    os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(fname):
    """ load requirements from a pip requirements file """
    line_iter = (line.strip() for line in open(fname))
    return [line for line in line_iter if line and not line.startswith("#")]


setup(
    name='storefront',
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    long_description=open('README.rst').read(),
    platforms="all",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
    entry_points={
        'console_scripts': [
            'storefront-api = storefront.main:main',
            'storefront-db = storefront.db:main',
      ]
    },
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    python_requires=">3.5.*, <4",
    extras_require={
        'develop': load_requirements('requirements.dev.txt'),
    },
    url='https://github.com/JaneTurueva/storefront'
)