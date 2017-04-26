# coding=utf-8
"""Install config."""
from setuptools import setup, find_packages
import os

long_description = '''A wrapper around Espeak and Mbrola, to do simple Text-To-Speech (TTS),
    with the possibility to tweak the phonemic form.'''
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name='katalixia',
    version='0.1.2',
    description='A lib to rhyme',
    url='https://github.com/hadware/katalixia',
    author='Hadware',
    author_email='hadwarez@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='rhyme phonems language',
    packages=find_packages(),
    install_requires=['voxpopuli', 'distance'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'])
