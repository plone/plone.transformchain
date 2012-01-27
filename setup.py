from setuptools import setup, find_packages
import os

version = '1.0.1'

setup(name='plone.transformchain',
      version=version,
      description="Hook into repoze.zope2 that allows third party packages to register a sequence of hooks that will be allowed to modify the response before it is returned to the browser",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zope2 repoze transform',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/plone.transformchain',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      extras_require={
        'repoze': ['repoze.zope2'],
        'Zope2.10': ['ZPublisherEventsBackport'],
        'test': 'plone.testing [zca]',
      },
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'zope.schema',
      ],
      entry_points="""
      """,
      )
