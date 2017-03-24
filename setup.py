import io

from os import path
from setuptools import setup
from quantity_field import __version__


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-quantity-field',
    long_description=long_description,
    version='.'.join(str(x) for x in __version__),
    description='Field for Django models that stores multidimensional physical quantities',
    url='https://github.com/tapeit/django-quantity-field',
    author='Evgeniy Krysanov',
    author_email='evgeniy.krysanov@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    keywords='django multiple quantity field',
    packages=['quantity_field'],
    install_requires=['Pint', 'Django>=1.8'],
)
