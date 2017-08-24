from setuptools import setup, find_packages

setup(
    name='sample-hydra-consent',
    version='0.0.1',
    description='',
    long_description='',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-login',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'run-hydra-sample-consent=hydra_sample_consent.consent:cli',
        ]
    },
    tests_require=['nose'],
    test_suite='nose.collector'
)
