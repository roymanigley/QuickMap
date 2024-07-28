from setuptools import setup

long_description = open('README.md', "rt").read()

setup(
    name='quickmap',
    version='1.0.1',
    description='Quick and Simple Class-to-Dict Mapping for Python using decorators',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roymanigley/QuickMap',
    author='Roy Manigley',
    author_email='roy.manigley@gmail.com',
    license='MIT',
    packages=['quickmap'],
    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
)
