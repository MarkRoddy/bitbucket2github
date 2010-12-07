#!/usr/bin/env python

project = 'bitbucket2github'
version = 0.1

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

install_requires = [
    # -*- Extra requirements: -*-
    'github2',
    'hg-git',
    'scriptine',
    'vault',
    ]


setup(name=project,
      version=version,
      description="Mirrors all public repos of a BitBucket account to GitHub and vice versa.",
      long_description=open('README').read(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Software Development',
      ],
      platforms='any',
      keywords='github bitbucket bitbucket2github github2bitbucket',
      author='Ramana',
      author_email='sramana9@gmail.com',
      url='http://bitbucket.org/sramana/bitbucket2github',
      license='BSD',
      zip_safe=False,

      packages=find_packages(),
      py_modules = ['distribute_setup'],
      install_requires=install_requires,

      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      bitbucket2github=bitbucket2github.bitbucket2github:main
      github2bitbucket=bitbucket2github.github2bitbucket:main
      """
     )
