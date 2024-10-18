from setuptools import setup, find_packages

setup(
    name='BatterySaviour',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'requests',
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'battery-saviour = main:main',
        ],
    },
)
