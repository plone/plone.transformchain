from setuptools import find_packages
from setuptools import setup


version = "3.0.0"

setup(
    name="plone.transformchain",
    version=version,
    description=(
        "Hook into repoze.zope2 that allows third party packages "
        "to register a sequence of hooks that will be allowed to "
        "modify the response before it is returned to the browser"
    ),
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="zope2 repoze transform",
    author="Martin Aspeli",
    author_email="optilude@gmail.com",
    url="https://pypi.org/project/plone.transformchain",
    license="BSD",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    extras_require={
        "test": "plone.testing [zca]",
    },
    install_requires=[
        "setuptools",
        "Zope",
    ],
    entry_points="""
    """,
)
