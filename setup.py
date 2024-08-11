from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='Dmhylib',
    version='2.0.0',
    packages=find_packages(exclude=['tests*']),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': ['dmhysearch=dmhylib.cli:main'],
    },
    author='adogecheems',
    author_email='adogecheems@outlook.com',
    description='A library for searching and downloading from dmhy.org.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adogecheems/Dmhylib/',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='dmhy search download anime',
)
