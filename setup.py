#!/usr/bin/python3
"""Setup
"""
from setuptools import find_packages
from distutils.core import setup

version = "0.0.2"

with open('README.md') as f:
    long_description = f.read()

setup(name='ofxstatement-sparkasse-freiburg',
      version=version,
      author="Omar Kohl",
      author_email="omarkohl@gmail.com",
      url="https://github.com/omarkohl/ofxstatement-sparkasse-freiburg",
      description=("ofxstatement plugin for German bank Sparkasse Freiburg-Nördlicher Breisgau"),
      long_description=long_description,
      long_description_content_type='text/markdown',
      license="MIT",
      keywords=["ofx", "banking", "statement"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          'ofxstatement':
          ['germany_sparkasse_freiburg = ofxstatement.plugins.germany_sparkasse_freiburg:SparkasseFreiburgPlugin']
          },
      install_requires=['ofxstatement'],
      include_package_data=True,
      zip_safe=True
      )
