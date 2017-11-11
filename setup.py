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
    url='https://github.com/catcombo/django-quantity-field',
    author='Evgeniy Krysanov',
    author_email='evgeniy.krysanov@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='django multiple quantity field',
    packages=['quantity_field'],
    install_requires=['Pint'],
)
