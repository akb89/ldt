from setuptools import setup

setup(
    name='ldt',
    version='0.1.0',
    url='http://ldtoolkit.space/',
    license='Apache Software License',
    author='Anna Rogers',
    tests_require=['pytest'],
    install_requires=["ruamel.yaml", "wiktionaryparser==0.0.7",
                      "hurry.filesize", "timeout-decorator", "inflect",
                      "nltk", "vecto", "pandas", "pyenchant", "outdated",
                      "p_tqdm"],
    # cmdclass={'test': PyTest},# "install": Install},
    author_email='anna_rogers@uml.edu',
    description='Linguistic diagnostics for word embeddings',
    long_description='',
    packages=['ldt', 'ldt.dicts', 'ldt.experiments', 'ldt.helpers',
              'ldt.relations'],
    package_dir={"ldt":"ldt"},
    include_package_data=True,
    package_data={'ldt': ['test/sample_files/ldt-config.yaml']},
    entry_points={},
    zip_safe=False,
    platforms='any',
    test_suite='ldt.test.test_ldt',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        "Topic :: Text Processing :: Linguistic"
        ],
    extras_require = {
        'testing': ['pytest'],
    }
)
