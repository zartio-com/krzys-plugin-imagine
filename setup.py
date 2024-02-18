from setuptools import setup, find_namespace_packages

setup(
    name='krzys-plugins-imagine',
    version='1.0.0',
    author="iTokajo",
    packages=find_namespace_packages(where='src/', include=['krzys.plugins.imagine']),
    package_dir={
        '': 'src'
    },
    entry_points={
        'krzys.plugins': [
            'imagine = krzys.plugins.imagine:Plugin',
        ]
    },
    install_requires=[
    ],
)
