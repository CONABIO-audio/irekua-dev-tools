import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='irekua-dev-tools',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Tools for Irekua/Selia system development',
    long_description=README,
    url='',
    author='CONABIO, Gustavo Everardo Robredo Esquivelzeta, Santiago Martínez Balvanera',
    author_email='erobredo@conabio.gob.mx, smartinez@conabio.gob.mx',
    install_requires=[
        'Click',
        'colorama',
        'pygments',
        'virtualenv',
        'watchdog',
        'psycopg2_binary',
    ],
    entry_points='''
        [console_scripts]
        irekua=irekua_dev_tools.cli:cli
    ''',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
