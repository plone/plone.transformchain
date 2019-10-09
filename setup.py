from setuptools import find_packages
from setuptools import setup


version = '2.0.2.dev0'

setup(
    name='plone.transformchain',
    version=version,
    description=("Hook into repoze.zope2 that allows third party packages "
                 "to register a sequence of hooks that will be allowed to "
                 "modify the response before it is returned to the browser"),
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='zope2 repoze transform',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://pypi.org/project/plone.transformchain',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'repoze': ['repoze.zope2'],
        'test': 'plone.testing [zca]',
    },
    install_requires=[
        'setuptools',
        'six',
        'zope.interface',
        'zope.component',
        'zope.schema',
        'Zope2>=2.13.23'
    ],
    entry_points="""
    """,
)
