from setuptools import find_packages
from setuptools import setup


version = '1.2.1'

setup(
    name='plone.transformchain',
    version=version,
    description=("Hook into repoze.zope2 that allows third party packages "
                 "to register a sequence of hooks that will be allowed to "
                 "modify the response before it is returned to the browser"),
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='zope2 repoze transform',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://pypi.python.org/pypi/plone.transformchain',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'repoze': ['repoze.zope2'],
        'test': 'plone.testing [zca]',
    },
    install_requires=[
        'setuptools',
        'zope.interface',
        'zope.component',
        'zope.schema',
        'Zope2>=2.13.23'
    ],
    entry_points="""
    """,
)
