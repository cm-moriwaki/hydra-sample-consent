from setuptools import setup, find_packages

setup(
    name='sample-hydra-consent',
    version='0.0.1',
    description='',
    long_description='',
    packages=find_packages(),
    zip_safe=False,
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
    include_package_data=True,
    tests_require=['nose'],
    test_suite='nose.collector'
)
