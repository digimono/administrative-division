# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='zx-adm',
    version='1.0.0',
    description='Administrative-division',
    long_description='Administrative-division',

    keywords=[
        'administrative-division',
        'scrapy',
    ],

    url='https://github.com/digimono/administrative-division',

    author='yangyanju',
    author_email='yanjuyq@gmail.com',

    maintainer='yangyanju',
    maintainer_email='yanjuyq@gmail.com',

    packages=find_packages(
        where='.',
        exclude=('tests',),
        include=('*',),
    ),

    license='Apache License 2.0',

    classifiers=[
        'License :: OSI Approved :: Apache License 2.0',

        'Programming Language :: Python :: 3.7',
    ],

    include_package_data=True,
    platforms="any",
    zip_safe=False,

    install_requires=[
        'scrapy>=1.6.0'
    ],

    scripts=[],
    entry_points={
        'console_scripts': [
            'get-zx-adm = administrative_division.run:main'
        ]
    },
)
