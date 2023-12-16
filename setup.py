from setuptools import setup

setup(
    name='NTLMCrack',
    version='0.1',
    py_modules=['NTLMCrack'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'NTLMCrack = NTLMCrack:main',
        ],
    },
)
