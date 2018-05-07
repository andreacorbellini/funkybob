import os
from setuptools import setup


def readme():
    path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(path) as fp:
        return fp.read()


setup(
    name='funkybob',
    packages=['funkybob'],
    version='2018.05.1',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Andrea Corbellini',
    author_email='corbellini.andrea@gmail.com',
    url='https://github.com/andreacorbellini/funkybob',
    setup_requires=['setuptools>=38.6.0'],
)
