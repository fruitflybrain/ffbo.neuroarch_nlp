try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# NOTE: The "diffdata" package is only used to nicely display differences during testing.
#    install_requires=["diffdata"],



setup(
    name="neuroarch_nlp",
    version="0.1.2",
    description="",
    long_description=open('README.md').read(),
    author="Wesley A. S. Bruning",
    author_email="wesley.bruning@columbia.edu",
    url="TBD",
    keywords=["NLP",
              "natural language processing",
              "natural language interface to database"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing"
        ],
    install_requires = [
        'fuzzywuzzy >= 0.12.0', 'datadiff'
    ],
    packages = find_packages()
)
