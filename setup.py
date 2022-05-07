try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# NOTE: The "diffdata" package is only used to nicely display differences during testing.
#    install_requires=["diffdata"],



setup(
    name="neuroarch_nlp",
    version="0.4.0",
    description="A package for translating English queries to NeuroArch Database queries",
    long_description=open('README.md').read(),
    author="Wesley A. S. Bruning, Nikul Ukani, Yiyin Zhou",
    author_email="wesley.bruning@columbia.edu, nikul@ee.columbia.edu, yiyin@ee.columbia.edu",
    maintainer='Yiyin Zhou',
    maintainer_email='yiyin@ee.columbia.edu',
    url="https://github.com/fruitflybrain/ffbo.neuroarch_nlp",
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
        'python-Levenshtein',
        'thefuzz', 
        'datadiff',
        'spacy >= 3',
        'nltk',
        'refo @ https://github.com/fruitflybrain/refo/tarball/master#egg=refo-0.14',
    ],
    package_data = {
        'hemibrain': ['neuron_types.json']
    },
    dependency_links=['https://github.com/fruitflybrain/refo/tarball/master#egg=refo-0.14'],
    packages = find_packages()
)
